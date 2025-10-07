# Cloudflare Function Setup for Resend API

## Overview
This project includes a Cloudflare Function that acts as a proxy to send emails via the Resend API, avoiding CORS issues when calling the API directly from the browser.

## Function Details
- **Function Path**: `/api/send-email`
- **Method**: POST
- **Purpose**: Handle contact form submissions and send emails via Resend API

## Setup Instructions

### 1. Set Environment Variables in Cloudflare Dashboard

1. Go to your Cloudflare Pages project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add the following environment variable:
   - **Variable name**: `RESEND_API_KEY`
   - **Value**: `re_ciFGGhwD_EWw3w69J6XxPMCfkoW7BLWkC`
   - **Environment**: Production (and Preview if needed)

### 2. Alternative: Set via Wrangler CLI

```bash
# Set the environment variable
wrangler pages secret put RESEND_API_KEY --project-name=clicko-static

# When prompted, enter: re_ciFGGhwD_EWw3w69J6XxPMCfkoW7BLWkC
```

### 3. Verify Function is Working

After deployment, test the function by visiting:
```
https://your-domain.pages.dev/api/send-email
```

You should see a 405 Method Not Allowed error (this is expected for GET requests).

## Function Features

### Input Validation
- Validates required fields: name, email, message
- Validates email format using regex
- Returns appropriate error messages for invalid data

### Email Formatting
- Sends both HTML and plain text versions
- Includes form type identification (Homepage Popup, Contact Page)
- Adds timestamp and source information
- Professional email template with Clicko Digital branding

### Error Handling
- Comprehensive error handling for API failures
- Fallback to mailto links if function fails
- User-friendly error messages
- Console logging for debugging

### CORS Support
- Handles preflight OPTIONS requests
- Allows cross-origin requests from your domain
- Proper CORS headers for browser compatibility

## Form Integration

The contact forms now:
1. **Primary**: Send data to `/api/send-email` Cloudflare Function
2. **Fallback**: Use mailto links if the function fails
3. **Loading States**: Show "Sending..." during submission
4. **User Feedback**: Display success/error messages

## Testing

### Test the Function Directly
```bash
curl -X POST https://your-domain.pages.dev/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "message": "This is a test message",
    "phone": "1234567890",
    "scheduleCall": "Yes",
    "formType": "Test"
  }'
```

### Expected Response
```json
{
  "success": true,
  "message": "Email sent successfully",
  "emailId": "resend-email-id"
}
```

## Troubleshooting

### Common Issues

1. **Function not found (404)**
   - Ensure the function is deployed correctly
   - Check that the path is `/api/send-email`

2. **Environment variable not set**
   - Verify `RESEND_API_KEY` is set in Cloudflare dashboard
   - Check that the API key is correct

3. **CORS errors**
   - The function includes CORS headers
   - Ensure you're calling from the correct domain

4. **Email not received**
   - Check Resend API dashboard for delivery status
   - Verify the recipient email address
   - Check spam folder

### Debug Mode

To enable debug logging, you can modify the function to log more details:

```javascript
console.log('Request body:', body);
console.log('Resend response:', resendData);
```

## Security Notes

- The Resend API key is stored as an environment variable (secure)
- Input validation prevents malicious data
- CORS is properly configured
- No sensitive data is logged

## Deployment

The function is automatically deployed when you run:
```bash
wrangler pages deploy clickodigital.com --project-name=clicko-static
```

The function will be available at:
```
https://your-domain.pages.dev/api/send-email
```
