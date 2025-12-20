#!/usr/bin/env python3
"""
Content Validation System
Validates markdown content for broken links, structural integrity, and defensive patterns.
"""

import sys
import re
from pathlib import Path
from typing import List, Set, Dict, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse


# Display constants for output formatting
MAX_DISPLAYED_ISSUES = 10
MAX_URL_DISPLAY_LENGTH = 50


@dataclass
class ContentIssue:
    """Represents an issue found in content."""
    file_path: Path
    line_number: int
    severity: str  # error, warning, info
    category: str  # link, structure, formatting, accessibility
    message: str


class ContentValidator:
    """Validates markdown content for quality and defensive patterns."""
    
    def __init__(self, content_dir: Path):
        self.content_dir = content_dir
        self.issues: List[ContentIssue] = []
        self.stats = {
            'files_checked': 0,
            'internal_links_found': 0,
            'external_links_found': 0,
            'images_found': 0,
        }
    
    def find_markdown_files(self) -> List[Path]:
        """Find all markdown files in content directory."""
        if not self.content_dir.exists():
            print(f"Error: Content directory not found: {self.content_dir}")
            return []
        
        return list(self.content_dir.rglob("*.md"))
    
    def validate_file(self, file_path: Path) -> None:
        """Validate a single markdown file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            self.stats['files_checked'] += 1
            
            # Check for various issues
            self._check_frontmatter(file_path, content, lines)
            self._check_links(file_path, content, lines)
            self._check_headings(file_path, content, lines)
            self._check_code_blocks(file_path, content, lines)
            self._check_accessibility(file_path, content, lines)
            
        except Exception as e:
            self.issues.append(ContentIssue(
                file_path=file_path,
                line_number=0,
                severity="error",
                category="structure",
                message=f"Failed to read file: {e}"
            ))
    
    def _check_frontmatter(self, file_path: Path, content: str, lines: List[str]) -> None:
        """Check for proper Hugo frontmatter."""
        # Hugo uses --- or +++ for frontmatter
        if not (content.startswith('---') or content.startswith('+++')):
            # Some files like _index.md might not need complex frontmatter
            if file_path.name != '_index.md':
                self.issues.append(ContentIssue(
                    file_path=file_path,
                    line_number=1,
                    severity="warning",
                    category="structure",
                    message="No frontmatter detected - consider adding title and metadata"
                ))
    
    def _check_links(self, file_path: Path, content: str, lines: List[str]) -> None:
        """Check links for potential issues."""
        # Markdown link pattern: [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        
        for line_num, line in enumerate(lines, 1):
            for match in re.finditer(link_pattern, line):
                link_text = match.group(1)
                link_url = match.group(2)
                
                # Skip anchor links and mailto
                if link_url.startswith('#') or link_url.startswith('mailto:'):
                    continue
                
                # Check for external links
                if link_url.startswith(('http://', 'https://')):
                    self.stats['external_links_found'] += 1
                    
                    # Warn about http (non-secure)
                    if link_url.startswith('http://'):
                        self.issues.append(ContentIssue(
                            file_path=file_path,
                            line_number=line_num,
                            severity="warning",
                            category="link",
                            message=f"Non-HTTPS link found: {link_url[:MAX_URL_DISPLAY_LENGTH]}..."
                        ))
                else:
                    self.stats['internal_links_found'] += 1
                    
                    # Check for potentially broken internal links
                    if not link_url.startswith('/') and not link_url.startswith('../'):
                        # Relative link without proper prefix
                        if '.' in link_url:  # Likely a file reference
                            self.issues.append(ContentIssue(
                                file_path=file_path,
                                line_number=line_num,
                                severity="info",
                                category="link",
                                message=f"Relative link without path prefix: {link_url}"
                            ))
                
                # Check for empty link text (bad for accessibility)
                if not link_text.strip():
                    self.issues.append(ContentIssue(
                        file_path=file_path,
                        line_number=line_num,
                        severity="warning",
                        category="accessibility",
                        message="Link has empty text - bad for screen readers"
                    ))
    
    def _check_headings(self, file_path: Path, content: str, lines: List[str]) -> None:
        """Check heading structure for accessibility and hierarchy."""
        headings = []
        
        for line_num, line in enumerate(lines, 1):
            # Check for ATX-style headings (# Heading)
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                headings.append((level, text, line_num))
        
        # Check for heading hierarchy issues
        if headings:
            prev_level = 0
            for level, text, line_num in headings:
                # Check for skipped levels (e.g., # then ###)
                if level > prev_level + 1 and prev_level > 0:
                    self.issues.append(ContentIssue(
                        file_path=file_path,
                        line_number=line_num,
                        severity="info",
                        category="structure",
                        message=f"Heading level jump from h{prev_level} to h{level} - may affect accessibility"
                    ))
                prev_level = level
    
    def _check_code_blocks(self, file_path: Path, content: str, lines: List[str]) -> None:
        """Check code blocks for language specification."""
        in_code_block = False
        code_block_start = 0
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Starting a code block
                    in_code_block = True
                    code_block_start = line_num
                    
                    # Check if language is specified
                    lang = line.strip()[3:].strip()
                    if not lang:
                        self.issues.append(ContentIssue(
                            file_path=file_path,
                            line_number=line_num,
                            severity="info",
                            category="formatting",
                            message="Code block without language specification - consider adding for syntax highlighting"
                        ))
                else:
                    # Ending a code block
                    in_code_block = False
    
    def _check_accessibility(self, file_path: Path, content: str, lines: List[str]) -> None:
        """Check for accessibility issues."""
        # Check for images without alt text
        # Pattern: ![alt](url) - if alt is empty, that's an issue
        image_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        
        for line_num, line in enumerate(lines, 1):
            for match in re.finditer(image_pattern, line):
                alt_text = match.group(1)
                image_url = match.group(2)
                
                self.stats['images_found'] += 1
                
                if not alt_text.strip():
                    # Truncate long image URLs for cleaner error messages
                    display_url = image_url[:MAX_URL_DISPLAY_LENGTH] if len(image_url) > MAX_URL_DISPLAY_LENGTH else image_url
                    truncation_suffix = "..." if len(image_url) > MAX_URL_DISPLAY_LENGTH else ""
                    
                    self.issues.append(ContentIssue(
                        file_path=file_path,
                        line_number=line_num,
                        severity="warning",
                        category="accessibility",
                        message=f"Image without alt text: {display_url}{truncation_suffix} (bad for screen readers)"
                    ))
    
    def validate_all(self) -> bool:
        """Validate all markdown files in content directory."""
        markdown_files = self.find_markdown_files()
        
        if not markdown_files:
            print(f"No markdown files found in {self.content_dir}")
            return True
        
        print(f"Validating {len(markdown_files)} markdown files...\n")
        
        for file_path in markdown_files:
            self.validate_file(file_path)
        
        return len([i for i in self.issues if i.severity == "error"]) == 0
    
    def print_report(self) -> None:
        """Print validation report."""
        print("\n" + "="*70)
        print("CONTENT VALIDATION REPORT")
        print("="*70 + "\n")
        
        # Statistics
        print("📊 Statistics:")
        print(f"  • Files checked: {self.stats['files_checked']}")
        print(f"  • Internal links: {self.stats['internal_links_found']}")
        print(f"  • External links: {self.stats['external_links_found']}")
        print(f"  • Images: {self.stats['images_found']}")
        print()
        
        # Group issues by severity
        errors = [i for i in self.issues if i.severity == "error"]
        warnings = [i for i in self.issues if i.severity == "warning"]
        info = [i for i in self.issues if i.severity == "info"]
        
        if errors:
            print(f"❌ ERRORS ({len(errors)}):")
            for issue in errors[:MAX_DISPLAYED_ISSUES]:
                rel_path = issue.file_path.relative_to(self.content_dir)
                print(f"  • {rel_path}:{issue.line_number} - {issue.message}")
            if len(errors) > MAX_DISPLAYED_ISSUES:
                print(f"  ... and {len(errors) - MAX_DISPLAYED_ISSUES} more errors")
            print()
        
        if warnings:
            print(f"⚠️  WARNINGS ({len(warnings)}):")
            for issue in warnings[:MAX_DISPLAYED_ISSUES]:
                rel_path = issue.file_path.relative_to(self.content_dir)
                print(f"  • {rel_path}:{issue.line_number} - {issue.message}")
            if len(warnings) > MAX_DISPLAYED_ISSUES:
                print(f"  ... and {len(warnings) - MAX_DISPLAYED_ISSUES} more warnings")
            print()
        
        if info:
            print(f"ℹ️  INFO ({len(info)}):")
            # Just show count, not all info messages
            print(f"  • {len(info)} informational suggestions found")
            print()
        
        # Summary
        print("-"*70)
        if errors:
            print("Status: ❌ FAILED - Fix errors before proceeding")
        elif warnings:
            print("Status: ⚠️  PASSED WITH WARNINGS - Review recommendations")
        else:
            print("Status: ✅ PASSED - All content validated successfully")
        print("="*70 + "\n")


def main() -> int:
    """Main entry point."""
    # Determine content path
    repo_root = Path(__file__).parent.parent
    content_dir = repo_root / "content"
    
    # Allow override via command line
    if len(sys.argv) > 1:
        content_dir = Path(sys.argv[1])
    
    print(f"Validating content directory: {content_dir}")
    
    validator = ContentValidator(content_dir)
    success = validator.validate_all()
    validator.print_report()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
