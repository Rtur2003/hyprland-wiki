# Contributing to Hyprland Wiki

Thank you for contributing to the Hyprland Wiki! This guide will help you make high-quality contributions that follow our standards.

## Quick Start

1. **Fork and clone** the repository
2. **Install dependencies** (Go, Hugo Extended)
3. **Run validation** to ensure your environment is ready
4. **Make changes** following our guidelines
5. **Test locally** before submitting
6. **Create a pull request** with a clear description

---

## Development Environment

### Required Tools

- **Go** 1.22 or higher
- **Hugo Extended** (latest version)
- **Python** 3.7+ (for validation scripts)
- **Git** (for version control)

### Setup Validation

Check your environment is ready:

```bash
python3 scripts/validate_env.py
```

This will verify all required tools are installed and properly configured.

---

## Making Changes

### Content Guidelines

#### File Organization
- Place content in appropriate directories under `content/`
- Use meaningful file names (lowercase, hyphens for spaces)
- Include frontmatter in all markdown files

#### Markdown Best Practices

**Frontmatter** (required for most pages):
```yaml
---
title: "Page Title"
weight: 1
---
```

**Headings** - Use proper hierarchy:
```markdown
# Page Title (H1 - only one per page)

## Main Section (H2)

### Subsection (H3)

Don't skip levels (e.g., H1 → H3)
```

**Links** - Always include descriptive text:
```markdown
✅ Good: [Hugo documentation](https://gohugo.io/)
❌ Bad: [click here](https://gohugo.io/)
```

**Images** - Always include alt text:
```markdown
✅ Good: ![Hyprland desktop showing multiple workspaces](image.png)
❌ Bad: ![](image.png)
```

**Code Blocks** - Specify language for syntax highlighting:
````markdown
✅ Good:
```bash
hugo serve
```

❌ Bad:
```
hugo serve
```
````

---

### Commit Guidelines

Format: `Dir/Page: summary of changes`

Examples:
```
Configuring/Window-Rules: update animation examples
FAQ: add troubleshooting for Nvidia issues
Getting Started: clarify installation steps
```

**Commit Message Best Practices:**
- Use present tense ("add" not "added")
- Keep summary under 72 characters
- Add detailed description if needed (2 lines below summary)
- One logical change per commit

**For multiple changes in same PR:**
Squash related commits into self-contained logical units. See [this guide](https://stackoverflow.com/a/5189600) for how to squash commits.

---

## Local Development

### Start Development Server

```bash
# Using Makefile (recommended)
make serve

# Or directly with Hugo
hugo serve
```

Then open http://localhost:1313 to see your changes live.

### Validation

Before submitting a PR, run all validations:

```bash
# All checks
make validate

# Individual checks
make validate-config    # Check configuration
make validate-content   # Check markdown files
make validate-env       # Check development setup
```

---

## Quality Standards

### Accessibility

- Use semantic HTML when needed
- Include alt text for all images
- Maintain proper heading hierarchy
- Ensure sufficient color contrast
- Use descriptive link text

### Content Quality

- Write clear, concise documentation
- Use examples where helpful
- Keep information up-to-date
- Link to related documentation
- Use proper grammar and spelling

### Technical Standards

- Follow existing file structure
- Maintain consistent formatting
- Use HTTPS links when possible
- Test all internal links
- Ensure code examples work

---

## Pull Request Process

### Before Submitting

1. **Run validation**:
   ```bash
   make validate
   ```

2. **Test locally**:
   ```bash
   hugo serve
   # Verify your changes at http://localhost:1313
   ```

3. **Review your changes**:
   ```bash
   git diff
   ```

### PR Description

Include:
- **What** changed
- **Why** you made the change
- **How** to test/verify
- Screenshots (if UI changes)

### PR Checklist

- [ ] Changes follow commit message format
- [ ] All validation checks pass
- [ ] Tested locally with `hugo serve`
- [ ] Documentation updated (if needed)
- [ ] Links tested and working
- [ ] Images include alt text
- [ ] Code blocks have language specified

---

## Common Tasks

### Adding a New Page

1. Create markdown file in appropriate directory:
   ```bash
   touch content/Category/new-page.md
   ```

2. Add frontmatter:
   ```markdown
   ---
   title: "New Page Title"
   weight: 10
   ---
   
   Your content here...
   ```

3. Test locally:
   ```bash
   make serve
   ```

### Updating Existing Content

1. Find and edit the relevant file
2. Maintain existing formatting style
3. Run validation to check for issues
4. Test changes locally

### Adding Images

1. Place images in `static/` directory
2. Reference in markdown:
   ```markdown
   ![Descriptive alt text](/path/to/image.png)
   ```

3. Optimize images before adding:
   - Use appropriate format (PNG for screenshots, JPEG for photos)
   - Compress to reasonable size
   - Consider max width of 1200px

---

## Defensive Patterns

This wiki implements defensive patterns to ensure robustness:

### Text Overflow
Long content is handled gracefully:
- Links break properly
- Code blocks scroll horizontally
- Navigation truncates safely

### Accessibility
Built-in support for:
- Screen readers (ARIA labels)
- Keyboard navigation
- High contrast mode
- Reduced motion preferences

### Responsive Design
Works on all screen sizes:
- Mobile-first approach
- Touch targets meet minimum size (44x44px)
- Content adapts to viewport

---

## Getting Help

- **Issues**: Check existing issues or open a new one
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: See `scripts/README.md` for tooling details

---

## Philosophy

We aim for documentation that is:
- **Accurate**: Information is correct and up-to-date
- **Accessible**: Everyone can use and understand it
- **Maintainable**: Easy to update and improve
- **Resilient**: Works under various conditions
- **User-Friendly**: Clear, helpful, and well-organized

Thank you for helping make the Hyprland Wiki better! 🎉
