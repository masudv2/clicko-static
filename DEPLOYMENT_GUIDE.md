# Cloudflare Pages Deployment Guide

## Overview
This WordPress site has been converted to a static site and is ready for deployment to Cloudflare Pages.

## Changes Made

### 1. Contact Form Fixes
- ✅ Removed all Salesmate.io redirects from contact forms
- ✅ Updated contact form popup (homepage) to work with static hosting
- ✅ Updated contact form (contact page) to work with static hosting
- ✅ Added Resend.io integration for form submissions

### 2. Form Configuration
Both contact forms now use Resend.io for handling submissions:
- **Homepage popup form**: `brxe-ascmxj`
- **Contact page form**: `brxe-phpbme`

**Important**: You need to replace `YOUR_RESEND_API_KEY` in both forms with your actual Resend API key.

## Deployment Steps

### 1. Set up Resend.io (Required)
1. Go to [Resend.io](https://resend.com)
2. Create a free account
3. Verify your domain (clickodigital.com)
4. Get your API key from the dashboard
5. Replace `YOUR_RESEND_API_KEY` in both forms:
   - `index.html` (line ~2691)
   - `contact-us/index.html` (line ~1484)
   
   **Or use the helper script:**
   ```bash
   python3 update_resend_api_key.py YOUR_API_KEY
   ```

### 2. Deploy to Cloudflare Pages
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to Pages
3. Click "Create a project"
4. Choose "Upload assets"
5. Upload the entire `clickodigital.com` folder
6. Set build settings:
   - **Build command**: (leave empty)
   - **Build output directory**: `/` (root)
7. Deploy

### 3. Custom Domain (Optional)
1. In Cloudflare Pages, go to your project
2. Click "Custom domains"
3. Add your domain
4. Update DNS records as instructed

## File Structure
```
clickodigital.com/
├── index.html (homepage with popup form)
├── contact-us/
│   └── index.html (contact page with form)
├── wp-content/ (assets, images, etc.)
├── wp-includes/ (WordPress assets)
└── [other pages and directories]
```

## Form Fields
Both forms collect:
- Full Name (required)
- Email Address (required)
- Phone Number (optional)
- Project Description (required)
- File Upload (optional)
- Schedule a call? (Yes/No radio buttons)

## Testing
After deployment:
1. Test the homepage popup form
2. Test the contact page form
3. Verify form submissions are received via Resend.io
4. Check that popup closes after submission
5. Check your email for form submissions

## Email Configuration
The forms are configured to send emails to:
- **From**: noreply@clickodigital.com
- **To**: hello@clickodigital.com
- **Subject**: Different for each form (Homepage Popup vs Contact Page)

You can modify these in the JavaScript code if needed.

## Backup Files
All original files have been backed up with `.backup` extension. You can safely delete these after confirming the deployment works correctly.

## Notes
- The site is now fully static and doesn't require a server
- All WordPress functionality has been converted to static HTML/CSS/JS
- Forms use Resend.io API for reliable email delivery
- The Yes/No radio buttons no longer trigger Salesmate.io redirects
- Resend.io provides better deliverability and analytics compared to basic form services
