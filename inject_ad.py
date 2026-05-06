import os
import glob

# The HTML snippet for the ad
ad_html = """
    <!-- Quản cáo -->
    <div class="ad-banner" style="text-align: center; margin: 20px 0;">
        <a href="https://senvoi.vn/tu-chau/tu-chau-lavabo-pvc/bo-tu-lavabo-guong-den-led-ztlv8963.html?utm_source=Admicro_AdX&utm_campaign=AdX&utm_content=tuoitre.vn&cpa_tid=01KQY14PS0CDYQK8DG9ZYB25JC&_tp=11&tpn=4&dmn=tuoitre.vn" target="_blank" rel="noopener noreferrer">
            <img src="https://adi.admicro.vn/adt/adn/2019/07/banner-mxSC8cKQUS.gif" alt="Advertisement" style="max-width: 100%; height: auto;">
        </a>
    </div>
"""

# Find all HTML files
html_files = glob.glob('*.html')

for filename in html_files:
    # Skip the canvas game folder files if any, but since we are running in root, glob gives mostly root files
    if not os.path.isfile(filename):
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Inject right after </header> if present
    if '</header>' in content and 'class="ad-banner"' not in content:
        new_content = content.replace('</header>', '</header>' + ad_html, 1)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Injected ad into {filename}")
    else:
        # If no </header> is found or ad is already there, check next
        print(f"Skipped {filename} (no </header> found or ad already exists)")

