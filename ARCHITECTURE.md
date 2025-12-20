# Architecture Documentation

## Overview

The Hyprland Wiki is a static documentation site built with Hugo, implementing defensive design patterns for robustness, accessibility, and maintainability.

---

## Technology Stack

### Core Technologies

- **Hugo Extended** (Static Site Generator)
  - Version: Latest
  - Module: `github.com/imfing/hextra` (theme)
  - Purpose: Content transformation and site generation

- **Go** (Runtime for Hugo modules)
  - Version: 1.22+
  - Purpose: Dependency management and Hugo module support

- **Python** (Tooling and Validation)
  - Version: 3.7+
  - Purpose: Quality assurance and validation scripts
  - Zero external dependencies (stdlib only)

### Content

- **Markdown** (Content format)
  - Frontmatter: YAML
  - Extensions: Goldmark renderer with HTML support
  - Highlighting: Syntax highlighting with language specifications

---

## Directory Structure

```
hyprland-wiki/
├── .github/
│   ├── workflows/          # CI/CD pipelines
│   │   ├── ci.yml         # Build and validation
│   │   └── updateWebsite.yml  # Production deployment trigger
│   └── pull_request_template.md
│
├── assets/
│   └── css/
│       └── custom.css     # Defensive CSS patterns
│
├── content/               # Markdown documentation
│   ├── Configuring/
│   ├── Getting Started/
│   ├── Hypr Ecosystem/
│   └── ...               # Other categories
│
├── layouts/
│   └── partials/         # Template overrides
│       ├── navbar.html   # Navigation with defensive patterns
│       └── version.html  # Version badge with accessibility
│
├── scripts/              # Python validation tooling
│   ├── validate_config.py    # Configuration validation
│   ├── validate_content.py   # Content quality checks
│   ├── validate_env.py       # Environment setup verification
│   ├── pre-commit-hook.sh    # Git hook template
│   └── README.md             # Tooling documentation
│
├── static/               # Static assets (images, favicons)
│
├── config.toml           # Hugo configuration
├── Makefile              # Development commands
├── CONTRIBUTING.md       # Contribution guidelines
└── README.md             # Project overview
```

---

## Defensive Patterns

### 1. Configuration Validation

**Principle:** Fail fast with clear error messages

**Implementation:**
- Python-based validation before build
- Required field checking (baseURL, title, languageCode)
- Security audit (external link attributes, unsafe HTML)
- Menu structure validation (unique weights, proper ordering)

**Location:** `scripts/validate_config.py`

### 2. Content Quality Assurance

**Principle:** Catch issues early, guide contributors

**Implementation:**
- Link integrity checking (internal/external)
- Accessibility auditing (alt text, heading hierarchy)
- Code block language specification
- HTTPS enforcement for external links

**Location:** `scripts/validate_content.py`

### 3. Visual Robustness

**Principle:** Graceful degradation under all conditions

**Implementation:**
- Text overflow protection (truncation, line clamping)
- Responsive breakpoints for all screen sizes
- Print stylesheet optimization
- High contrast and reduced motion support

**Location:** `assets/css/custom.css`

### 4. Accessibility

**Principle:** Universal access for all users

**Implementation:**
- ARIA labels on navigation elements
- Semantic HTML5 elements (nav, banner)
- Focus indicators for keyboard navigation
- Screen reader optimizations
- Minimum touch target sizes (44x44px)

**Location:** `layouts/partials/*.html`

### 5. Environment Validation

**Principle:** Catch setup issues before development

**Implementation:**
- Tool availability checking (Hugo, Go, Python, Git)
- Version compatibility validation
- Go module verification
- Git configuration checks

**Location:** `scripts/validate_env.py`

---

## Build Pipeline

### Local Development

```
Developer writes content
    ↓
Runs: make validate (optional but recommended)
    ├── validate-config: Check configuration
    ├── validate-content: Check markdown files
    └── validate-env: Verify tools
    ↓
Runs: make serve
    ↓
Hugo builds and serves at localhost:1313
    ↓
Developer reviews changes
    ↓
Commits and pushes (optional: pre-commit hook runs)
```

### CI Pipeline

```
Push/PR to GitHub
    ↓
Checkout code
    ↓
Job: Validate
    ├── Setup Python
    ├── Run: validate_config.py
    └── Run: validate_content.py
    ↓
Job: Build (if validation passes)
    ├── Setup Go
    ├── Setup Hugo Extended
    └── Run: hugo --minify --gc --enableGitInfo --panicOnWarning
    ↓
Success: All checks passed
```

### Production Deployment

```
Merge to main branch
    ↓
CI validation and build
    ↓
updateWebsite workflow triggers
    ↓
Repository dispatch to hyprland-wiki-backend
    ↓
Backend rebuilds and deploys to wiki.hypr.land
```

---

## Configuration System

### Hugo Configuration (`config.toml`)

**Key Sections:**

1. **Core Settings**
   ```toml
   baseURL = "https://wiki.hypr.land/"
   title = "Hyprland Wiki"
   enableRobotsTXT = true
   enableGitInfo = true
   ```

2. **Module Imports**
   ```toml
   [module.imports]
   path = "github.com/imfing/hextra"
   ```

