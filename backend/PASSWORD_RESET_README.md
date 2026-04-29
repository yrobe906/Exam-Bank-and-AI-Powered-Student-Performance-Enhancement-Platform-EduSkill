# Password Reset Feature Implementation

This document describes the complete forgot password & reset password feature added to the EduSkill Hub backend.

## Backend Implementation

### Database Changes

A new table `password_reset_tokens` has been created with the following structure:
- `id` (Integer, Primary Key)
- `user_id` (Integer, Foreign Key to users.id)
- `token_hash` (String, Hashed reset token)
- `expires_at` (DateTime, UTC)
- `used` (Boolean, default False)
- `created_at` (DateTime, default UTC now)

### New API Endpoints

#### POST /api/auth/forgot-password
- **Request Body**: `{"email": "user@example.com"}`
- **Response**: Always `{"message": "If an account with this email exists, a password reset link has been sent."}`
- **Functionality**:
  - Generates secure random token (32 bytes URL-safe)
  - Hashes token using bcrypt
  - Invalidates previous tokens for the user
  - Sets expiry to 1 hour from creation (UTC)
  - Sends reset email via Gmail SMTP
  - Email contains link: `{FRONTEND_URL}/reset-password?token=RAW_TOKEN`

#### POST /api/auth/reset-password
- **Request Body**: `{"token": "raw_token_here", "new_password": "new_password_here"}`
- **Response**: `{"message": "Password has been reset successfully"}`
- **Functionality**:
  - Verifies token exists and is not used/expired
  - Hashes new password using existing `hash_password` function
  - Updates user password_hash
  - Marks token as used

### Environment Variables Required

Add these to your `.env` file:
```
GMAIL_USER=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_app_password
FRONTEND_URL=http://localhost:3000
SECRET_KEY=your_secret_key
```

### Files Created/Modified

#### New Files:
- `app/models/password_reset_models.py` - PasswordResetToken model
- `app/routers/password_reset_router.py` - Password reset endpoints
- `create_password_reset_table.py` - Migration script
- `frontend/ForgotPassword.vue` - Forgot password component
- `frontend/ResetPassword.vue` - Reset password component
- `frontend/Login.vue` - Sample login component with forgot password link

#### Modified Files:
- `app/models/user_models.py` - Added password_reset_tokens relationship
- `app/models/__init__.py` - Added PasswordResetToken import
- `main.py` - Added password_reset_router import and include

## Frontend Implementation (Vue.js)

### Components

#### ForgotPassword.vue
- Email input form
- Always shows success message (prevents email enumeration)
- Calls `/api/auth/forgot-password`

#### ResetPassword.vue
- Reads token from URL query parameter
- New password + confirm password validation
- Calls `/api/auth/reset-password`
- Redirects to login on success

#### Login.vue (Sample)
- Basic login form
- "Forgot Password?" link to `/forgot-password`

### Routes to Add

```javascript
{
  path: '/forgot-password',
  name: 'ForgotPassword',
  component: ForgotPassword
},
{
  path: '/reset-password',
  name: 'ResetPassword',
  component: ResetPassword
}
```

## Security Features

1. **Token Security**:
   - Tokens are 32 bytes URL-safe random strings
   - Stored as bcrypt hashes (not plain text)
   - Previous tokens invalidated on new request

2. **Email Enumeration Prevention**:
   - Always returns success message for forgot password
   - No indication if email exists or not

3. **Token Expiration**:
   - Tokens expire after 1 hour
   - Checked against UTC time

4. **Single Use**:
   - Tokens can only be used once
   - Marked as used after successful reset

5. **Password Hashing**:
   - Uses existing `hash_password` function (supports bcrypt and PBKDF2)

## Setup Instructions

1. **Run Migration**:
   ```bash
   python create_password_reset_table.py
   ```

2. **Set Environment Variables**:
   Add to `.env`:
   ```
   GMAIL_USER=your_gmail@gmail.com
   GMAIL_APP_PASSWORD=your_app_password
   FRONTEND_URL=http://localhost:3000
   ```

3. **Start Backend**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Test Endpoints**:
   - Visit `http://localhost:8000/docs` for API documentation
   - Test forgot password and reset password endpoints

## Email Template

The reset email contains:
- Subject: "Password Reset Request - EduSkill Hub"
- Body with reset link: `{FRONTEND_URL}/reset-password?token={RAW_TOKEN}`
- Expiration notice (1 hour)
- Security warning for unrecognized requests

## Error Handling

- Invalid/expired tokens: 400 Bad Request
- User not found: 400 Bad Request (generic)
- Network/email errors: Logged but not exposed to user
- All endpoints return appropriate HTTP status codes

## Production Considerations

1. **Email Service**: Consider using services like SendGrid for production
2. **Rate Limiting**: Add rate limiting to prevent abuse
3. **Token Length**: 32 bytes provides ~128 bits of entropy
4. **HTTPS**: Ensure all communications are over HTTPS
5. **Logging**: Sensitive operations are logged for security monitoring

## Testing

Test scenarios:
1. Forgot password with valid email
2. Forgot password with invalid email (should still show success)
3. Reset with valid token and matching passwords
4. Reset with expired token
5. Reset with already used token
6. Reset with non-matching passwords (frontend validation)
7. Reset with invalid token

The implementation is production-ready and follows security best practices.