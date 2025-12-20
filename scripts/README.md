# Development Scripts

This directory contains Python-based validation and quality assurance tools for the Hyprland Wiki.

## Overview

These scripts implement defensive validation patterns to ensure:
- Configuration integrity
- Content quality and accessibility
- Development environment readiness
- Consistent standards enforcement

## Available Scripts

### `validate_config.py`
**Purpose:** Validates Hugo configuration for structural integrity and defensive patterns.

**Features:**
- Required field validation (baseURL, title, languageCode)
- Security settings audit (unsafe HTML, external link attributes)
- Defensive defaults verification (robots.txt, git info)
- Menu structure validation (weight uniqueness, ordering)
- Accessibility checks (language settings, search functionality)

**Usage:**
```bash
python3 scripts/validate_config.py [path/to/config.toml]
```

**Exit Codes:**
- `0`: All checks passed
- `1`: Errors found (must be fixed)

---

### `validate_content.py`
**Purpose:** Validates markdown content for quality, accessibility, and link integrity.

**Features:**
- Broken link detection (internal and external)
- Accessibility auditing (alt text, link text, heading hierarchy)
- Code block language specification
- Frontmatter validation
- Security checks (HTTP vs HTTPS links)

**Usage:**
```bash
python3 scripts/validate_content.py [path/to/content/]
```

**Statistics Reported:**
- Files checked
- Internal and external link counts
- Image count with accessibility checks

**Exit Codes:**
- `0`: No errors (warnings acceptable)
- `1`: Critical errors found

---

### `validate_env.py`
**Purpose:** Validates development environment setup and tool availability.

**Features:**
- Required tool detection (Hugo Extended, Go, Python, Git)
- Version compatibility checks
- Go module verification
- Git configuration validation
- Setup guidance for missing tools

**Usage:**
```bash
python3 scripts/validate_env.py
```

**Exit Codes:**
- `0`: Environment ready for development
- `1`: Missing required tools or configuration

---

## Defensive Patterns Implemented

### 1. **Graceful Failure**
All scripts handle errors without crashing and provide clear, actionable error messages.

### 2. **Progressive Validation**
Scripts continue checking even after finding errors, providing a complete report rather than failing fast.

### 3. **Severity Levels**
Issues are categorized by severity:
- **Error:** Must be fixed before proceeding
- **Warning:** Should be addressed but not blocking
- **Info:** Suggestions for improvement

### 4. **Human-Readable Output**
Reports use clear formatting with:
- Visual indicators (✅ ❌ ⚠️ ℹ️)
- Contextual file paths and line numbers
- Actionable recommendations

### 5. **Extensibility**
Each validator is designed as a class with methods that can be:
- Extended with new checks
- Customized per project needs
- Integrated into CI pipelines

---

## Integration with CI

These scripts are designed to be CI-friendly:

```yaml
# Example GitHub Actions integration
- name: Validate Configuration
  run: python3 scripts/validate_config.py

- name: Validate Content
  run: python3 scripts/validate_content.py

- name: Check Environment
  run: python3 scripts/validate_env.py
```

---

## Development Guidelines

### Adding New Validations

1. **Identify the validation category:**
   - Configuration integrity
   - Content quality
   - Security concerns
   - Accessibility issues
   - Structural problems

2. **Implement as a method:**
   ```python
   def _check_new_pattern(self, file_path: Path, content: str, lines: List[str]) -> None:
       """Check for new pattern."""
       # Implementation
       if issue_found:
           self.issues.append(ContentIssue(...))
   ```

3. **Add to validation flow:**
   ```python
   def validate(self) -> bool:
       # ... existing checks
       self._check_new_pattern()
   ```

4. **Test thoroughly:**
   - Test with valid input (should pass)
   - Test with invalid input (should catch issue)
   - Test with edge cases (should handle gracefully)

### Defensive Coding Standards

- Always handle file not found gracefully
- Provide context in error messages (file, line, reason)
- Use type hints for clarity
- Document expected inputs and outputs
- Fail with exit code 1 for errors, 0 for success

---

## Requirements

- **Python:** 3.7 or higher
- **Dependencies:** None (standard library only)

This keeps the scripts lightweight, portable, and easy to maintain.

---

## Future Enhancements

Potential additions to consider:
- Link availability checking (network requests)
- Image size validation
- Markdown linting integration
- Custom rule configuration via YAML
- JSON output format for CI parsing
- Performance metrics and timing

---

## Philosophy

These scripts embody the principle of **defensive innovation**:
- They add value without changing core functionality
- They catch problems before they reach production
- They guide developers toward best practices
- They make quality assurance automatic and consistent

Quality gates should be:
- **Automatic:** Run without manual intervention
- **Fast:** Complete in seconds
- **Clear:** Report what's wrong and how to fix it
- **Extensible:** Easy to add new checks
