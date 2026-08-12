import os
import glob
import re

html_files = glob.glob("d:/creashiiftads/public/**/*.html", recursive=True)

old_timer_pattern = re.compile(
    r'// Lead Popup Timer.*?setTimeout\(\(\) => \{\s*const isSubmitted = localStorage\.getItem\(\'creashift_lead_submitted\'\);.*?\n\s*\}, 5000\);',
    re.DOTALL
)

# Generic pattern matching leadPopup setTimeout blocks across all variations
generic_timer_pattern = re.compile(
    r'setTimeout\(\(\) => \{\s*const popup = document\.getElementById\(\'leadPopup\'\);.*?\n\s*\}, 5000\);',
    re.DOTALL
)

new_timer_code = """// Lead Popup Timer (5 Seconds) - Shows ONCE on whichever landing page the user enters first
            const popup = document.getElementById('leadPopup');
            if (popup) {
                setTimeout(() => {
                    const isSubmitted = localStorage.getItem('creashift_lead_submitted');
                    const alreadyShown = sessionStorage.getItem('creashift_popup_shown');
                    if (!isSubmitted && !alreadyShown) {
                        sessionStorage.setItem('creashift_popup_shown', 'true');
                        popup.classList.add('active');
                    }
                }, 5000);
            }"""

modified_count = 0
for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated = content
    if generic_timer_pattern.search(updated):
        updated = generic_timer_pattern.sub(new_timer_code, updated)
    elif 'leadPopup' in updated and '5000' in updated:
        # Fallback regex for non-standard whitespace
        updated = re.sub(
            r'setTimeout\(\(\) => \{[^}]*leadPopup[^}]*\}, 5000\);',
            new_timer_code,
            updated,
            flags=re.DOTALL
        )
    
    # Replace any leftover creashift_lead_closed with creashift_popup_shown
    updated = updated.replace("sessionStorage.setItem('creashift_lead_closed', 'true');", "sessionStorage.setItem('creashift_popup_shown', 'true');")
    
    if updated != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(updated)
        modified_count += 1
        print(f"Updated session landing logic in: {fpath}")

print(f"Total HTML files updated: {modified_count}")
