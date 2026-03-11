#!/usr/bin/env python3
"""
Check papers in bibliography for correctness and critical fields.
Validates all bib entries and reports missing fields.
Optionally generates missing thumbnails with --generate-missing flag.

Run from root directory: python script_automation/check-papers.py
"""

import argparse
import re
import sys
import shutil
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from html.parser import HTMLParser

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None


class BibEntry:
    def __init__(self, raw_block: str):
        self.raw = raw_block
        self.key = self._parse_key(raw_block)
        self.fields = self._parse_fields(raw_block)
        self.title = self._clean(self.fields.get("title", ""))

    def _parse_key(self, raw: str) -> str:
        """Extract the citation key from bib entry."""
        lines = raw.splitlines()
        for i, ln in enumerate(lines[:4]):
            s = ln.strip()
            if s.startswith('@') and s.endswith('{'):
                if i + 1 < len(lines):
                    return lines[i + 1].strip().rstrip(',').strip()
        m = re.search(r"^@\w+\s*\{\s*([^,\n]+),", raw, re.M)
        return m.group(1).strip() if m else ""

    def _parse_fields(self, raw: str) -> Dict[str, str]:
        """Parse all fields from bib entry."""
        fields: Dict[str, str] = {}
        for ln in raw.splitlines():
            m = re.match(r"^\s*(\w+)\s*=\s*(.+?)(,\s*)?$", ln)
            if not m:
                continue
            name = m.group(1).lower()
            val = m.group(2).strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if val.startswith('{') and val.endswith('}'):
                val = val[1:-1]
            fields[name] = val.strip()
        return fields

    def _clean(self, s: str) -> str:
        """Normalize whitespace in text."""
        return re.sub(r"\s+", " ", s.strip())

    def has_field(self, field_name: str) -> bool:
        """Check if field exists."""
        return field_name.lower() in self.fields

    def get_field(self, field_name: str) -> Optional[str]:
        """Get field value."""
        return self.fields.get(field_name.lower())

    def render_with_updates(self, pdf_rel: Optional[str] = None, preview_rel: Optional[str] = None) -> str:
        """Update bib entry with pdf and/or preview fields."""
        lines = self.raw.splitlines()
        out: List[str] = []
        have_pdf_field = False
        have_preview_field = False

        for ln in lines:
            if re.match(r"^\s*pdf\s*=", ln):
                have_pdf_field = True
            elif re.match(r"^\s*preview\s*=", ln):
                have_preview_field = True
            out.append(ln)

        # If both fields already exist, return as-is
        if have_pdf_field and have_preview_field:
            return "\n".join(out)

        # Find closing brace
        closing_brace_idx = -1
        for i in range(len(out) - 1, -1, -1):
            if out[i].strip() == '}':
                closing_brace_idx = i
                break

        if closing_brace_idx == -1:
            return "\n".join(out)

        # Find last field line
        last_field_idx = -1
        for i in range(closing_brace_idx - 1, -1, -1):
            if out[i].strip() and not out[i].strip().startswith('@'):
                last_field_idx = i
                break

        # Ensure last field has comma
        if last_field_idx != -1:
            line = out[last_field_idx].rstrip()
            if not line.endswith(','):
                out[last_field_idx] = line + ','

        # Insert new fields before closing brace
        insert_lines = []
        if pdf_rel and not have_pdf_field:
            insert_lines.append(f"pdf={{{pdf_rel}}},")
        if preview_rel and not have_preview_field:
            insert_lines.append(f"preview={{{preview_rel}}},")

        # Insert in reverse order
        for line in reversed(insert_lines):
            out.insert(closing_brace_idx, line)

        return "\n".join(out)


def parse_bib(path: Path) -> Tuple[str, List[BibEntry]]:
    """Parse bib file, returning (header_text, entries_list)."""
    text = path.read_text(encoding="utf-8")

    # Extract header
    first_at = text.find('@')
    header = text[:first_at] if first_at > 0 else ""

    # Parse entries
    entries: List[BibEntry] = []
    entry_text = text[first_at:] if first_at >= 0 else text

    # Split on closing brace followed by newline
    blocks = re.split(r"\n\}\s*\n", entry_text)

    for b in blocks:
        b = b.strip()
        if not b or not b.startswith('@'):
            continue
        entries.append(BibEntry(b + "\n}"))

    return header, entries


class PDFLinkParser(HTMLParser):
    """Extract PDF link from ArXiv HTML page."""
    def __init__(self):
        super().__init__()
        self.pdf_url = None

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href' and '/pdf/' in value and value.endswith('.pdf'):
                    self.pdf_url = value
                    return


def extract_arxiv_pdf_url(arxiv_url: str) -> Optional[str]:
    """Extract PDF URL from arXiv abstract page."""
    try:
        response = requests.get(arxiv_url, timeout=30)
        response.raise_for_status()
        parser = PDFLinkParser()
        parser.feed(response.text)
        if parser.pdf_url:
            if not parser.pdf_url.startswith('http'):
                return f"https://arxiv.org{parser.pdf_url}"
            return parser.pdf_url
    except Exception as e:
        pass
    return None


def resolve_pdf_url(url: str, eprint: Optional[str] = None) -> Optional[str]:
    """Resolve PDF URL from various sources."""
    if not url:
        return None

    url = url.strip()

    # Direct PDF link
    if url.endswith('.pdf'):
        return url

    # ArXiv abstract page - use eprint ID if available for direct PDF URL
    if 'arxiv.org/abs' in url or 'arxiv.org' in url:
        # If we have eprint ID, construct direct PDF URL (more reliable)
        if eprint:
            eprint = eprint.strip()
            return f"https://arxiv.org/pdf/{eprint}.pdf"
        # Otherwise try HTML parsing as fallback
        pdf_url = extract_arxiv_pdf_url(url)
        if pdf_url:
            return pdf_url

    return None


