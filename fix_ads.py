import os
import glob
import re

ad_html = """
    <!-- Quản cáo -->
    <div class="ad-banner" style="text-align: center; margin: 20px 0;">
        <a href="https://senvoi.vn/tu-chau/tu-chau-lavabo-pvc/bo-tu-lavabo-guong-den-led-ztlv8963.html?utm_source=Admicro_AdX&utm_campaign=AdX&utm_content=tuoitre.vn&cpa_tid=01KQY14PS0CDYQK8DG9ZYB25JC&_tp=11&tpn=4&dmn=tuoitre.vn" target="_blank" rel="noopener noreferrer">
            <img src="https://adi.admicro.vn/adt/adn/2019/07/banner-mxSC8cKQUS.gif" alt="Advertisement" style="max-width: 100%; height: auto;">
        </a>
    </div>
"""

# HTML files
html_files = glob.glob('*.html')

for filename in html_files:
    if not os.path.isfile(filename):
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove the ad injected mistakenly after </header>
    # Note: the injected string is exact, so we can replace it back with </header>
    if ad_html in content:
        content = content.replace('</header>' + ad_html, '</header>')
    
    # 2. Replace the horizontal banner ad (SPONSORED CONTENT)
    # <div class="banner-ad"> ... </div>
    # We will use regex to find <div class="banner-ad"> block
    banner_pattern = re.compile(r'<div class="banner-ad">\s*<span class="ad-label">SPONSORED CONTENT</span>.*?</div>', re.DOTALL)
    content = banner_pattern.sub(ad_html.strip(), content)
    
    # 3. Replace sidebar square ad
    # <div class="sidebar-ad"> ... </div>
    sidebar_pattern = re.compile(r'<div class="sidebar-ad">\s*<span class="ad-label">ADVERTISEMENT</span>.*?<p class="ad-text">.*?</p>\s*</div>', re.DOTALL)
    content = sidebar_pattern.sub(ad_html.strip(), content)

    # Note: we are not touching "side-ad" (the sticky ones on left and right) unless asked, 
    # but the prompt specifically mentioned the "SPONSORED CONTENT Luxury Seafood Restaurant"
    # and "ADVERTISEMENT Square Ad Support Sustainable Fishing Practices Worldwide."
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {filename}")
