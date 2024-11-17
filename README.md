# Hotel Room Booking System (Backend-Only)
The Hotel Room Booking System Backend is designed to handle all the server-side operations required for booking hotel rooms. It provides APIs to manage room availability, process bookings, and store user data. The backend serves as the backbone of the system, ensuring secure and efficient data handling for a smooth user experience.

# API Endpoints

## Authentication & User Management Endpoints

### 1. Register
- **URL**: `api/register/`
- **Method**: `POST`
- **Description**: Allows new users to register by providing necessary details (username, password, and fullname).

### 2. Login
- **URL**: `api/login/`
- **Method**: `POST`
- **Description**: Authenticates users and provides a token for secure access to protected resources.


### 4. Logout
- **URL**: `api/logout/`
- **Method**: `POST`
- **Description**: Logs out the user by invalidating their authentication token.

### 5. Verify Code
- **URL**: `api/verify/`
- **Method**: `POST`
- **Description**: Verifies a user-provided code, used for email verification during registration .

### 6. Forget Password
- **URL**: `api/forgetpassword/`
- **Method**: `POST`
- **Description**: Initiates the password recovery process by sending a reset link to the user's email.

### 7. Change Password
- **URL**: `api/change_password/`
- **Method**: `POST`
- **Description**: Allows users to change their password after providing the current password and the new password.

### 8. User Profile
- **URL**: `api/users/`
- **Method**: `GET`
- **Description**: Fetches details about the authenticated user.

### 9. Activate Account
- **URL**: `api/activate/`
- **Method**: `POST`
- **Description**: Activates a user account using a code sent to their email , completing the registration process.

## Hotel Booking Endpoints

### Search Hotels
- **URL**: `api/search/`
- **Method**: `GET`
- **Description**: Allows users to search for hotels based on various criteria.
- **Query Parameters**:
  - `destination` (string): The location where the user wants to search for hotels.
  - `checkin` (date): The check-in date for the booking (format: YYYY-MM-DD).
  - `checkout` (date): The check-out date for the booking (format: YYYY-MM-DD).
  - `amenities` (string): Comma-separated list of desired amenities (e.g., "wifi,pool").
  - `max_price` (float): The maximum price the user is willing to pay per night.
  - `min_price` (float): The minimum price the user is willing to pay per night.
  - `nb_star` (integer): The star rating of the hotels (e.g., 3, 4, 5).

### Check Available Rooms
- **URL**: `api/availableRooms/`
- **Method**: `GET`
- **Description**: Retrieves a list of rooms available for booking in a selected hotel based on the provided dates.
- **Query Parameters**:
  - `id_hotel` (integer): The unique ID of the hotel for which available rooms are being queried.
  - `checkin` (date): The check-in date for the booking (format: YYYY-MM-DD).
  - `checkout` (date): The check-out date for the booking (format: YYYY-MM-DD).

### Hotel Details
- **URL**: `api/hotel/`
- **Method**: `GET`
- **Description**: Fetches detailed information about a specific hotel, including its name, location, amenities, and pricing.
- **Query Parameters**:
  - `id_hotel` (integer): The unique ID of the hotel for which detailed information is being fetched.


## Hotel Booking Endpoints    
 
### Create a Booking
- **URL**: `api/book/`
- **Method**: `POST`
- **Description**: Creates a new hotel booking.

### Get User Bookings
- **URL**: `api/getbookings/`
- **Method**: `GET`
- **Description**: Retrieves all bookings for the authenticated user.

### Update Booking
- **URL**: `api/updatebooking/`
- **Method**: `POST`
- **Description**: Updates an existing booking.

### Cancel Booking
- **URL**: `api/cancelbooking/`
- **Method**: `POST`
- **Description**: Cancels an existing booking.


  


