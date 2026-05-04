#!/usr/bin/env python3
"""
Extract images from MHTML file
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
    
    # Find boundary
    boundary_match = re.search(r'boundary="(.*?)"', content)
    if boundary_match:
        boundary = boundary_match.group(1)
    else:
        boundary = None
    
    print(f"Boundary: {boundary}")
    
    # Split content by boundary
    if boundary:
        parts = content.split(f'--{boundary}')
    else:
        parts = [content]
    
    images_info = []
    image_count = 0
    
    for part in parts:
        # Check if it's an image
        if 'Content-Type: image' not in part:
            continue
            
        # Get content ID
        cid_match = re.search(r'Content-ID:\s*<([^>]+)>', part)
        if not cid_match:
            continue
        content_id = cid_match.group(1)
        
        # Get encoding
        encoding_match = re.search(r'Content-Transfer-Encoding:\s*(\w+)', part)
        encoding = encoding_match.group(1) if encoding_match else 'base64'
        
        # Determine image type
        if 'image/avif' in part:
            ext = 'avif'
        elif 'image/jpeg' in part or 'image/jpg' in part:
            ext = 'jpg'
        elif 'image/png' in part:
            ext = 'png'
        elif 'image/gif' in part:
            ext = 'gif'
        elif 'image/webp' in part:
            ext = 'webp'
        elif 'image/svg' in part:
            ext = 'svg'
        else:
            ext = 'bin'
        
        # Find the actual image data (after headers)
        header_end = part.find('\n\n')
        if header_end == -1:
            header_end = part.find('\r\n\r\n')
        if header_end == -1:
            continue
            
        image_data = part[header_end + 2:]
        
        # Generate unique filename
        img_hash = hashlib.md5(content_id.encode()).hexdigest()[:16]
        filename = f"img_{image_count:03d}_{img_hash}.{ext}"
        filepath = images_dir / filename
        
        # Decode and save
        try:
            if encoding == 'base64':
                decoded = base64.b64decode(image_data.strip())
            elif encoding == 'quoted-printable':
                # Decode quoted-printable
                decoded = image_data
                decoded = re.sub(r'=([0-9A-Fa-f]{2})', 
                               lambda m: bytes.fromhex(m.group(1)).decode('utf-8', errors='ignore'), 
                               decoded)
                decoded = re.sub(r'=\r?\n', '', decoded)
                decoded = decoded.strip().encode('latin-1')
            else:
                decoded = image_data.strip().encode('latin-1')
                
            with open(filepath, 'wb') as f:
                f.write(decoded)
                
            images_info.append({
                'cid': content_id,
                'filename': filename,
                'filepath': str(filepath),
                'ext': ext,
                'size': len(decoded)
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


def extract_svg_and_inline_images(mhtml_path):
    """Extract inline SVG and other embedded images"""
    mhtml_path = Path(mhtml_path)
    images_dir = mhtml_path.parent / 'converted' / 'images'
    
    with open(mhtml_path, 'rb') as f:
        content = f.read().decode('utf-8', errors='ignore')
    
    # Split by boundary
    boundary_match = re.search(r'boundary="(.*?)"', content)
    if boundary_match:
        boundary = boundary_match.group(1)
        parts = content.split(f'--{boundary}')
    else:
        parts = [content]
    
    svg_count = 0
    for i, part in enumerate(parts):
        # Look for embedded SVGs
        if 'image/svg' in part:
            cid_match = re.search(r'Content-ID:\s*<([^>]+)>', part)
            if cid_match:
                content_id = cid_match.group(1)
                
                header_end = part.find('\n\n')
                if header_end == -1:
                    header_end = part.find('\r\n\r\n')
                if header_end == -1:
                    continue
                    
                svg_data = part[header_end + 2:]
                
                # Decode if needed
                svg_data = re.sub(r'=([0-9A-Fa-f]{2})', 
                                 lambda m: bytes.fromhex(m.group(1)).decode('utf-8', errors='ignore'), 
                                 svg_data)
                svg_data = re.sub(r'=\r?\n', '', svg_data)
                
                filename = f"svg_{svg_count:03d}.svg"
                filepath = images_dir / filename
                
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(svg_data.strip())
                    print(f"Extracted SVG: {filename} (CID: {content_id})")
                    svg_count += 1
                except Exception as e:
                    print(f"Error extracting SVG: {e}")
    
    print(f"Extracted {svg_count} SVG files")


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
    extract_svg_and_inline_images(mhtml_file)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Image Summary:")
    print("=" * 60)
    total_size = sum(img['size'] for img in images_info)
    print(f"Total images: {len(images_info)}")
    print(f"Total size: {total_size / 1024:.2f} KB")
    
    # Show image types
    types = {}
    for img in images_info:
        ext = img['ext']
        types[ext] = types.get(ext, 0) + 1
    print("\nBy type:")
    for ext, count in sorted(types.items()):
        print(f"  .{ext}: {count}")
