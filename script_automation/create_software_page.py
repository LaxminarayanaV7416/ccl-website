#!/usr/bin/env python3
"""
Create a software page from an existing CCL software webpage.

Usage:
    python create_software_page.py https://ccl.cse.nd.edu/software/parrot/ parrot
    python create_software_page.py https://ccl.cse.nd.edu/software/workqueue/ workqueue --order 5
"""

import sys
import argparse
import re
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse
import html2text


def download_image(img_url, software_name, img_dir):
    """Download an image and save it to the software image directory."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(img_dir, exist_ok=True)
        
        response = requests.get(img_url, timeout=30)
        response.raise_for_status()
        
        # Get file extension from URL
        ext = os.path.splitext(urlparse(img_url).path)[1]
        if not ext:
            ext = '.png'
        
        # Save with software name
        filename = f"{software_name}-logo{ext}"
        filepath = os.path.join(img_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"  ✓ Downloaded image: {filename}")
        return filename
    
    except Exception as e:
        print(f"  ✗ Failed to download image: {e}")
        return None


def extract_keyword_from_html(soup):
    """Extract the keyword/tag from the publications section."""
    # Look for text like "Showing papers with tag <b>parrot</b>"
    # Search in the HTML string for the pattern
    html_str = str(soup)
    match = re.search(r'Showing papers with tag\s+<b>(\w+)</b>', html_str, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # Alternative: look in plain text
    text = soup.get_text()
    match = re.search(r'Showing papers with tag\s+(\w+)', text, re.IGNORECASE)
    if match:
        return match.group(1)
    
    return None


def extract_paper_titles_from_html(soup):
    """Extract paper titles from the publications section."""
    titles = []
    
    # Find all tables in the publications section
    # Papers are typically in table rows with the title in <b> tags inside <a> tags
    for table in soup.find_all('table'):
        # Look for links with <b> tags containing titles
        for link in table.find_all('a'):
            b_tag = link.find('b')
            if b_tag:
                title = b_tag.get_text().strip()
                if title and len(title) > 10:  # Reasonable title length
                    titles.append(title)
    
    return titles


def html_to_markdown(html_content):
    """Convert HTML to Markdown."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    h.unicode_snob = True
    h.skip_internal_links = True
    
    markdown = h.handle(html_content)
    
    # Clean up excessive newlines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    return markdown.strip()


def extract_description(soup, base_url):
    """Extract the main description content from the page."""
    # Find the subpagebody section
    body = soup.find('td', class_='subpagebody')
    if not body:
        return ""
    
    # Get all content after the first h2 heading and before "Publications" section
    content_parts = []
    found_heading = False
    
    for element in body.children:
        if not element.name:
            continue
        
        # Start collecting after the first h2 heading
        if element.name == 'h2' and not found_heading:
            found_heading = True
            # Include the heading
            content_parts.append(str(element))
            continue
        
        # Stop at More Info or Publications sections (subsequent h2s)
        if element.name == 'h2' and found_heading:
            h2_text = element.get_text().lower()
            if 'more info' in h2_text or 'publication' in h2_text or 'documentation' in h2_text:
                break
        
        # Collect content after the heading
        if found_heading:
            # Skip large images with links (they're usually logos)
            if element.name == 'a' and element.find('img'):
                img = element.find('img')
                # Skip if it's a large image (height > 200 or width > 200)
                height = img.get('height', '0')
                width = img.get('width', '0')
                try:
                    if int(height) > 200 or int(width) > 200:
                        continue
                except:
                    pass
            
            content_parts.append(str(element))
    
    # Convert to markdown
    html_content = '\n'.join(content_parts)
    markdown = html_to_markdown(html_content)
    
    return markdown


def get_manual_link(soup, software_name):
    """Extract the manual link from the More Info section."""
    # Look for links containing 'manual' in the href
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if 'manual' in href.lower() and software_name in href.lower():
            # Make sure it's a relative or full URL
            if href.startswith('http'):
                return href
            elif href.startswith('../'):
                return f"https://ccl.cse.nd.edu/software/manuals/{software_name}.html"
            else:
                return f"https://ccl.cse.nd.edu/software/manuals/{href}"
    
    # Default fallback
    return f"https://ccl.cse.nd.edu/software/manuals/{software_name}.html"


def create_software_markdown(software_name, description, manual_link, logo_filename, order, carousel):
    """Create the markdown content for the software page."""
    # Capitalize first letter for title
    title = software_name.capitalize()
    
    # Use placeholder text for front matter descriptions (to be manually edited later)
    short_desc = "Description goes here."
    long_desc_placeholder = "Description goes here."
    
    # Use actual extracted description for the page body
    body_content = description if description else "Description goes here."
    
    content = f"""---
layout: software3
title: {title}
description: {short_desc}
long_description: "{long_desc_placeholder}"
"""
    
    if logo_filename:
        content += f'img: assets/img/software/{logo_filename}\n'
    
    content += f"""carousel: {str(carousel).lower()}
order: {order}
category: tools
publication_keywords:
  - {software_name}
links:
  - name: User Manual
    url: {manual_link}
---

{body_content}
"""
    
    return content


