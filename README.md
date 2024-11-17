# Hotel Room Booking System (Backend-Only)
The Hotel Room Booking System Backend is designed to handle all the server-side operations required for booking hotel rooms. It provides APIs to manage room availability, process bookings, and store user data. The backend serves as the backbone of the system, ensuring secure and efficient data handling for a smooth user experience.

# API Endpoints
All endpoints are prefixed with api/ to standardize access.

Register

URL: api/register/
Method: POST
Description: Allows new users to register by providing necessary details like email, password, and personal information.
Login

URL: api/login/
Method: POST
Description: Authenticates users and provides a token for secure access to protected resources.
List Users

URL: api/list/
Method: GET
Description: Retrieves a list of all users. Access restricted to admin roles.
Logout

URL: api/logout/
Method: POST
Description: Logs out the user by invalidating their authentication token.
Verify Code

URL: api/verify/
Method: POST
Description: Verifies a user-provided code, typically used for email or phone verification during registration or login.
Forget Password

URL: api/forgetpassword/
Method: POST
Description: Initiates the password recovery process by sending a reset link or verification code to the user's email or phone.
Change Password

URL: api/change_password/
Method: POST
Description: Allows users to change their password after providing the current password and the new password.
User Profile

URL: api/users/
Method: GET
Description: Fetches details about the authenticated user.
Activate Account

URL: api/activate/
Method: POST
Description: Activates a user account using a code sent to their email or phone, completing the registration process.
