#!/usr/bin/env python3
import os
import re

# Read the updated form submission JavaScript from index.html
with open('clickodigital.com/index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Extract the form submission script for brxe-ascmxj (homepage popup form)
popup_form_pattern = r'const formId = document\.getElementById\("brxe-ascmxj"\);.*?}\);[\s]*}[\s]*\);'
popup_form_match = re.search(popup_form_pattern, index_content, re.DOTALL)

if not popup_form_match:
    print("Could not find popup form script in index.html")
    exit(1)

popup_form_script = popup_form_match.group(0)

# Find all HTML files
html_files = []
for root, dirs, files in os.walk('clickodigital.com'):
    for file in files:
        if file.endswith('.html') and not file.endswith('.backup'):
            html_files.append(os.path.join(root, file))

print(f"Found {len(html_files)} HTML files to update")

updated_count = 0

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if this is index.html (already updated)
        if html_file == 'clickodigital.com/index.html':
            continue
        
        # Check if file has the popup form (brxe-ascmxj)
        if 'id="brxe-ascmxj"' in content:
            # Replace the old form script with the new one
            old_pattern = r'const formId = document\.getElementById\("brxe-ascmxj"\);.*?}\);[\s]*}[\s]*\);'
            
            if re.search(old_pattern, content, re.DOTALL):
                new_content = re.sub(old_pattern, popup_form_script, content, flags=re.DOTALL)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✓ Updated popup form in: {html_file}")
                updated_count += 1
        
        # Check if file has contact page form (brxe-phpbme)
        if 'id="brxe-phpbme"' in content:
            # Replace brxe-ascmxj with brxe-phpbme in the script for contact page
            contact_form_script = popup_form_script.replace('brxe-ascmxj', 'brxe-phpbme')
            contact_form_script = contact_form_script.replace('Homepage Popup', 'Contact Page')
            
            old_pattern = r'const cFormId = document\.getElementById\("brxe-phpbme"\);.*?}\);[\s]*}[\s]*\);'
            
            if re.search(old_pattern, content, re.DOTALL):
                new_content = re.sub(old_pattern, contact_form_script.replace('const formId', 'const cFormId').replace('formId', 'cFormId'), content, flags=re.DOTALL)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✓ Updated contact form in: {html_file}")
                updated_count += 1
                
    except Exception as e:
        print(f"✗ Error updating {html_file}: {str(e)}")

print(f"\n✓ Successfully updated {updated_count} files")

