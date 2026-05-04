#!/usr/bin/env python3
"""
Extract images from MHTML file - Fixed version
Handles different boundary variations
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
    
    # Find the main boundary
    boundary_match = re.search(r'boundary="(----MultipartBoundary[^"]+)"', content)
    if boundary_match:
        main_boundary = boundary_match.group(1)
    else:
        boundary_match = re.search(r'boundary="([^"]+)"', content)
        main_boundary = boundary_match.group(1) if boundary_match else None
    
    print(f"Main boundary: {main_boundary[:50]}...")
    
    # Extract all images by finding Content-Type: image blocks
    # Pattern to match image blocks
    image_pattern = r'Content-Type:\s*image/[a-z]+\s*\nContent-Transfer-Encoding:\s*(\w+)\s*\n(?:Content-ID:\s*<([^>]+)>\s*\n)?(?:Content-Location:\s*[^\n]+\s*\n)?\n([A-Za-z0-9+/=\n]+?)(?=\n\n------|\n\n------|$)'
    
    images_info = []
    image_count = 0
    
    # Find all image blocks
    matches = list(re.finditer(r'Content-Type: (image/[a-z+]+)\s*\nContent-Transfer-Encoding: (\w+)\s*\n(?:Content-ID: <([^>]+)>\s*\n)?(?:Content-Location: [^\n]+\s*\n)?\n', content))
    
    for match in matches:
        content_type = match.group(1)
        encoding = match.group(2)
        content_id = match.group(3) if match.group(3) else f"unknown_{image_count}"
        
        # Find the actual image data
        start_pos = match.end()
        
        # Find end of image data (before next boundary or end of file)
        end_search = content.find('\n------', start_pos)
        if end_search == -1:
            end_search = len(content)
        
        # Get the image data
        image_data = content[start_pos:end_search].strip()
        
        # Remove any trailing newlines
        while image_data.endswith('\n') or image_data.endswith('\r'):
            image_data = image_data[:-1]
        
        # Determine extension
        if 'avif' in content_type:
            ext = 'avif'
        elif 'jpeg' in content_type or 'jpg' in content_type:
            ext = 'jpg'
        elif 'png' in content_type:
            ext = 'png'
        elif 'gif' in content_type:
            ext = 'gif'
        elif 'webp' in content_type:
            ext = 'webp'
        elif 'svg' in content_type:
            ext = 'svg'
        else:
            ext = 'bin'
        
        # Generate unique filename
        img_hash = hashlib.md5(content_id.encode()).hexdigest()[:12]
        filename = f"img_{image_count:03d}_{img_hash}.{ext}"
        filepath = images_dir / filename
        
        # Decode and save
        try:
            if encoding == 'base64':
                # Remove any whitespace from base64 data
                b64_clean = re.sub(r'\s+', '', image_data)
                decoded = base64.b64decode(b64_clean)
            elif encoding == 'quoted-printable':
                # Decode quoted-printable
                decoded = re.sub(r'=([0-9A-Fa-f]{2})', 
                               lambda m: bytes.fromhex(m.group(1)).decode('utf-8', errors='ignore'), 
                               image_data)
                decoded = re.sub(r'=\r?\n', '', decoded)
                decoded = decoded.encode('latin-1')
            else:
                decoded = image_data.encode('latin-1')
                
            with open(filepath, 'wb') as f:
                f.write(decoded)
                
            images_info.append({
                'cid': content_id,
                'filename': filename,
                'filepath': str(filepath),
                'ext': ext,
                'size': len(decoded),
                'type': content_type
            })
            
            image_count += 1
            
        except Exception as e:
            print(f"Error extracting {content_id}: {e}")
    
    print(f"\nExtracted {len(images_info)} images")
    
    # Save mapping
    mapping_file = images_dir / 'image_mapping.txt'
    with open(mapping_file, 'w') as f:
        f.write("# Image Mapping (CID -> filename)\n")
        for info in images_info:
            f.write(f"{info['cid']}|{info['filename']}|{info['ext']}|{info['size']} bytes\n")
    
    return images_info


def extract_wix_images(mhtml_path):
    """Extract images using Content-Location URLs"""
    mhtml_path = Path(mhtml_path)
    images_dir = mhtml_path.parent / 'converted' / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)
    
    with open(mhtml_path, 'rb') as f:
        content = f.read().decode('utf-8', errors='ignore')
    
    # Find all Content-Location URLs pointing to wixstatic
    url_pattern = r'(https://static\.wixstatic\.com/media/[^?]+\.(?:png|jpg|jpeg|avif|webp|svg|gif))'
    urls = re.findall(url_pattern, content)
    
    print(f"\nFound {len(urls)} Wix image URLs (these are external, not embedded)")
    return urls


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
    wix_urls = extract_wix_images(mhtml_file)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Image Summary:")
    print("=" * 60)
    total_size = sum(img['size'] for img in images_info)
    print(f"Total embedded images extracted: {len(images_info)}")
    print(f"Total embedded size: {total_size / 1024:.2f} KB")
    
    # Show image types
    if images_info:
        types = {}
        for img in images_info:
            ext = img['ext']
            types[ext] = types.get(ext, 0) + 1
        print("\nBy type:")
        for ext, count in sorted(types.items()):
            print(f"  .{ext}: {count}")
    
    print(f"\nExternal Wix images (URLs found): {len(wix_urls)}")
    if wix_urls:
        unique_urls = list(set(wix_urls))
        print(f"Unique URLs: {len(unique_urls)}")