def download_pdf(url: str, dest: Path) -> None:
    """Download PDF from URL."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    dest.write_bytes(response.content)


def generate_thumbnail(pdf_path: Path, thumb_path: Path) -> None:
    """Generate PNG thumbnail from first page of PDF."""
    if fitz is None:
        raise Exception("PyMuPDF not installed")

    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    thumb_path.write_bytes(pix.tobytes("png"))


def write_bib(path: Path, header: str, entries: List[str]) -> None:
    """Write bib file with header and entries."""
    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copyfile(path, backup)
    content = header + "\n\n".join(entries) + "\n"
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check papers in bibliography for correctness and missing fields",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python script_automation/check-papers.py              # Check and report issues
  python script_automation/check-papers.py --verbose    # Show detailed report
  python script_automation/check-papers.py --generate-missing  # Generate missing files
        """
    )
    parser.add_argument("--bib", type=Path, default=Path("_bibliography/papers.bib"))
    parser.add_argument("--pdf-dir", type=Path, default=Path("assets/paper/pdf"))
    parser.add_argument("--preview-dir", type=Path, default=Path("assets/paper/preview"))
    parser.add_argument("--generate-missing", action="store_true",
                       help="Generate missing PDFs and thumbnails")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show detailed report for all entries")
    args = parser.parse_args()

    bib_path = args.bib
    pdf_dir = args.pdf_dir
    preview_dir = args.preview_dir

    # Verify bib file exists
    if not bib_path.exists():
        print(f"Error: Bib file not found: {bib_path}")
        return 1

    header, entries = parse_bib(bib_path)
    print(f"Checking {len(entries)} bibliography entries\n")

    # Critical fields that must exist
    CRITICAL_FIELDS = {"pdf", "preview"}

    # Track issues
    issues = []
    generated_count = 0
    downloaded_count = 0
    updated_entries = []

    for idx, entry in enumerate(entries, 1):
        entry_issues = []
        
        has_pdf_field = entry.has_field("pdf")
        has_preview_field = entry.has_field("preview")
        has_url_field = entry.has_field("url")

        pdf_path = pdf_dir / f"{entry.key}.pdf"
        preview_path = preview_dir / f"{entry.key}.png"

        pdf_exists = pdf_path.exists()
        preview_exists = preview_path.exists()

        # Check for missing fields
        if not has_pdf_field:
            entry_issues.append("missing pdf field")
        if not has_preview_field:
            entry_issues.append("missing preview field")

        # Check if files exist
        if has_pdf_field and not pdf_exists:
            entry_issues.append("pdf field exists but file missing")
        if has_preview_field and not preview_exists:
            entry_issues.append("preview field exists but file missing")

        # Verbose: show all entries
        if args.verbose:
            status = "✓ OK" if not entry_issues else f"⚠ {len(entry_issues)} issue(s)"
            print(f"[{idx}/{len(entries)}] {entry.key:<50} {status}")
            if entry_issues:
                for issue in entry_issues:
                    print(f"   - {issue}")

        # Track entry with issues
        if entry_issues:
            issues.append((entry.key, entry_issues))

        # Optional: Generate missing files
        if args.generate_missing and entry_issues:
            try:
                # Case 1: PDF file missing but field exists - skip (can't regenerate)
                if has_pdf_field and not pdf_exists:
                    pass  # Skip

                # Case 2: PDF exists but preview missing - generate thumbnail
                if pdf_exists and not preview_exists:
                    generate_thumbnail(pdf_path, preview_path)
                    generated_count += 1
                    updated_entries.append((entry.key, "generated thumbnail"))

                # Case 3: No PDF field but URL exists - download and generate
                if not has_pdf_field and has_url_field:
                    url = entry.get_field("url")
                    eprint = entry.get_field("eprint")
                    pdf_url = resolve_pdf_url(url, eprint)
                    if pdf_url:
                        download_pdf(pdf_url, pdf_path)
                        downloaded_count += 1
                        generate_thumbnail(pdf_path, preview_path)
                        generated_count += 1
                        # Update entry
                        entry = entry.render_with_updates(
                            pdf_rel=f"{entry.key}.pdf",
                            preview_rel=f"{entry.key}.png"
                        )
                        updated_entries.append((entry.key, "downloaded and generated"))

            except Exception as e:
                if not args.verbose:
                    print(f"[{idx}/{len(entries)}] {entry.key}: failed to generate - {e}")

        # Always append to updated entries (even if not modified)
        if args.generate_missing:
            if entry not in updated_entries:
                updated_entries.append(entry.raw if isinstance(entry, BibEntry) else entry)
        else:
            updated_entries.append(entry.raw)

    # Report missing fields
    print("\n" + "=" * 80)
    print("MISSING CRITICAL FIELDS REPORT")
    print("=" * 80)
    
    if not issues:
        print("✓ All entries have critical fields (pdf, preview)")
    else:
        print(f"Found {len(issues)} entries with missing fields:\n")
        for key, entry_issues in issues:
            print(f"  {key}")
            for issue in entry_issues:
                print(f"    - {issue}")
        print()

    # Summary
    if args.generate_missing:
        print("=" * 80)
        print("GENERATION SUMMARY")
        print("=" * 80)
        print(f"Thumbnails generated: {generated_count}")
        print(f"PDFs downloaded: {downloaded_count}")
        
        if downloaded_count > 0 or generated_count > 0:
            write_bib(bib_path, header, updated_entries)
            print(f"✓ Bibliography updated and backed up")
        print()

    # Exit code
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
