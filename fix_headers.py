import os
import re

files_to_fix = [
    'about.html',
    'culinary.html',
    'culture.html',
    'environment.html',
    'index.html',
    'opinion.html',
    'people.html',
    'travel.html'
]

menu_items = [
    ('index.html', 'HOME'),
    ('travel.html', 'TRAVEL'),
    ('culinary.html', 'CULINARY'),
    ('environment.html', 'ENVIRONMENT'),
    ('people.html', 'PEOPLE'),
    ('culture.html', 'CULTURE'),
    ('opinion.html', 'OPINION'),
    ('sea_seafood.html', 'FINAL'),
    ('about.html', 'ABOUT US')
]

for filename in files_to_fix:
    if not os.path.exists(filename):
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    nav_pattern = re.compile(r'(<nav id="main-nav">\s*<ul>).*?(</ul>)', re.DOTALL)
    
    new_ul = "\n"
    for href, text in menu_items:
        if filename == href:
            new_ul += f'                    <li><a href="{href}" class="active">{text}</a></li>\n'
        else:
            new_ul += f'                    <li><a href="{href}">{text}</a></li>\n'
    new_ul += '                '
    
    def repl(match):
        return match.group(1) + new_ul + match.group(2)
        
    new_content = nav_pattern.sub(repl, content)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed {filename}")
