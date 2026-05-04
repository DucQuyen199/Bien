#!/usr/bin/env python3
"""
MHTML to HTML/CSS Converter
Extracts content from MHTML files and creates standalone HTML with external CSS
"""

import os
import re
import base64
import hashlib
from email import policy
from email.parser import BytesParser
from pathlib import Path

class MHTMLConverter:
    def __init__(self, mhtml_path):
        self.mhtml_path = Path(mhtml_path)
        self.output_dir = self.mhtml_path.parent / 'converted'
        self.images_dir = self.output_dir / 'images'
        self.css_dir = self.output_dir / 'css'
        self.html_content = None
        self.css_content = []
        self.images = {}
        self.fonts = {}
        
    def create_directories(self):
        """Create output directories"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.css_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directories at {self.output_dir}")
        
    def parse_mhtml(self):
        """Parse MHTML file and extract all parts"""
        print(f"Parsing MHTML file: {self.mhtml_path}")
        
        with open(self.mhtml_path, 'rb') as f:
            content = f.read()
        
        # Decode quoted-printable encoding
        try:
            content = content.decode('utf-8')
        except:
            content = content.decode('latin-1')
        
        # Split by boundaries
        boundary_match = re.search(r'boundary="(.*?)"', content)
        if boundary_match:
            boundary = boundary_match.group(1)
        else:
            # Try alternative format
            boundary_match = re.search(r'boundary=(.+)', content)
            if boundary_match:
                boundary = boundary_match.group(1).strip('"')
            else:
                boundary = '----MultipartBoundary'
        
        # Handle different boundary formats
        boundary = boundary.replace('"', '')
        parts = content.split(f'--{boundary}')
        
        print(f"Found {len(parts)} parts in MHTML")
        
        for i, part in enumerate(parts):
            self._process_part(part, i)
        
    def _process_part(self, part, index):
        """Process a single MHTML part"""
        # Extract Content-Type
        content_type_match = re.search(r'Content-Type:\s*([^\n]+)', part)
        if not content_type_match:
            return
            
        content_type = content_type_match.group(1).strip()
        
        # Extract Content-ID
        content_id_match = re.search(r'Content-ID:\s*<([^>]+)>', part)
        content_id = content_id_match.group(1) if content_id_match else None
        
        # Extract Content-Location for reference
        location_match = re.search(r'Content-Location:\s*([^\n]+)', part)
        location = location_match.group(1).strip() if location_match else None
        
        # Extract Transfer-Encoding
        encoding_match = re.search(r'Content-Transfer-Encoding:\s*(\w+)', part)
        encoding = encoding_match.group(1) if encoding_match else '7bit'
        
        # Find the content (after double newline)
        content_start = part.find('\n\n')
        if content_start == -1:
            content_start = part.find('\r\n\r\n')
        if content_start == -1:
            return
            
        part_content = part[content_start + 2:]
        
        # Process based on content type
        if 'text/html' in content_type.lower():
            self._process_html(part_content, encoding, content_id, location)
        elif 'text/css' in content_type.lower():
            self._process_css(part_content, encoding, content_id, location)
        elif 'image/' in content_type.lower():
            self._process_image(part_content, encoding, content_id, location)
        elif 'font/' in content_type.lower() or 'application/font' in content_type.lower():
            self._process_font(part_content, encoding, content_id, location)
        elif 'audio/' in content_type.lower():
            self._process_audio(part_content, encoding, content_id, location)
            
    def _process_html(self, content, encoding, content_id, location):
        """Process HTML content"""
        if encoding == 'quoted-printable':
            content = self._decode_quoted_printable(content)
        else:
            # Remove any remaining =XX encoded characters
            content = self._decode_quoted_printable(content)
        
        # Clean up HTML
        content = content.strip()
        
        if self.html_content is None:
            self.html_content = content
            print(f"Extracted HTML content (length: {len(content)} chars)")
        
    def _process_css(self, content, encoding, content_id, location):
        """Process CSS content"""
        if encoding == 'quoted-printable':
            content = self._decode_quoted_printable(content)
        
        content = content.strip()
        
        # Generate a hash for the CSS filename
        if content_id:
            css_hash = hashlib.md5(content_id.encode()).hexdigest()[:8]
        else:
            css_hash = hashlib.md5(content[:100].encode()).hexdigest()[:8]
        
        css_filename = f"style_{css_hash}.css"
        
        # Replace cid: references with relative paths
        content = self._convert_cid_references(content, 'css', css_filename)
        
        self.css_content.append({
            'content': content,
            'filename': css_filename,
            'content_id': content_id,
            'location': location
        })
        
        print(f"Extracted CSS: {css_filename} (length: {len(content)} chars)")
        
    def _process_image(self, content, encoding, content_id, location):
        """Process image content"""
        if not content_id:
            return
            
        # Determine image type
        content_type_match = re.search(r'Content-Type:\s*([^\n]+)', 
                                        self.mhtml_path.read_text()[:100000])
        
        # Try to determine extension from content or content-type
        img_ext = 'png'  # default
        if 'jpeg' in content.lower() or 'jpg' in content.lower():
            img_ext = 'jpg'
        elif 'gif' in content.lower():
            img_ext = 'gif'
        elif 'webp' in content.lower():
            img_ext = 'webp'
        elif 'svg' in content.lower():
            img_ext = 'svg'
        elif 'avif' in content.lower():
            img_ext = 'avif'
            
        # Extract extension from content-type header in part
        img_hash = hashlib.md5(content_id.encode()).hexdigest()[:12]
        img_filename = f"image_{img_hash}.{img_ext}"
        img_path = self.images_dir / img_filename
        
        # Decode content
        try:
            if encoding == 'base64':
                decoded = base64.b64decode(content)
            elif encoding == 'quoted-printable':
                decoded = self._decode_quoted_printable(content).encode('latin-1')
            else:
                decoded = content.encode('latin-1')
        except Exception as e:
            print(f"Error decoding image {content_id}: {e}")
            return
            
        # Save image
        with open(img_path, 'wb') as f:
            f.write(decoded)
            
        self.images[content_id] = f"images/{img_filename}"
        print(f"Extracted image: {img_filename}")
        
    def _process_font(self, content, encoding, content_id, location):
        """Process font content"""
        if not content_id:
            return
            
        # Determine font type
        if 'woff2' in content.lower():
            font_ext = 'woff2'
        elif 'woff' in content.lower():
            font_ext = 'woff'
        elif 'ttf' in content.lower() or 'truetype' in content.lower():
            font_ext = 'ttf'
        elif 'otf' in content.lower() or 'opentype' in content.lower():
            font_ext = 'otf'
        else:
            font_ext = 'bin'
            
        font_hash = hashlib.md5(content_id.encode()).hexdigest()[:12]
        font_filename = f"font_{font_hash}.{font_ext}"
        font_path = self.images_dir / font_filename
        
        # Decode content
        try:
            if encoding == 'base64':
                decoded = base64.b64decode(content)
            else:
                decoded = self._decode_quoted_printable(content).encode('latin-1')
        except:
            return
            
        with open(font_path, 'wb') as f:
            f.write(decoded)
            
        self.fonts[content_id] = f"images/{font_filename}"
        print(f"Extracted font: {font_filename}")
        
    def _process_audio(self, content, encoding, content_id, location):
        """Process audio content"""
        # Audio files are typically base64 encoded
        if not content_id:
            return
            
        audio_hash = hashlib.md5(content_id.encode()).hexdigest()[:12]
        audio_filename = f"audio_{audio_hash}.mp3"
        audio_path = self.images_dir / audio_filename
        
        try:
            if encoding == 'base64':
                decoded = base64.b64decode(content)
            else:
                decoded = self._decode_quoted_printable(content).encode('latin-1')
        except:
            return
            
        with open(audio_path, 'wb') as f:
            f.write(decoded)
            
        self.images[content_id] = f"images/{audio_filename}"
        print(f"Extracted audio: {audio_filename}")
        
    def _decode_quoted_printable(self, text):
        """Decode quoted-printable encoded text"""
        # Pattern to match =XX hex escapes
        def replace_qp(match):
            try:
                return bytes.fromhex(match.group(1)).decode('utf-8', errors='replace')
            except:
                return match.group(0)
        
        text = re.sub(r'=([0-9A-Fa-f]{2})', replace_qp, text)
        
        # Handle soft line breaks (= at end of line)
        text = re.sub(r'=\r?\n', '', text)
        text = re.sub(r'=\n', '', text)
        
        return text
        
    def _convert_cid_references(self, content, resource_type, source_filename):
        """Convert cid: references to relative paths"""
        # Convert cid: references
        def replace_cid(match):
            cid = match.group(1)
            if cid in self.images:
                return f'"{self.images[cid]}"'
            elif cid in self.fonts:
                return f'"{self.fonts[cid]}"'
            else:
                # Try to find in other parts - use placeholder
                return match.group(0)
        
        content = re.sub(r'cid:([^\s"\']+)', replace_cid, content)
        
        # Also handle url(cid:...) format
        content = re.sub(r'url\(cid:([^\s"\']+)\)', 
                         lambda m: f'url("{self.images.get(m.group(1), m.group(0))}")', 
                         content)
        
        return content
        
    def generate_standalone_html(self):
        """Generate standalone HTML file with consolidated CSS"""
        if not self.html_content:
            print("No HTML content found!")
            return
            
        # Consolidate CSS
        consolidated_css = self._consolidate_css()
        
        # Save consolidated CSS
        css_path = self.css_dir / 'styles.css'
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(consolidated_css)
        print(f"Saved consolidated CSS: {css_path}")
        
        # Update HTML to reference consolidated CSS
        html = self.html_content
        
        # Remove old stylesheet references and add our own
        # Remove cid: stylesheet links
        html = re.sub(r'<link[^>]*href="cid:[^"]*"[^>]*>', '', html)
        
        # Remove any inline style tags that are just imports
        html = re.sub(r'<style[^>]*>@import[^;]*;</style>', '', html)
        
        # Add consolidated stylesheet link
        head_end = html.find('</head>')
        if head_end != -1:
            css_link = f'<link rel="stylesheet" href="css/styles.css">\n'
            html = html[:head_end] + css_link + html[head_end:]
        
        # Convert remaining cid: references in HTML
        html = self._convert_cid_references(html, 'html', 'index.html')
        
        # Also convert src="cid:..." patterns
        def replace_src_cid(match):
            cid = match.group(1)
            if cid in self.images:
                return f'src="{self.images[cid]}"'
            return match.group(0)
        
        html = re.sub(r'src="cid:([^"]+)"', replace_src_cid, html)
        
        # Fix any remaining cid: references in srcset, data, etc.
        html = re.sub(r'data-src="cid:([^"]+)"', 
                      lambda m: f'data-src="{self.images.get(m.group(1), m.group(0))}"', 
                      html)
        
        # Save HTML
        html_path = self.output_dir / 'index.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Saved HTML: {html_path}")
        
        return html_path
        
    def _consolidate_css(self):
        """Consolidate all CSS into one file"""
        css_parts = []
        
        for css_item in self.css_content:
            css = css_item['content']
            
            # Convert url(cid:...) to url(...)
            css = re.sub(r'url\(cid:([^\s")]+)\)', 
                        lambda m: f'url("{self.images.get(m.group(1), self.images.get(m.group(1).replace('@', ''), m.group(0)))}")', 
                        css)
            
            # Convert url("cid:...") to url(...)
            css = re.sub(r'url\("cid:([^")]+)"\)', 
                        lambda m: f'url("{self.images.get(m.group(1), m.group(0))}")', 
                        css)
            
            # Add source comment
            css_parts.append(f"\n/* Source: {css_item['content_id']} */\n")
            css_parts.append(css)
            
        return '\n'.join(css_parts)
        
    def convert(self):
        """Main conversion method"""
        print("=" * 60)
        print("MHTML to HTML/CSS Converter")
        print("=" * 60)
        
        self.create_directories()
        self.parse_mhtml()
        html_path = self.generate_standalone_html()
        
        print("=" * 60)
        print("Conversion complete!")
        print(f"Output directory: {self.output_dir}")
        print(f"HTML file: {html_path}")
        print("=" * 60)
        
        return self.output_dir


if __name__ == '__main__':
    import sys
    
    # Get MHTML file path
    mhtml_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not mhtml_file:
        # Look for MHTML file in current directory
        for f in Path('.').glob('*.mhtml'):
            mhtml_file = str(f)
            break
            
    if not mhtml_file:
        print("Error: No MHTML file specified")
        print("Usage: python mhtml_converter.py <path_to_mhtml_file>")
        sys.exit(1)
        
    converter = MHTMLConverter(mhtml_file)
    converter.convert()
