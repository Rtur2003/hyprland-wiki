#!/usr/bin/env python3
"""
Configuration Validation System
Validates Hugo config.toml for structural integrity, defensive patterns, and required fields.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    message: str
    severity: str = "error"  # error, warning, info


class ConfigValidator:
    """Validates Hugo configuration for defensive patterns and integrity."""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config_content = ""
        self.results: List[ValidationResult] = []
        
    def load_config(self) -> bool:
        """Load configuration file."""
        try:
            if not self.config_path.exists():
                self.results.append(ValidationResult(
                    passed=False,
                    message=f"Configuration file not found: {self.config_path}",
                    severity="error"
                ))
                return False
            
            self.config_content = self.config_path.read_text(encoding='utf-8')
            return True
        except Exception as e:
            self.results.append(ValidationResult(
                passed=False,
                message=f"Failed to read config: {e}",
                severity="error"
            ))
            return False
    
    def validate_required_fields(self) -> None:
        """Ensure all required configuration fields are present."""
        required_fields = [
            ('baseURL', 'Base URL must be defined for proper site generation'),
            ('title', 'Site title is required for SEO and accessibility'),
            ('languageCode', 'Language code required for proper HTML lang attribute'),
        ]
        
        for field, reason in required_fields:
            pattern = rf'^\s*{re.escape(field)}\s*=\s*.+$'
            if not re.search(pattern, self.config_content, re.MULTILINE):
                self.results.append(ValidationResult(
                    passed=False,
                    message=f"Missing required field '{field}': {reason}",
                    severity="error"
                ))
            else:
                self.results.append(ValidationResult(
                    passed=True,
                    message=f"Required field '{field}' is present",
                    severity="info"
                ))
    
    def validate_security_settings(self) -> None:
        """Check for security-related configuration issues."""
        # Check for unsafe markup rendering
        if 'unsafe = true' in self.config_content:
            # This is intentional in Hugo for flexibility, but should be documented
            self.results.append(ValidationResult(
                passed=True,
                message="Unsafe HTML rendering enabled - ensure content is trusted",
                severity="warning"
            ))
        
        # Validate external links have proper rel attributes
        if 'rel=' in self.config_content:
            if 'noreferrer' in self.config_content or 'noopener' in self.config_content:
                self.results.append(ValidationResult(
                    passed=True,
                    message="External links have security attributes (noreferrer/noopener)",
                    severity="info"
                ))
    
    def validate_defensive_defaults(self) -> None:
        """Ensure defensive defaults are in place."""
        checks = [
            ('enableRobotsTXT', 'Robots.txt should be enabled for SEO control'),
            ('enableGitInfo', 'Git info provides useful metadata for debugging'),
        ]
        
        for field, reason in checks:
            pattern = rf'^\s*{re.escape(field)}\s*=\s*true'
            if re.search(pattern, self.config_content, re.MULTILINE):
                self.results.append(ValidationResult(
                    passed=True,
                    message=f"Defensive default enabled: {field}",
                    severity="info"
                ))
            else:
                self.results.append(ValidationResult(
                    passed=False,
                    message=f"Recommended: Enable {field} - {reason}",
                    severity="warning"
                ))
    
    def validate_menu_structure(self) -> None:
        """Validate menu configuration for completeness and accessibility."""
        # Check for menu weight ordering
        menu_items = re.findall(r'\[\[menu\.main\]\](.*?)(?=\[\[menu\.main\]\]|$)', 
                                self.config_content, re.DOTALL)
        
        weights = []
        for item in menu_items:
            weight_match = re.search(r'weight\s*=\s*(\d+)', item)
            if weight_match:
                weights.append(int(weight_match.group(1)))
        
        if weights:
            if len(weights) == len(set(weights)):
                self.results.append(ValidationResult(
                    passed=True,
                    message=f"Menu weights are unique ({len(weights)} items)",
                    severity="info"
                ))
            else:
                self.results.append(ValidationResult(
                    passed=False,
                    message="Duplicate menu weights found - may cause ordering issues",
                    severity="warning"
                ))
    
    def validate_accessibility(self) -> None:
        """Check accessibility-related configuration."""
        # Ensure language is properly set
        if 'languageCode' in self.config_content or 'defaultContentLanguage' in self.config_content:
            self.results.append(ValidationResult(
                passed=True,
                message="Language configuration present for accessibility",
                severity="info"
            ))
        
        # Check for search functionality (improves accessibility)
        if re.search(r'type\s*=\s*["\']search["\']', self.config_content):
            self.results.append(ValidationResult(
                passed=True,
                message="Search functionality configured (enhances accessibility)",
                severity="info"
            ))
    
    def validate(self) -> bool:
        """Run all validations and return overall result."""
        if not self.load_config():
            return False
        
        self.validate_required_fields()
        self.validate_security_settings()
        self.validate_defensive_defaults()
        self.validate_menu_structure()
        self.validate_accessibility()
        
        # Determine overall result
        has_errors = any(r.severity == "error" and not r.passed for r in self.results)
        return not has_errors
    
    def print_report(self) -> None:
        """Print validation report."""
        print("\n" + "="*70)
        print("CONFIGURATION VALIDATION REPORT")
        print("="*70 + "\n")
        
        # Group by severity
        errors = [r for r in self.results if r.severity == "error" and not r.passed]
        warnings = [r for r in self.results if r.severity == "warning" and not r.passed]
        info = [r for r in self.results if r.severity == "info" and r.passed]
        
        if errors:
            print("❌ ERRORS:")
            for result in errors:
                print(f"  • {result.message}")
            print()
        
        if warnings:
            print("⚠️  WARNINGS:")
            for result in warnings:
                print(f"  • {result.message}")
            print()
        
        if info and not (errors or warnings):
            print("✅ ALL CHECKS PASSED:")
            for result in info[:5]:  # Show first 5
                print(f"  • {result.message}")
            if len(info) > 5:
                print(f"  ... and {len(info) - 5} more")
            print()
        
        # Summary
        total = len(self.results)
        passed = len([r for r in self.results if r.passed])
        print("-"*70)
        print(f"Summary: {passed}/{total} checks passed")
        
        if errors:
            print("Status: ❌ FAILED - Fix errors before proceeding")
        elif warnings:
            print("Status: ⚠️  PASSED WITH WARNINGS - Review recommendations")
        else:
            print("Status: ✅ PASSED")
        print("="*70 + "\n")


def main() -> int:
    """Main entry point."""
    # Determine config path
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / "config.toml"
    
    # Allow override via command line
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    
    print(f"Validating configuration: {config_path}")
    
    validator = ConfigValidator(config_path)
    success = validator.validate()
    validator.print_report()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
