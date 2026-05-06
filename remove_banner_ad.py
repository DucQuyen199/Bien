import re
import os
import glob

# The block to remove:
ad_block_regex = re.compile(
    r'(</section>\s*)+[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z\s*<!-- Horizontal Banner Ad -->\s*<!-- Quản cáo -->.*?</div>\s*</div>\s*(<div class="magazine-grid">)',
    re.DOTALL
)

html_files = glob.glob('*.html')
for filename in html_files:
    if not os.path.isfile(filename): continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We also check for just the banner without the timestamp just in case
    banner_pattern = re.compile(
        r'<!-- Horizontal Banner Ad -->\s*<!-- Quản cáo -->.*?</div>\s*</div>',
        re.DOTALL
    )
    
    if ad_block_regex.search(content):
        # Remove the weird timestamp and ad, keep magazine-grid
        new_content = ad_block_regex.sub(r'</section>\n\n            \2', content)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed ad block with timestamp in {filename}")
    elif banner_pattern.search(content):
        new_content = banner_pattern.sub(r'<!-- Horizontal Banner Ad Space Removed -->', content)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed banner ad in {filename}")

