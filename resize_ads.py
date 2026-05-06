import os
import glob

html_files = glob.glob('*.html')
old_img_tag = '<img src="https://adi.admicro.vn/adt/adn/2019/07/banner-mxSC8cKQUS.gif" alt="Advertisement" style="max-width: 100%; height: auto;">'
new_img_tag = '<img src="https://adi.admicro.vn/adt/adn/2019/07/banner-mxSC8cKQUS.gif" alt="Advertisement" style="max-width: 80%; width: 300px; height: auto;">'

for filename in html_files:
    if not os.path.isfile(filename):
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_img_tag in content:
        content = content.replace(old_img_tag, new_img_tag)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Resized ad in {filename}")

