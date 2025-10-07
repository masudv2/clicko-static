#!/usr/bin/env python3
"""
Script to update Resend API keys in the contact forms.
Run this after setting up your Resend.io account.
"""

import os
import sys

def update_resend_api_key(api_key):
    """Update Resend API key in both contact forms"""
    
    if not api_key:
        print("Error: Please provide a Resend API key")
        print("Usage: python3 update_resend_api_key.py YOUR_API_KEY")
        sys.exit(1)
    
    # Validate API key format (should start with 're_' and be alphanumeric)
    if not api_key.startswith('re_') or len(api_key) < 20:
        print("Error: Invalid API key format. Resend API keys should start with 're_'")
        sys.exit(1)
    
    files_to_update = [
        "clickodigital.com/index.html",
        "clickodigital.com/contact-us/index.html"
    ]
    
    updated_count = 0
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace the placeholder
                new_content = content.replace('YOUR_RESEND_API_KEY', api_key)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ Updated: {file_path}")
                    updated_count += 1
                else:
                    print(f"⚠️  No changes needed: {file_path}")
                    
            except Exception as e:
                print(f"❌ Error updating {file_path}: {e}")
        else:
            print(f"❌ File not found: {file_path}")
    
    if updated_count > 0:
        print(f"\n🎉 Successfully updated {updated_count} files!")
        print("Your contact forms are now ready for deployment.")
        print("\n📧 Make sure to verify your domain in Resend.io dashboard!")
    else:
        print("\n⚠️  No files were updated.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 update_resend_api_key.py YOUR_API_KEY")
        print("\nExample: python3 update_resend_api_key.py re_1234567890abcdef")
        print("\nGet your API key from: https://resend.com/api-keys")
        sys.exit(1)
    
    api_key = sys.argv[1]
    update_resend_api_key(api_key)
