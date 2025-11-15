# GitHub Upload Guide for AUX-QHE

**Paper:** "Experimental Validation of AUX scheme for Quantum Homomorphic Encryption on IBM Quantum Platforms"
**Conference:** QCNC 2026
**Status:** Ready to upload

---

## ✅ Pre-Upload Checklist

✅ Git initialized
✅ .gitignore created (protects sensitive data)
✅ README_GITHUB.md created (GitHub-friendly README)
✅ Repository organized (127 files)
✅ Latest results included

---

## 🚀 Step-by-Step Upload Instructions

### Step 1: Create GitHub Repository

1. Go to https://github.com
2. Click "New" repository or go to https://github.com/new
3. Fill in repository details:
   - **Repository name:** `AUX-QHE` (or `aux-qhe-qcnc-2026`)
   - **Description:** "Experimental Validation of AUX-QHE on IBM Quantum - QCNC 2026"
   - **Visibility:**
     - ✅ **Public** (recommended for published research)
     - OR **Private** (if you want to keep it private until paper acceptance)
   - **Initialize:** Leave UNCHECKED (we already initialized locally)
   - Click "Create repository"

### Step 2: Configure Git (One-time setup)

```bash
# Set your name and email (if not already set)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global user.name
git config --global user.email
```

### Step 3: Add Files to Git

```bash
cd /Users/giadang/my_qiskitenv/AUX-QHE

# Check what will be added
git status

# Add all files (respecting .gitignore)
git add .

# Verify what's staged
git status
```

**Expected output:** Should show files to be committed, excluding:
- `__pycache__/`
- `.vscode/`
- Large interim JSON files
- CSV files (too large)
- Credentials

### Step 4: Create Initial Commit

```bash
# Create commit with descriptive message
git commit -m "$(cat <<'EOF'
Initial commit: AUX-QHE implementation for QCNC 2026

- Complete AUX-QHE protocol implementation
- IBM Quantum hardware validation (ibm_torino)
- 4 error mitigation strategies (Baseline, ZNE, Opt-3, Opt-3+ZNE)
- Test configurations: 5q-2t, 4q-3t, 5q-3t
- Comprehensive testing suite
- Results analysis and table generation tools
- QOTP decryption bug fix (bit-ordering)
- Hardware results: 37.82% fidelity (5q-2t, Opt-3+ZNE)

Paper: "Experimental Validation of AUX scheme for Quantum Homomorphic
Encryption on IBM Quantum Platforms" - Submitted to QCNC 2026

🤖 Generated with Claude Code
EOF
)"
```

### Step 5: Connect to GitHub Repository

```bash
# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/AUX-QHE.git

# Verify remote
git remote -v
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

### Step 6: Push to GitHub

```bash
# Push to GitHub (main branch)
git push -u origin main

# If you get an error about 'master' vs 'main', use:
git branch -M main
git push -u origin main
```

**You may need to authenticate:**
- **Option 1:** GitHub Personal Access Token (recommended)
  - Go to GitHub → Settings → Developer settings → Personal access tokens
  - Generate new token with `repo` permissions
  - Use token as password when prompted

- **Option 2:** SSH key
  - Set up SSH key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Step 7: Verify Upload

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/AUX-QHE`
2. You should see:
   - ✅ All folders (core/, results/, 05_Results_Analysis/, etc.)
   - ✅ Main scripts (ibm_hardware_noise_experiment.py, test_hardware_script_local.py)
   - ✅ README.md
   - ✅ Latest results table

---

## 📝 After Upload: Update README

Replace the placeholder README with GitHub version:

```bash
# Backup current README
cp README.md README_LOCAL.md

# Use GitHub README
cp README_GITHUB.md README.md

# Commit the change
git add README.md
git commit -m "docs: Update README for GitHub visibility"
git push
```

---

## 🔒 Important Security Notes

### ✅ What's Protected by .gitignore

- IBM credentials (never uploaded)
- API keys
- Virtual environment files
- Large interim result files
- System files (__pycache__, .DS_Store)

### ⚠️ Before Pushing, Verify No Secrets