def backup_bib_file(bib_file):
    """Create a timestamped backup of the bib file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"{bib_file}.bak.{timestamp}"
    
    with open(bib_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Backup created: {backup_file}")
    return backup_file


def normalize_title(title):
    """Normalize title for comparison."""
    normalized = re.sub(r'[{}\\]', '', title)
    normalized = re.sub(r'[^\w\s]', ' ', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized.lower().strip()


def find_entry_by_title(bib_content, title):
    """Find a bib entry that matches the given title."""
    normalized_target = normalize_title(title)
    
    entry_pattern = r'(@\w+\s*\{[^@]+\n\})'
    entries = re.finditer(entry_pattern, bib_content, re.MULTILINE | re.DOTALL)
    
    for match in entries:
        entry_text = match.group(0)
        title_match = re.search(r'title\s*=\s*["{]([^"}]+)["}]', entry_text, re.IGNORECASE | re.DOTALL)
        
        if title_match:
            entry_title = title_match.group(1)
            normalized_entry = normalize_title(entry_title)
            
            if normalized_target == normalized_entry or \
               normalized_target in normalized_entry or \
               normalized_entry in normalized_target:
                return entry_text, match.start(), match.end()
    
    return None, None, None


def add_keyword_to_entry(entry_text, keyword):
    """Add keyword field to a bib entry if not already present."""
    keywords_match = re.search(r'keywords\s*=\s*\{([^}]*)\}', entry_text, re.IGNORECASE)
    
    if keywords_match:
        existing_keywords = keywords_match.group(1).strip()
        keyword_list = [k.strip() for k in existing_keywords.split(',')]
        if keyword in keyword_list:
            return entry_text, False
        
        if existing_keywords:
            new_keywords = f"{existing_keywords}, {keyword}"
        else:
            new_keywords = keyword
        
        entry_text = re.sub(
            r'(keywords\s*=\s*\{)[^}]*(\})',
            f'\\1{new_keywords}\\2',
            entry_text,
            flags=re.IGNORECASE
        )
        return entry_text, True
    
    # Keywords field doesn't exist, add it
    cclpaperid_match = re.search(r'(cclpaperid\s*=\s*"[^"]+",?\s*\n)', entry_text, re.IGNORECASE)
    if cclpaperid_match:
        insert_pos = cclpaperid_match.end()
        entry_text = (
            entry_text[:insert_pos] +
            f"keywords={{{keyword}}},\n" +
            entry_text[insert_pos:]
        )
        return entry_text, True
    
    pdf_match = re.search(r'(\s*)(pdf\s*=)', entry_text, re.IGNORECASE)
    if pdf_match:
        indent = pdf_match.group(1)
        insert_pos = pdf_match.start()
        entry_text = (
            entry_text[:insert_pos] +
            f"keywords={{{keyword}}},\n{indent}" +
            entry_text[insert_pos:]
        )
        return entry_text, True
    
    return entry_text, False


def update_papers_bib(titles, keyword, bib_file):
    """Update papers.bib with the keyword for matching papers."""
    print(f"\n📚 Updating papers.bib with keyword '{keyword}'...")
    
    # Read bib file
    with open(bib_file, 'r', encoding='utf-8') as f:
        bib_content = f.read()
    
    original_content = bib_content
    updated_count = 0
    not_found = []
    already_has_keyword = []
    
    for i, title in enumerate(titles, 1):
        print(f"  {i:2d}. {title[:60]}{'...' if len(title) > 60 else ''}")
        entry_text, start_pos, end_pos = find_entry_by_title(bib_content, title)
        
        if entry_text:
            updated_entry, was_updated = add_keyword_to_entry(entry_text, keyword)
            
            if was_updated:
                bib_content = bib_content[:start_pos] + updated_entry + bib_content[end_pos:]
                updated_count += 1
                print(f"      ✓ Added keyword '{keyword}'")
            else:
                already_has_keyword.append(title)
                print(f"      - Already has keyword")
        else:
            not_found.append(title)
            print(f"      ✗ Not found in bib file")
    
    # Only write if something changed
    if bib_content != original_content:
        # Create backup first
        backup_bib_file(bib_file)
        
        with open(bib_file, 'w', encoding='utf-8') as f:
            f.write(bib_content)
        print(f"\n  ✓ Updated {updated_count} entries in papers.bib")
    else:
        print(f"\n  - No changes made to papers.bib")
    
    return updated_count, len(already_has_keyword), len(not_found)


def main():
    parser = argparse.ArgumentParser(
        description='Create a software page from an existing CCL software webpage.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_software_page.py https://ccl.cse.nd.edu/software/parrot/ parrot
  python create_software_page.py https://ccl.cse.nd.edu/software/workqueue/ workqueue --order 5
  python create_software_page.py https://ccl.cse.nd.edu/software/chirp/ chirp --carousel
        """
    )
    parser.add_argument(
        'url',
        help='URL of the CCL software page to download'
    )
    parser.add_argument(
        'name',
        help='Software name (e.g., parrot, workqueue, chirp)'
    )
    parser.add_argument(
        '--order',
        type=int,
        default=9,
        help='Order in the software list (default: 9)'
    )
    parser.add_argument(
        '--carousel',
        action='store_true',
        help='Enable carousel display'
    )
    parser.add_argument(
        '--bib-file',
        default='../_bibliography/papers.bib',
        help='Path to papers.bib file (default: ../_bibliography/papers.bib)'
    )
    
    args = parser.parse_args()
    
    # Get absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(script_dir, '..', 'assets', 'img', 'software')
    software_dir = os.path.join(script_dir, '..', '_software')
    
    if not os.path.isabs(args.bib_file):
        bib_file = os.path.join(script_dir, args.bib_file)
    else:
        bib_file = args.bib_file
    
    print(f"\n{'='*70}")
    print(f"CREATING SOFTWARE PAGE: {args.name.upper()}")
    print(f"{'='*70}")
    
    # Step 1: Download HTML
    print(f"\n📥 Downloading HTML from: {args.url}")
    try:
        response = requests.get(args.url, timeout=30)
        response.raise_for_status()
        print(f"  ✓ Downloaded {len(response.content)} bytes")
    except Exception as e:
        print(f"  ✗ Failed to download: {e}")
        sys.exit(1)
    
    # Step 2: Parse HTML
    print(f"\n🔍 Parsing HTML content...")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 3: Extract main image
    print(f"\n🖼️  Extracting logo image...")
    logo_filename = None
    body = soup.find('td', class_='subpagebody')
    if body:
        img_tag = body.find('img')
        if img_tag and img_tag.get('src'):
            img_url = urljoin(args.url, img_tag.get('src'))
            logo_filename = download_image(img_url, args.name, img_dir)
    
    # Step 4: Extract description
    print(f"\n📝 Extracting description...")
    description = extract_description(soup, args.url)
    if description:
        lines = description.split('\n')
        preview = '\n'.join(lines[:3])
        print(f"  ✓ Extracted {len(description)} characters")
        print(f"  Preview:\n{preview}...")
    else:
        print(f"  ⚠️  No description found")
    
    # Step 5: Get manual link
    print(f"\n🔗 Finding manual link...")
    manual_link = get_manual_link(soup, args.name)
    print(f"  ✓ Manual: {manual_link}")
    
    # Step 6: Extract keyword
    print(f"\n🏷️  Extracting publication keyword...")
    keyword = extract_keyword_from_html(soup)
    if keyword:
        print(f"  ✓ Found keyword: '{keyword}'")
    else:
        print(f"  ⚠️  No keyword found, using software name: '{args.name}'")
        keyword = args.name
    
    # Step 7: Extract paper titles
    print(f"\n📄 Extracting paper titles...")
    paper_titles = extract_paper_titles_from_html(soup)
    print(f"  ✓ Found {len(paper_titles)} papers")
    
    # Step 8: Create markdown file
    print(f"\n📄 Creating software markdown file...")
    markdown_content = create_software_markdown(
        args.name,
        description,
        manual_link,
        logo_filename,
        args.order,
        args.carousel
    )
    
    software_file = os.path.join(software_dir, f"{args.name}.md")
    os.makedirs(software_dir, exist_ok=True)
    
    with open(software_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"  ✓ Created: {software_file}")
    
    # Step 9: Update papers.bib
    if paper_titles and os.path.exists(bib_file):
        updated, already_has, not_found = update_papers_bib(paper_titles, keyword, bib_file)
        
        print(f"\n{'='*70}")
        print(f"SUMMARY")
        print(f"{'='*70}")
        print(f"  Software page:       {software_file}")
        print(f"  Logo image:          {logo_filename or 'N/A'}")
        print(f"  Keyword:             {keyword}")
        print(f"  Papers found:        {len(paper_titles)}")
        print(f"  ✓ Updated in bib:    {updated}")
        print(f"  - Already tagged:    {already_has}")
        print(f"  ✗ Not found:         {not_found}")
        print(f"{'='*70}")
    else:
        print(f"\n{'='*70}")
        print(f"SUMMARY")
        print(f"{'='*70}")
        print(f"  Software page:       {software_file}")
        print(f"  Logo image:          {logo_filename or 'N/A'}")
        print(f"  Keyword:             {keyword}")
        print(f"  Papers found:        {len(paper_titles)}")
        print(f"{'='*70}")
    
    print(f"\n✓ Successfully created software page for '{args.name}'!")


if __name__ == '__main__':
    main()
