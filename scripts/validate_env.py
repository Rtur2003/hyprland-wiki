#!/usr/bin/env python3
"""
Development Environment Validation
Ensures all required tools and dependencies are properly configured.
"""

import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ToolCheck:
    """Result of a tool availability check."""
    tool: str
    required: bool
    found: bool
    version: Optional[str] = None
    message: Optional[str] = None


class EnvironmentValidator:
    """Validates development environment setup."""
    
    def __init__(self):
        self.checks: List[ToolCheck] = []
        self.repo_root = Path(__file__).parent.parent
    
    def check_command(self, cmd: str, version_arg: str = "--version", 
                     required: bool = True) -> ToolCheck:
        """Check if a command is available and get its version."""
        found = shutil.which(cmd) is not None
        version = None
        message = None
        
        if found:
            try:
                result = subprocess.run(
                    [cmd, version_arg],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                # Get first line of output
                output = result.stdout or result.stderr
                version = output.strip().split('\n')[0] if output else "Unknown"
            except Exception as e:
                version = "Unknown"
                message = f"Found but version check failed: {e}"
        else:
            message = f"Not found in PATH"
        
        return ToolCheck(
            tool=cmd,
            required=required,
            found=found,
            version=version,
            message=message
        )
    
    def check_go_modules(self) -> Tuple[bool, str]:
        """Check if Go modules are properly initialized."""
        go_mod = self.repo_root / "go.mod"
        go_sum = self.repo_root / "go.sum"
        
        if not go_mod.exists():
            return False, "go.mod not found"
        
        if not go_sum.exists():
            return False, "go.sum not found - run 'hugo mod get' or 'hugo mod tidy'"
        
        # Check if modules are up to date
        try:
            result = subprocess.run(
                ["go", "mod", "verify"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return True, "Go modules verified"
            else:
                return False, f"Go module verification failed: {result.stderr}"
        except Exception as e:
            return False, f"Could not verify Go modules: {e}"
    
    def check_hugo_version(self) -> Tuple[bool, str]:
        """Check if Hugo version meets minimum requirements."""
        hugo_check = self.check_command("hugo", "version", required=True)
        
        if not hugo_check.found:
            return False, "Hugo not installed"
        
        # Hugo extended is required for this project
        if hugo_check.version and "extended" in hugo_check.version.lower():
            return True, f"Hugo extended found: {hugo_check.version}"
        else:
            return False, f"Hugo extended required but found: {hugo_check.version}"
    
    def check_python_version(self) -> Tuple[bool, str]:
        """Check if Python version is adequate."""
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            version_str = result.stdout.strip()
            
            # Extract version number
            import re
            match = re.search(r'Python (\d+)\.(\d+)', version_str)
            if match:
                major, minor = int(match.group(1)), int(match.group(2))
                if major >= 3 and minor >= 7:
                    return True, f"Python {major}.{minor} (meets requirement: 3.7+)"
                else:
                    return False, f"Python {major}.{minor} found but 3.7+ required"
            
            return True, version_str
        except Exception as e:
            return False, f"Python check failed: {e}"
    
    def check_git_config(self) -> Tuple[bool, str]:
        """Check if Git is properly configured."""
        try:
            # Check if we're in a git repo
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return False, "Not a git repository"
            
            # Check if user is configured
            name_result = subprocess.run(
                ["git", "config", "user.name"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            email_result = subprocess.run(
                ["git", "config", "user.email"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            has_name = name_result.returncode == 0 and name_result.stdout.strip()
            has_email = email_result.returncode == 0 and email_result.stdout.strip()
            
            if has_name and has_email:
                return True, "Git user configured"
            else:
                return False, "Git user.name or user.email not configured"
                
        except Exception as e:
            return False, f"Git check failed: {e}"
    
    def validate(self) -> bool:
        """Run all validation checks."""
        print("Checking development environment...\n")
        
        # Required tools
        print("🔧 Required Tools:")
        
        # Hugo (required, extended version)
        hugo_ok, hugo_msg = self.check_hugo_version()
        print(f"  {'✅' if hugo_ok else '❌'} Hugo Extended: {hugo_msg}")
        
        # Go (required for Hugo modules)
        go_check = self.check_command("go", "version", required=True)
        self.checks.append(go_check)
        print(f"  {'✅' if go_check.found else '❌'} Go: {go_check.version or go_check.message}")
        
        # Python (for validation scripts)
        python_ok, python_msg = self.check_python_version()
        print(f"  {'✅' if python_ok else '❌'} Python: {python_msg}")
        
        # Git
        git_check = self.check_command("git", "version", required=True)
        self.checks.append(git_check)
        print(f"  {'✅' if git_check.found else '❌'} Git: {git_check.version or git_check.message}")
        
        print()
        
        # Configuration checks
        print("⚙️  Configuration:")
        
        # Git config
        git_config_ok, git_config_msg = self.check_git_config()
        print(f"  {'✅' if git_config_ok else '❌'} Git Configuration: {git_config_msg}")
        
        # Go modules
        if go_check.found:
            go_mod_ok, go_mod_msg = self.check_go_modules()
            print(f"  {'✅' if go_mod_ok else '⚠️ '} Go Modules: {go_mod_msg}")
        else:
            go_mod_ok = False
            print(f"  ⚠️  Go Modules: Skipped (Go not found)")
        
        print()
        
        # Optional but recommended tools
        print("📦 Optional Tools:")
        
        make_check = self.check_command("make", "--version", required=False)
        print(f"  {'✅' if make_check.found else 'ℹ️ '} Make: {make_check.version or 'Not found (optional)'}")
        
        print()
        
        # Determine overall success
        all_required_ok = (
            hugo_ok and 
            go_check.found and 
            python_ok and 
            git_check.found and 
            git_config_ok
        )
        
        return all_required_ok
    
    def print_summary(self, success: bool) -> None:
        """Print validation summary."""
        print("="*70)
        if success:
            print("✅ Development environment is properly configured!")
            print("\nYou can start developing with:")
            print("  hugo serve        # Start local development server")
            print("  python3 scripts/validate_config.py   # Validate configuration")
            print("  python3 scripts/validate_content.py  # Validate content")
        else:
            print("❌ Development environment setup incomplete")
            print("\nPlease install missing requirements:")
            print("  • Hugo Extended: https://gohugo.io/installation/")
            print("  • Go: https://go.dev/doc/install")
            print("  • Python 3.7+: https://www.python.org/downloads/")
            print("\nThen run 'hugo mod get' to fetch Hugo modules")
        print("="*70)


def main() -> int:
    """Main entry point."""
    validator = EnvironmentValidator()
    success = validator.validate()
    validator.print_summary(success)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
