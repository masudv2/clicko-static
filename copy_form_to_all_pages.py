#!/usr/bin/env python3
import os
import glob

# The new form submission script
NEW_FORM_SCRIPT = '''// Form Email Start
	// Popup Email ----------
	const formId = document.getElementById("brxe-ascmxj");
	if (formId) {
		formId.addEventListener("submit", async (e) => {
			e.preventDefault();
			
				const formData = new FormData(formId);
				const name = formData.get('form-field-1314f5');
				const email = formData.get('form-field-ee3ce5');
				const phone = formData.get('form-field-rpauey') || 'Not provided';
				const message = formData.get('form-field-54f2cc');
				const scheduleCall = formData.get('form-field-vgrpjm[]') || 'Not selected';
				
				// Handle file uploads - convert to base64
				const files = formData.getAll('form-field-dpdxuc');
				let fileAttachments = [];
				
				if (files && files.length > 0 && files[0].size > 0) {
					// Convert files to base64 for email attachment
					for (const file of files) {
						const base64 = await new Promise((resolve) => {
							const reader = new FileReader();
							reader.onloadend = () => resolve(reader.result.split(',')[1]);
							reader.readAsDataURL(file);
						});
						
						fileAttachments.push({
							filename: file.name,
							content: base64,
							type: file.type || 'application/octet-stream'
						});
					}
				}
			
			// Show loading state
			const submitBtn = formId.querySelector('button[type="submit"]');
			const originalText = submitBtn ? submitBtn.textContent : '';
			if (submitBtn) {
				submitBtn.textContent = 'Sending...';
				submitBtn.disabled = true;
			}
			
			try {
				// Send to Cloudflare Function
				const response = await fetch('/api/send-email', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
						body: JSON.stringify({
							name,
							email,
							phone,
							message,
							scheduleCall,
							attachments: fileAttachments,
							formType: 'Homepage Popup'
						})
				});
				
				const result = await response.json();
				
				if (result.success) {
					// Show thank you message in popup
					const thankYouMessage = document.getElementById('thank-you-message');
					const meetingScheduler = document.getElementById('meeting-scheduler');
					const formFields = formId.querySelectorAll('.form-group');
					
					// Hide form fields and show thank you message
					formFields.forEach(field => field.style.display = 'none');
					thankYouMessage.style.display = 'block';
					
					// Check if user wants to schedule a call
					if (scheduleCall === 'Yes') {
						// Show meeting scheduler after a short delay
						setTimeout(() => {
							meetingScheduler.style.display = 'block';
							// Scroll to scheduler
							meetingScheduler.scrollIntoView({ behavior: 'smooth', block: 'start' });
							
							// Pre-populate Salesmate form after iframe loads
							setTimeout(() => {
								try {
									const iframe = meetingScheduler.querySelector('iframe');
									if (iframe) {
										iframe.onload = function() {
											try {
												const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
												if (iframeDoc) {
													// Pre-populate form fields
													const nameField = iframeDoc.getElementById('Contact_name');
													const emailField = iframeDoc.getElementById('Contact_email');
													const mobileField = iframeDoc.getElementById('Contact_mobile');
													const descriptionField = iframeDoc.getElementById('Contact_description');
													
													if (nameField) nameField.value = name;
													if (emailField) emailField.value = email;
													if (mobileField) mobileField.value = phone;
													if (descriptionField) descriptionField.value = message;
												}
											} catch (e) {
												console.log('Cannot access iframe content due to CORS policy');
											}
										};
									}
								} catch (e) {
									console.log('Error accessing iframe:', e);
								}
							}, 2000);
						}, 1500);
					}
					
					// Scroll to top of popup
					const popupContent = document.querySelector('.brx-popup-content');
					if (popupContent) {
						popupContent.scrollTop = 0;
					}
					
					// Auto-close popup after 3 seconds (only if no scheduler)
					if (scheduleCall !== 'Yes') {
						setTimeout(() => {
							const popup = document.querySelector('.brx-popup');
							if (popup) {
								popup.classList.add('hide');
							}
							// Reset form and show fields again
							formId.reset();
							formFields.forEach(field => field.style.display = 'block');
							thankYouMessage.style.display = 'none';
							meetingScheduler.style.display = 'none';
						}, 3000);
					}
				} else {
					throw new Error(result.error || 'Failed to send message');
				}
			} catch (error) {
				console.error('Form submission error:', error);
				
				// Show error message in popup
				const thankYouMessage = document.getElementById('thank-you-message');
				const formFields = formId.querySelectorAll('.form-group');
				
				// Update thank you message to show error
				thankYouMessage.innerHTML = `
					<div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 8px;">
						<svg style="width: 24px; height: 24px; animation: bounce 0.6s ease-in-out;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
							<circle cx="12" cy="12" r="10" fill="#dc3545"/>
							<path d="M12 8V12M12 16H12.01" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
						<h3 style="color: #dc3545; margin: 0; font-size: 20px; font-weight: 600;">Error</h3>
					</div>
					<p style="color: #666; margin: 0; font-size: 14px; line-height: 1.4;">Sorry, there was an error sending your message. Please try again or contact us directly at hello@clickodigital.com</p>
				`;
				
				// Hide form fields and show error message
				formFields.forEach(field => field.style.display = 'none');
				thankYouMessage.style.display = 'block';
				
				// Scroll to top of popup
				const popupContent = document.querySelector('.brx-popup-content');
				if (popupContent) {
					popupContent.scrollTop = 0;
				}
				
				// Auto-close popup after 5 seconds
				setTimeout(() => {
					const popup = document.querySelector('.brx-popup');
					if (popup) {
						popup.classList.add('hide');
					}
					// Reset form and show fields again
					formId.reset();
					formFields.forEach(field => field.style.display = 'block');
					thankYouMessage.style.display = 'none';
					// Reset thank you message content
					thankYouMessage.innerHTML = `
						<div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 8px;">
							<svg style="width: 24px; height: 24px; animation: bounce 0.6s ease-in-out;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<circle cx="12" cy="12" r="10" fill="#28a745"/>
								<path d="M8 12L11 15L16 9" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
							<h3 style="color: #28a745; margin: 0; font-size: 20px; font-weight: 600;">Thank You!</h3>
						</div>
						<p style="color: #666; margin: 0; font-size: 14px; line-height: 1.4;">Your message has been sent successfully. We'll get back to you soon!</p>
					`;
					// Hide meeting scheduler
					const meetingScheduler = document.getElementById('meeting-scheduler');
					if (meetingScheduler) {
						meetingScheduler.style.display = 'none';
					}
				}, 5000);
			} finally {
				// Reset button state
				if (submitBtn) {
					submitBtn.textContent = originalText;
					submitBtn.disabled = false;
				}
			}
		});
	}'''