```bash
# Search for potential credentials
grep -r "token" . --include="*.py" --include="*.md" --exclude-dir=".git"
grep -r "api_key" . --include="*.py" --include="*.md" --exclude-dir=".git"
grep -r "password" . --include="*.py" --include="*.md" --exclude-dir=".git"
```

If you find any hardcoded credentials, remove them and use environment variables instead.

---

## 📊 What Gets Uploaded

### ✅ Included (Essential Research Code)

- Core algorithm (`core/`)
- Main scripts (`ibm_hardware_noise_experiment.py`, `test_hardware_script_local.py`)
- Testing suite (`06_Testing_Scripts/`)
- Analysis tools (`05_Results_Analysis/`)
- Documentation (`README.md`, `QUICK_START.md`, guides)
- **Latest results** (`results/hardware_2025_10_30/` - JSON files only)
- Papers folder (notebooks, LaTeX tables)

### ❌ Excluded (by .gitignore)

- Virtual environment (`my_qiskitenv/`)
- Python cache (`__pycache__/`)
- Large CSV files (500KB+ each)
- Interim autosave files (36 JSON files)
- Debug output
- System files (`.DS_Store`)
- VSCode workspace

**Total Upload Size:** ~5-10 MB (manageable)

---

## 🎯 Repository Best Practices

### Add GitHub Actions (Optional)

Create `.github/workflows/test.yml` for automated testing:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install qiskit qiskit-ibm-runtime numpy pandas
      - name: Run tests
        run: |
          python -m pytest 06_Testing_Scripts/
```

### Add LICENSE

```bash
# Add MIT License (example)
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy...
EOF

git add LICENSE
git commit -m "docs: Add MIT License"
git push
```

### Add CITATION.cff

```bash
# Create citation file
cat > CITATION.cff << 'EOF'
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Your Last Name"
    given-names: "Your First Name"
title: "AUX-QHE: Auxiliary Quantum Homomorphic Encryption"
version: 1.0.0
date-released: 2025-11-15
url: "https://github.com/YOUR_USERNAME/AUX-QHE"
EOF

git add CITATION.cff
git commit -m "docs: Add citation file"
git push
```

---

## 🔄 Future Updates

### To Update Repository After Changes

```bash
# Make your changes to files

# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

### To Add New Results

```bash
# Add new result files
git add results/hardware_2025_11_15/

# Commit
git commit -m "results: Add November 2025 hardware experiments"

# Push
git push
```

---

## 📧 Share Repository

After uploading, you can share:

**Repository URL:** `https://github.com/YOUR_USERNAME/AUX-QHE`

**Include in Paper:**
```
Code Availability: The complete implementation is available at
https://github.com/YOUR_USERNAME/AUX-QHE
```

**Include in Presentation:**
- Add GitHub link to slides
- Add QR code to poster

---

## 🎉 Ready to Upload!

Follow these commands in order:

```bash
# 1. Navigate to directory
cd /Users/giadang/my_qiskitenv/AUX-QHE

# 2. Configure git (one-time)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 3. Add files
git add .

# 4. Create commit
git commit -m "Initial commit: AUX-QHE for QCNC 2026"

# 5. Create GitHub repo at https://github.com/new

# 6. Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/AUX-QHE.git

# 7. Push to GitHub
git branch -M main
git push -u origin main
```

---

## ❓ Troubleshooting

### "Permission denied" Error
- You need to set up authentication (Personal Access Token or SSH)
- See: https://docs.github.com/en/authentication

### "Repository too large" Error
- Check file sizes: `du -sh results/`
- Verify .gitignore is working: `git status`
- Large files should be excluded

### "Nothing to commit" Message
- Files might be in .gitignore
- Check: `git status --ignored`

---

## ✅ Post-Upload Checklist

After successful upload:

1. ✅ Verify repository is visible on GitHub
2. ✅ Check README displays correctly
3. ✅ Verify code is accessible
4. ✅ Test clone: `git clone https://github.com/YOUR_USERNAME/AUX-QHE.git`
5. ✅ Add repository link to paper
6. ✅ Update paper with "Code availability" section

---

**Good luck with your QCNC 2026 submission! 🚀**
