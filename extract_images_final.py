#!/usr/bin/env python3
"""
Extract images from MHTML file - Final version
Handles images without Content-ID, uses Content-Location for naming
"""

import os
import re
import base64
import hashlib
from pathlib import Path

def extract_images_from_mhtml(mhtml_path):
    """Extract all images from MHTML file"""
    mhtml_path = Path(mhtml_path)
    images_dir = mhtml_path.parent / 'converted' / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)
    
    with open(mhtml_path, 'rb') as f:
        content = f.read().decode('utf-8', errors='ignore')
    
    # Find all image blocks - images don't have Content-ID, only Content-Location
    # Pattern: Content-Type: image/X\nContent-Transfer-Encoding: base64\nContent-Location: URL\n\nDATA
    image_pattern = r'Content-Type:\s*image/([a-z+]+)\s*\nContent-Transfer-Encoding:\s*(\w+)\s*\nContent-Location:\s*([^\n]+)\s*\n\n([A-Za-z0-9+/=\n\r]+?)(?=\n\n------|\n------MultipartBoundary|$)'
    
    images_info = []
    image_count = 0
    
    for match in re.finditer(image_pattern, content, re.DOTALL):
        content_type = match.group(1)
        encoding = match.group(2)
        location = match.group(3)
        image_data = match.group(4)
        
        # Determine extension
        if content_type == 'avif':
            ext = 'avif'
        elif content_type == 'jpeg' or content_type == 'jpg':
            ext = 'jpg'
        elif content_type == 'png':
            ext = 'png'
        elif content_type == 'gif':
            ext = 'gif'
        elif content_type == 'webp':
            ext = 'webp'
        elif content_type == 'svg+xml':
            ext = 'svg'
        else:
            ext = content_type if content_type else 'bin'
        
        # Extract original filename from location if possible
        original_name = location.split('/')[-1].split('?')[0] if location else f'image_{image_count}'
        if '.' in original_name:
            name_parts = original_name.rsplit('.', 1)
            if len(name_parts[0]) > 3:
                ext = name_parts[1] if len(name_parts) > 1 else ext
        
        # Clean up the base64 data
        b64_clean = re.sub(r'\s+', '', image_data.strip())
        
        # Generate unique filename
        img_hash = hashlib.md5(location.encode() if location else str(image_count).encode()).hexdigest()[:8]
        filename = f"img_{image_count:03d}_{img_hash}.{ext}"
        filepath = images_dir / filename
        
        # Decode and save
        try:
            decoded = base64.b64decode(b64_clean)
            
            with open(filepath, 'wb') as f:
                f.write(decoded)
                
            images_info.append({
                'location': location,
                'filename': filename,
                'filepath': str(filepath),
                'ext': ext,
                'size': len(decoded),
                'type': f'image/{content_type}'
            })
            
            image_count += 1
            
        except Exception as e:
            print(f"Error extracting image from {location}: {e}")
    
    print(f"\nExtracted {len(images_info)} images")
    
    # Save mapping
    mapping_file = images_dir / 'image_mapping.txt'
    with open(mapping_file, 'w', encoding='utf-8') as f:
        f.write("# Image Mapping (Location -> filename)\n")
        for info in images_info:
            f.write(f"{info['location']}|{info['filename']}|{info['ext']}|{info['size']} bytes\n")
    
    return images_info


def extract_svg_images(mhtml_path):
    """Extract SVG images that might be inline"""
    mhtml_path = Path(mhtml_path)
    images_dir = mhtml_path.parent / 'converted' / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)
    
    with open(mhtml_path, 'rb') as f:
        content = f.read().decode('utf-8', errors='ignore')
    
    # Find SVG image blocks
    svg_pattern = r'Content-Type:\s*image/svg\+xml\s*\n(?:Content-Transfer-Encoding:\s*(\w+)\s*\n)?(?:Content-ID:\s*<([^>]+)>\s*\n)?(?:Content-Location:\s*([^\n]+)\s*\n)?\n(<svg[\s\S]*?</svg>)(?=\n\n------|\n------MultipartBoundary|$)'
    
    svg_count = 0
    for match in re.finditer(svg_pattern, content, re.DOTALL):
        encoding = match.group(1)
        content_id = match.group(2)
        location = match.group(3)
        svg_data = match.group(4)
        
        filename = f"svg_{svg_count:03d}.svg"
        filepath = images_dir / filename
        
        try:
            # Decode if needed
            if encoding == 'quoted-printable':
                svg_data = re.sub(r'=([0-9A-Fa-f]{2})', 
                                 lambda m: bytes.fromhex(m.group(1)).decode('utf-8', errors='ignore'), 
                                 svg_data)
                svg_data = re.sub(r'=\r?\n', '', svg_data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(svg_data)
            print(f"Extracted SVG: {filename}")
            svg_count += 1
        except Exception as e:
            print(f"Error extracting SVG: {e}")
    
    return svg_count


def update_html_with_local_images(html_path, images_info):
    """Update HTML to use local images instead of external URLs"""
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Create mapping from URLs to local files
    url_to_local = {}
    for info in images_info:
        if info['location']:
            url_to_local[info['location']] = f"images/{info['filename']}"
    
    # Replace URLs in HTML
    for url, local_path in url_to_local.items():
        # Escape for regex
        url_escaped = re.escape(url)
        html = re.sub(url_escaped, local_path, html)
    
    # Save updated HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Updated HTML with {len(url_to_local)} local image references")
    return len(url_to_local)


if __name__ == '__main__':
    import sys
    
    mhtml_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not mhtml_file:
        for f in Path('.').glob('*.mhtml'):
            mhtml_file = str(f)
            break
    
    if not mhtml_file:
        print("Error: No MHTML file specified")
        sys.exit(1)
    
    print("=" * 60)
    print("Extracting Images from MHTML")
    print("=" * 60)
    
    images_info = extract_images_from_mhtml(mhtml_file)
    svg_count = extract_svg_images(mhtml_file)
    
    # Update HTML with local images
    html_path = Path(mhtml_file).parent / 'converted' / 'index.html'
    if html_path.exists():
        updated = update_html_with_local_images(html_path, images_info)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Image Summary:")
    print("=" * 60)
    total_size = sum(img['size'] for img in images_info)
    print(f"Total embedded images: {len(images_info)}")
    print(f"SVG images: {svg_count}")
    print(f"Total size: {total_size / 1024:.2f} KB")
    
    if images_info:
        types = {}
        for img in images_info:
            ext = img['ext']
            types[ext] = types.get(ext, 0) + 1
        print("\nBy type:")
        for ext, count in sorted(types.items()):
            print(f"  .{ext}: {count}")