# Find all HTML files
html_files = glob.glob('clickodigital.com/**/*.html', recursive=True)
html_files = [f for f in html_files if not f.endswith('.backup')]

print(f"Found {len(html_files)} HTML files")

updated_count = 0
skipped_count = 0

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has the popup form
        if 'id="brxe-ascmxj"' in content and '// Form Email Start' in content:
            # Find the start and end of the form script
            start_marker = '// Form Email Start'
            
            # Find where this script ends (looking for the closing of the addEventListener)
            start_idx = content.find(start_marker)
            if start_idx == -1:
                skipped_count += 1
                continue
            
            # Find the end - look for the closing of the if statement after all the code
            # We'll look for the pattern that closes the formId addEventListener
            end_pattern = '\t}\n// Form Email End'
            end_idx = content.find(end_pattern, start_idx)
            
            if end_idx == -1:
                # Try alternative end pattern
                end_idx = content.find('\t}\n\t// Contact Page Email', start_idx)
                if end_idx == -1:
                    print(f"Could not find end pattern in: {html_file}")
                    skipped_count += 1
                    continue
            
            # Replace the old script with new one
            new_content = content[:start_idx] + NEW_FORM_SCRIPT + content[end_idx:]
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✓ Updated: {html_file}")
            updated_count += 1
        else:
            skipped_count += 1
            
    except Exception as e:
        print(f"✗ Error updating {html_file}: {str(e)}")
        skipped_count += 1

print(f"\n✓ Successfully updated {updated_count} files")
print(f"⊘ Skipped {skipped_count} files")