3. **Markup Configuration**
   ```toml
   [markup.goldmark.renderer]
   unsafe = true  # Allows HTML in markdown
   ```

4. **Menu Structure**
   ```toml
   [[menu.main]]
   identifier = "version"
   weight = 1
   ```

**Defensive Defaults:**
- All external links use `rel="noreferrer"`
- Git info enabled for debugging
- Robots.txt enabled for SEO control
- Unique menu weights for predictable ordering

---

## Extension Points

### Adding New Validations

1. **Create validator method:**
   ```python
   def _check_new_pattern(self, file_path, content, lines):
       # Implementation
       if issue_found:
           self.issues.append(ContentIssue(...))
   ```

2. **Add to validation flow:**
   ```python
   def validate(self):
       self._check_new_pattern()
   ```

3. **Update documentation:**
   - Add to `scripts/README.md`
   - Document in CONTRIBUTING.md if relevant

### Customizing Templates

1. **Override in `layouts/`:**
   - Create matching directory structure
   - Hugo will use local version over theme

2. **Maintain defensive patterns:**
   - Add ARIA labels where applicable
   - Use semantic HTML
   - Include fallback behavior
   - Test responsive behavior

### Adding CI Checks

1. **Update `.github/workflows/ci.yml`:**
   ```yaml
   - name: New Check
     run: python3 scripts/new_check.py
   ```

2. **Ensure fast execution:**
   - Target: < 30 seconds per check
   - Parallel execution where possible

---

## Performance Considerations

### Build Time
- **Target:** < 5 seconds for local builds
- **Optimizations:**
  - Go module caching in CI
  - Minimal template complexity
  - Hugo's incremental builds

### Validation Speed
- **Target:** < 10 seconds for all validations
- **Optimizations:**
  - Python stdlib only (no dependency overhead)
  - Single-pass file reading
  - Efficient regex patterns

### Runtime Performance
- **Static output:** No server-side processing
- **Minification:** Enabled in production builds
- **Asset optimization:** Hugo handles automatically

---

## Security Considerations

### Content Security
- **HTML in Markdown:** Enabled but content is trusted (wiki contributors)
- **External Links:** Always use `noreferrer` to prevent referrer leakage
- **HTTPS Enforcement:** Validation warns about HTTP links

### Dependency Security
- **Minimal Dependencies:** Python stdlib only for tooling
- **Go Modules:** Locked versions in go.sum
- **Hugo Theme:** Pinned version via go.mod

### CI Security
- **Permissions:** Read-only for most jobs
- **Secrets:** Repository dispatch token for deployment
- **Validation:** All content validated before merge

---

## Failure Modes and Recovery

### Build Failures
- **Symptom:** Hugo build fails
- **Detection:** CI pipeline fails
- **Recovery:** Fix reported issue, validation helps identify

### Validation Failures
- **Symptom:** Pre-merge validation fails
- **Detection:** CI validation job fails
- **Recovery:** Address reported issues (errors) or warnings

### Deployment Failures
- **Symptom:** Site not updated after merge
- **Detection:** Manual verification at wiki.hypr.land
- **Recovery:** Check updateWebsite workflow, backend deployment

### Content Issues
- **Symptom:** Broken links, missing images
- **Detection:** Content validation script
- **Recovery:** Fix identified files, re-validate

---

## Testing Strategy

### Automated Testing
1. **Configuration Validation:** Every commit
2. **Content Validation:** Every commit
3. **Build Testing:** Every PR
4. **Integration:** Deployment to production

### Manual Testing
1. **Visual Review:** `hugo serve` before committing
2. **Cross-browser:** Verify in multiple browsers
3. **Accessibility:** Screen reader testing for major changes
4. **Mobile:** Test responsive behavior

---

## Maintenance

### Regular Tasks
- **Weekly:** Review validation warnings
- **Monthly:** Update Hugo version if needed
- **Quarterly:** Review and update documentation

### Monitoring
- **Build Status:** GitHub Actions badge
- **Site Availability:** External monitoring (if configured)
- **Content Quality:** Validation reports in CI

---

## Future Enhancements

### Potential Additions
1. **Link Availability Checking:** Network requests to verify external links
2. **Image Optimization:** Automated compression and format conversion
3. **Custom Linting Rules:** Project-specific markdown rules
4. **Performance Monitoring:** Build time tracking and optimization
5. **Visual Regression Testing:** Screenshot comparison for UI changes

### Scalability Considerations
- Current architecture supports 1000+ pages efficiently
- Hugo's parallel processing scales well
- Validation scripts handle large content volumes
- Consider caching strategies for very large sites

---

## Philosophy

This architecture embodies:

1. **Defensive Innovation:** Add robustness without breaking existing functionality
2. **Python-First Tooling:** Lightweight, portable, maintainable validation
3. **Graceful Degradation:** Handle errors without catastrophic failure
4. **Accessibility by Default:** Universal design principles throughout
5. **Developer Experience:** Clear documentation, helpful tooling, fast feedback

The goal is a documentation system that:
- **Just works** for contributors
- **Catches mistakes** before they reach production
- **Guides developers** toward best practices
- **Scales gracefully** as content grows
- **Remains maintainable** over years
