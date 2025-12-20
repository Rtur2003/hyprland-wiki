# Troubleshooting Guide

This guide helps you resolve common issues when working with the Hyprland Wiki.

## Table of Contents

- [Development Environment](#development-environment)
- [Build Issues](#build-issues)
- [Validation Errors](#validation-errors)
- [Content Problems](#content-problems)
- [CI/CD Issues](#cicd-issues)
- [Git Workflow](#git-workflow)

---

## Development Environment

### Hugo Not Found

**Problem:** `bash: hugo: command not found`

**Solution:**
1. Install Hugo Extended:
   - **macOS:** `brew install hugo`
   - **Linux:** Download from [Hugo releases](https://github.com/gohugoio/hugo/releases)
   - **Windows:** `choco install hugo-extended` or `scoop install hugo-extended`

2. Verify installation:
   ```bash
   hugo version
   # Should show "hugo v0.xxx.x+extended"
   ```

3. **Important:** Hugo Extended is required (not regular Hugo)

### Python Version Issues

**Problem:** `python3: command not found` or version too old

**Solution:**
1. Check Python version:
   ```bash
   python3 --version
   # Need 3.7 or higher
   ```

2. Install/upgrade Python:
   - **macOS:** `brew install python3`
   - **Linux:** `sudo apt install python3` (Ubuntu/Debian)
   - **Windows:** Download from [python.org](https://www.python.org/downloads/)

### Go Module Errors

**Problem:** `go: cannot find module` or `go.sum` issues

**Solution:**
1. Verify Go installation:
   ```bash
   go version
   # Need 1.22 or higher
   ```

2. Update modules:
   ```bash
   hugo mod get -u
   hugo mod tidy
   ```

3. Clean and rebuild:
   ```bash
   hugo mod clean
   hugo mod get
   ```

---

## Build Issues

### Build Fails with "panicOnWarning"

**Problem:** Build stops with warnings treated as errors

**Symptoms:**
```
Error: failed to build pages: /content/page.md:10:1: ...
```

**Solution:**
1. Read the error message carefully - it tells you exactly what's wrong
2. Common causes:
   - Invalid frontmatter syntax
   - Broken internal links
   - Invalid shortcodes
   - Missing required fields

3. Fix the reported issue and rebuild

### Template Execution Errors

**Problem:** `execute of template failed` errors

**Solution:**
1. Check for missing or misspelled template variables
2. Verify frontmatter has all required fields
3. Ensure template syntax is correct in custom partials
4. Test with a minimal example to isolate the issue

### Module Download Failures

**Problem:** Can't download theme module

**Solution:**
1. Check internet connection
2. Verify Go is installed: `go version`
3. Clear module cache:
   ```bash
   hugo mod clean
   rm -rf $HOME/go/pkg/mod/github.com/imfing
   hugo mod get
   ```

---

## Validation Errors

### Configuration Validation Fails

**Problem:** `validate_config.py` reports errors

**Common Issues:**

1. **Missing required field:**
   ```
   ❌ Missing required field 'baseURL'
   ```
   **Fix:** Add the field to `config.toml`:
   ```toml
   baseURL = "https://wiki.hypr.land/"
   ```

2. **Duplicate menu weights:**
   ```
   ⚠️  Duplicate menu weights found
   ```
   **Fix:** Ensure each menu item has a unique weight:
   ```toml
   [[menu.main]]
   weight = 1  # Must be unique
   ```

### Content Validation Warnings

**Problem:** `validate_content.py` reports issues

**Common Issues:**

1. **Image without alt text:**
   ```
   ⚠️  Image without alt text
   ```
   **Fix:** Add descriptive alt text:
   ```markdown
   ✅ ![Screenshot showing three workspaces](image.png)
   ❌ ![](image.png)
   ```

2. **Non-HTTPS link:**
   ```
   ⚠️  Non-HTTPS link found
   ```
   **Fix:** Use HTTPS when possible:
   ```markdown
   ✅ [Example](https://example.com)
   ❌ [Example](http://example.com)
   ```

3. **Code block without language:**
   ```
   ℹ️  Code block without language specification
   ```
   **Fix:** Specify the language:
   ````markdown
   ✅ ```bash
      command here
      ```
   
   ❌ ```
      command here
      ```
   ````

---

## Content Problems

### Links Not Working

**Problem:** Internal links return 404

**Solution:**
1. Use absolute paths from content root:
   ```markdown
   ✅ [Page](/Configuring/Windows/)
   ❌ [Page](Windows/)
   ```

2. Check file names match exactly (case-sensitive on Linux)

3. Verify file has `_index.md` if it's a directory

### Images Not Displaying

**Problem:** Images show broken icon

**Solution:**
1. Place images in `static/` directory
2. Reference from root:
   ```markdown
   ✅ ![Alt text](/images/screenshot.png)
   ❌ ![Alt text](screenshot.png)
   ```

3. Verify file exists and path is correct
4. Check file permissions (should be readable)

### Frontmatter Errors

**Problem:** Page doesn't render correctly

**Solution:**
1. Verify YAML syntax:
   ```yaml
   ---
   title: "Page Title"  # Quotes for strings with special chars
   weight: 10           # Numbers don't need quotes
   ---
   ```

2. Check for common mistakes:
   - Tabs instead of spaces (use spaces)
   - Missing closing `---`
   - Incorrect indentation
   - Special characters not quoted

### Markdown Rendering Issues

**Problem:** Markdown doesn't render as expected

**Solution:**
1. Check for conflicts with Hugo shortcodes
2. Use HTML if markdown doesn't work:
   ```html
   <div class="custom-class">
     Content here
   </div>
   ```

3. For literal curly braces, escape them:
   ```markdown
   Use \{\{ instead of {{
   ```

---

## CI/CD Issues

### CI Build Failing

**Problem:** GitHub Actions build fails

**Investigation Steps:**
1. Click "Details" next to failed check
2. Review the error message in logs
3. Common causes:
   - Validation errors
   - Build errors (same as local)
   - Missing dependencies

**Solution:**
1. Run locally first:
   ```bash
   make validate
   make build
   ```

2. Fix any errors found
3. Push again after confirming local build succeeds

### Validation Job Fails

**Problem:** Validation step fails in CI

**Solution:**
1. Run validation locally:
   ```bash
   python3 scripts/validate_config.py
   python3 scripts/validate_content.py
   ```

2. Fix reported errors
3. Re-run validation to confirm
4. Push changes

### Deployment Not Updating

**Problem:** Site doesn't update after merge to main

**Possible Causes:**
1. Backend deployment issue (not in this repo)
2. Cache not cleared
3. Webhook not triggered

**Solution:**
1. Wait 5-10 minutes (deployment takes time)
2. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
3. Check if commit reached main branch
4. Contact maintainers if issue persists

---

## Git Workflow

### Merge Conflicts

**Problem:** Git reports conflicts when pulling/merging

**Solution:**
1. Understand the conflict:
   ```bash
   git status  # Shows conflicting files
   ```

2. Open conflicting files and look for:
   ```
   <<<<<<< HEAD
   Your changes
   =======
   Incoming changes
   >>>>>>> branch-name
   ```

3. Manually resolve by choosing correct version
4. Remove conflict markers
5. Test that everything works
6. Complete merge:
   ```bash
   git add .
   git commit -m "Resolve merge conflict"
   ```

### Accidentally Committed Wrong Files

**Problem:** Committed files that shouldn't be tracked

**Solution:**
1. Remove from Git but keep locally:
   ```bash
   git rm --cached path/to/file
   ```

2. Add to `.gitignore`:
   ```bash
   echo "path/to/file" >> .gitignore
   ```

3. Commit the change:
   ```bash
   git add .gitignore
   git commit -m "Remove accidentally tracked file"
   ```

### Need to Undo Last Commit

**Problem:** Last commit was wrong

**Solution:**
1. **If not pushed yet:**
   ```bash
   git reset --soft HEAD~1  # Keep changes
   # or
   git reset --hard HEAD~1  # Discard changes (careful!)
   ```

2. **If already pushed:**
   ```bash
   git revert HEAD  # Creates new commit that undoes changes
   git push
   ```

### Lost Changes

**Problem:** Made changes but they disappeared

**Solution:**
1. Check if changes were staged:
   ```bash
   git status
   ```

2. Check stash:
   ```bash
   git stash list
   git stash show  # View latest stash
   git stash pop   # Restore changes
   ```

3. Check reflog for lost commits:
   ```bash
   git reflog
   git checkout <commit-hash>
   ```

---

## Getting More Help

### Before Asking for Help

1. **Search existing issues:** Someone may have had the same problem
2. **Check documentation:**
   - [CONTRIBUTING.md](./CONTRIBUTING.md)
   - [ARCHITECTURE.md](./ARCHITECTURE.md)
   - [scripts/README.md](./scripts/README.md)
3. **Run validation:** May reveal the problem
   ```bash
   make validate
   ```

### When Asking for Help

Include this information:

1. **What you tried:**
   - Command you ran
   - Steps to reproduce

2. **What happened:**
   - Full error message
   - Screenshots if UI-related

3. **Your environment:**
   ```bash
   python3 scripts/validate_env.py
   ```

4. **What you expected:**
   - Describe the intended behavior

### Where to Ask

- **GitHub Issues:** For bugs and feature requests
- **GitHub Discussions:** For questions and general help
- **Pull Request Comments:** For code review questions

---

## Quick Reference

### Common Commands

```bash
# Validation
make validate              # All checks
make validate-config       # Config only
make validate-content      # Content only
make validate-env          # Environment only

# Development
make serve                 # Start dev server
make build                 # Build site
make clean                 # Clean generated files

# Git
git status                 # Check what changed
git diff                   # See changes
git add .                  # Stage changes
git commit -m "message"    # Commit changes
git push                   # Push to GitHub
```

### Useful Hugo Commands

```bash
hugo serve                     # Dev server
hugo serve --disableFastRender # Full rebuild on change
hugo --minify                  # Production build
hugo mod clean                 # Clean module cache
hugo mod get -u                # Update modules
```

---

## Prevention Tips

### Before Making Changes

1. ✅ Pull latest changes: `git pull`
2. ✅ Run validation: `make validate`
3. ✅ Start dev server: `make serve`
4. ✅ Create feature branch (for large changes)

### While Working

1. ✅ Save and check browser frequently
2. ✅ Commit small, logical changes
3. ✅ Write clear commit messages
4. ✅ Test links and images

### Before Pushing

1. ✅ Run validation: `make validate`
2. ✅ Build locally: `make build`
3. ✅ Review changes: `git diff`
4. ✅ Read your own code/content

---

## Emergency Procedures

### Broke the Site (Deployed to Main)

**Immediate Action:**
1. Don't panic
2. Revert the breaking commit:
   ```bash
   git revert <commit-hash>
   git push
   ```
3. Wait for deployment (5-10 minutes)
4. Fix issue properly in new PR

### Can't Build Locally

**Recovery:**
1. Try clean rebuild:
   ```bash
   make clean
   hugo mod clean
   hugo mod get
   make build
   ```

2. If still broken, try fresh clone:
   ```bash
   cd ..
   git clone <repo-url> hyprland-wiki-fresh
   cd hyprland-wiki-fresh
   hugo mod get
   make serve
   ```

### Lost All Local Changes

**Recovery:**
1. Check Git:
   ```bash
   git status
   git stash list
   git reflog
   ```

2. If nothing found, check your editor's auto-save/recovery feature

3. Prevention: Commit frequently!

---

Remember: Most problems have simple solutions. Read error messages carefully - they usually tell you exactly what's wrong!
