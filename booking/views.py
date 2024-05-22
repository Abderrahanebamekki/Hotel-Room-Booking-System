from msilib import Table

import qrcode
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import jwt
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

from hotel.models import Hotel
from user.models import Client, User
from .models import Booking, BookingRoom, Room
from django.db import connection


class BookingRoomView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"message": "Authorization header missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationFailed('Unauthenticated!')

        data = request.data
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        address = data.get('address')
        email = data.get('email')
        phone = data.get('phone')
        rooms = data.get('rooms', [])
        id_hotel = data.get('id_hotel')
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        num_adults = data.get('num_adults')

        try:
            check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")
            if num_adults is not None:
                num_adults = int(num_adults)
        except ValueError:
            return Response('Invalid data format', status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=payload['user_id'])
        client = Client(first_name=firstname , last_name=lastname , email=email ,address=address,phone=phone , user=user)
        client.save()


        booking_date = datetime.now()
        booking = Booking(
            client=client,
            check_in=check_in_date,
            check_out=check_out_date,
            num_adults=num_adults,
            total_price=0,
            booking_date=booking_date
        )

        booking.save()

        total_price = 0
        room_details = []

        for room in rooms:
            room_type = room.get('type')
            room_number = room.get('number')
            list_room = []
            price = 0

            with connection.cursor() as cursor:
                cursor.callproc('check_available_room_type', [room_type, id_hotel, check_in_date, check_out_date])
                for row in cursor.fetchall():
                    list_room.append(row[0])
                    price = row[1]

            if not list_room:
                return Response(f'No available rooms of type {room_type}', status=status.HTTP_404_NOT_FOUND)

            for i in range(int(room_number)):
                if i >= len(list_room):
                    return Response(f'Not enough rooms of type {room_type} available', status=status.HTTP_400_BAD_REQUEST)

                booking_room = BookingRoom(
                    booking=booking,
                    room=Room.objects.get(id=list_room[i])
                )
                booking_room.save()

            total_price += price * room_number
            room_details.append({'type': room_type, 'number': room_number, 'price': price})

        booking.total_price = total_price
        booking.save()
        hotel = Hotel.objects.get(id=id_hotel)
        # Generate PDF
        pdf_path = self.generate_pdf(booking, room_details , hotel)

        # Send Email with PDF
        self.send_email_with_pdf(pdf_path, email)

        return Response('Booking created successfully', status=status.HTTP_201_CREATED)

    def generate_pdf(self, booking, room_details , hotel):
        pdf_path = f'D:/pdf_memo/booking_{booking.id}.pdf'
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Draw the title at the top center
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2.0, height - 40, "People's Democratic Republic of Algeria")

        # Draw user information on the right side
        c.setFont("Helvetica", 10)
        user_info = [
            f"First Name: {booking.client.first_name}",
            f"Last Name: {booking.client.last_name}",
            f"Email: {booking.client.email}"
        ]
        y = height - 100
        for info in user_info:
            c.drawString(width - 200, y, info)
            y -= 20

        # Draw the table for room details
        table_data = [['Room Type', 'Number of Rooms', 'Price']]
        for room in room_details:
            table_data.append([room['type'], room['number'], f'{room['price']}$'])

        table = Table(table_data, colWidths=[200, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        table.wrapOn(c, width, height)
        table.drawOn(c, 50, y - 50)

        # Calculate new y-coordinate after the table
        y -= 50 + 20 * len(room_details)

        # Draw the total price
        c.drawString(50, y - 30, f"Total Price: {booking.total_price}$")

        # Generate and draw a QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(booking.client.id)
        qr.make(fit=True)

        qr_img = qr.make_image(fill='black', back_color='white')
        qr_img_path = f'D:/pdf_memo/qr_{booking.client.id}.png'
        qr_img.save(qr_img_path)

        c.drawImage(qr_img_path, 50, y - 130, width=100, height=100)

        # Draw a line
        c.line(50, y - 150, width - 50, y - 150)

        # Draw hotel information below the line
        hotel_info = [
            f"Hotel Name: {hotel.name}",
            f"Number of Stars: {hotel.nb_star}",
            f"Email: {hotel.email}",
            f"Phone Number: {hotel.phone_num}"
        ]
        y -= 170
        for info in hotel_info:
            c.drawString(50, y, info)
            y -= 20

        c.save()
        return pdf_path

    def send_email_with_pdf(self, pdf_path, to_email):
        email = EmailMessage(
            'Hotel Booking Confirmation',
            'Please find attached your booking confirmation.',
            'timibamekki49@gmail.com',  # Replace with your email
            [to_email],
        )
        email.attach_file(pdf_path)
        email.send()


class GetBookingsView(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"message": "Authorization header missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationFailed('Unauthenticated!')

        id_client = Client.objects.get(user=payload['user_id'])
        client = Client.objects.get(id=id_client)
        list_booking = Booking.objects.filter(client=client)

        # Create a new list with only check_in and check_out
        bookings_data = [
            {'check_in': booking.check_in, 'check_out': booking.check_out , 'id':booking.id} for booking in list_booking
        ]

        return Response({'bookings': bookings_data})


class UpdateBookingView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"message": "Authorization header missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationFailed('Unauthenticated!')

        id_booking = request.data.get('id_booking')
        if not id_booking:
            return Response({'message': 'Booking ID missing.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.get(id=id_booking)
        except Booking.DoesNotExist:
            return Response({'message': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_check_in_date_str = request.data.get('check_in')
        new_check_out_date_str = request.data.get('check_out')

        if not new_check_in_date_str or not new_check_out_date_str:
            return Response({'message': 'Check-in or check-out date missing.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_check_in_date = datetime.strptime(new_check_in_date_str, '%Y-%m-%d %H:%M:%S')
            new_check_out_date = datetime.strptime(new_check_out_date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return Response({'message': 'Invalid date format.'}, status=status.HTTP_400_BAD_REQUEST)


        now = datetime.now()
        hours_difference = (new_check_in_date - now).total_seconds() / 3600

        if hours_difference < 48:
            return Response({'message': 'Cannot modify booking within 48 hours of check-in date.'},status=status.HTTP_400_BAD_REQUEST)

        # Update booking
        booking.check_in = new_check_in_date
        booking.check_out = new_check_out_date
        booking.save()

        return Response({'message': 'Booking updated successfully.'}, status=status.HTTP_200_OK)


class CancelBookingView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"message": "Authorization header missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationFailed('Unauthenticated!')

        id_booking = request.data.get('id_booking')
        if not id_booking:
            return Response({"message": "Booking ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.get(id=id_booking)
        except Booking.DoesNotExist:
            return Response({'message': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        time_difference = booking.check_in - datetime.now()
        hours_difference = time_difference.total_seconds() / 3600

        if hours_difference > 48:
            booking.delete()
            return Response({'message': 'Booking canceled successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Booking cannot be canceled less than 48 hours before check-in.'}, status=status.HTTP_400_BAD_REQUEST)

