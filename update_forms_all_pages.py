#!/usr/bin/env python3
import os
import re
import glob

# Read the source file (index.html with updated form)
with open('/Users/masud/Sites/personal/clicko-static/clickodigital.com/index.html', 'r', encoding='utf-8') as f:
    source_content = f.read()

# Extract the complete popup form script
# Find from "// Popup Email ----------" to just before "// Contact Email ----------"
popup_start = source_content.find('// Popup Email ----------')
popup_end = source_content.find('\n\t// Contact Email ----------', popup_start)

if popup_start == -1 or popup_end == -1:
    print("ERROR: Could not find popup form script markers")
    exit(1)

new_popup_script = source_content[popup_start:popup_end].strip()

print("✓ Extracted popup form script")
print(f"  Script length: {len(new_popup_script)} characters")

# Find all HTML files
html_files = []
for root, dirs, files in os.walk('/Users/masud/Sites/personal/clicko-static/clickodigital.com'):
    for file in files:
        if file.endswith('.html') and not file.endswith('.backup'):
            html_files.append(os.path.join(root, file))

print(f"\n✓ Found {len(html_files)} HTML files to process")

updated_count = 0
skipped_count = 0
error_count = 0

for html_file in html_files:
    try:
        # Skip index.html as it's already updated
        if html_file.endswith('/index.html') and 'clickodigital.com/index.html' in html_file:
            print(f"⊘ Skipped (source file): {html_file}")
            skipped_count += 1
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if this file has the popup form
        if 'id="brxe-ascmxj"' not in content:
            skipped_count += 1
            continue
        
        # Check if it has the old form script
        if '// Popup Email ----------' not in content:
            print(f"⚠ No popup script marker: {html_file}")
            skipped_count += 1
            continue
        
        # Find and replace the old popup script
        old_popup_start = content.find('// Popup Email ----------')
        if old_popup_start == -1:
            skipped_count += 1
            continue
        
        # Find where the old script ends (before Contact Email or before closing script tag)
        old_popup_end = content.find('\n\t// Contact Email ----------', old_popup_start)
        if old_popup_end == -1:
            # Try to find alternative end marker
            old_popup_end = content.find('\n// Form Email End', old_popup_start)
            if old_popup_end == -1:
                # Try to find the closing of the addEventListener function
                old_popup_end = content.find('\t}\n\n\t// Contact', old_popup_start)
                if old_popup_end == -1:
                    print(f"⚠ Could not find end marker: {html_file}")
                    error_count += 1
                    continue
        
        # Replace the old script with the new one
        new_content = content[:old_popup_start] + new_popup_script + content[old_popup_end:]
        
        # Write the updated content
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Updated: {os.path.relpath(html_file, '/Users/masud/Sites/personal/clicko-static/clickodigital.com')}")
        updated_count += 1
        
    except Exception as e:
        print(f"✗ Error updating {html_file}: {str(e)}")
        error_count += 1

print(f"\n" + "="*60)
print(f"📊 Summary:")
print(f"  ✓ Successfully updated: {updated_count} files")
print(f"  ⊘ Skipped: {skipped_count} files")
print(f"  ✗ Errors: {error_count} files")
print(f"="*60)

if updated_count > 0:
    print(f"\n🎉 Form functionality successfully copied to {updated_count} pages!")

