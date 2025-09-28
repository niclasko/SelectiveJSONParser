# PyPI Release Guide for SelectiveJSONParser

## Prerequisites ✅
- [x] Package built successfully
- [x] All tests pass
- [x] Package structure is correct
- [x] `pyproject.toml` is properly configured

## Step 1: Create PyPI Account (if you don't have one)
1. Go to https://pypi.org/account/register/
2. Create an account with a strong password
3. Verify your email address

## Step 2: Create Test PyPI Account (Recommended)
1. Go to https://test.pypi.org/account/register/
2. Create an account (can use same credentials as main PyPI)
3. This allows you to test uploads safely

## Step 3: Set up API Tokens (Recommended over username/password)

### For TestPyPI:
1. Go to https://test.pypi.org/manage/account/#api-tokens
2. Create a new token with scope: "Entire account"
3. Copy the token (starts with `pypi-`)

### For PyPI:
1. Go to https://pypi.org/manage/account/#api-tokens
2. Create a new token with scope: "Entire account" 
3. Copy the token (starts with `pypi-`)

## Step 4: Configure credentials (choose one method)

### Method A: Using .pypirc file
Create `~/.pypirc` (or `%USERPROFILE%\.pypirc` on Windows):
```ini
[distutils]
index-servers = 
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

### Method B: Environment variables
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-YOUR_TOKEN_HERE"
```

## Step 5: Upload to Test PyPI (RECOMMENDED FIRST!)
```powershell
python -m twine upload --repository testpypi dist/*
```

Test the installation from TestPyPI:
```powershell
pip install --index-url https://test.pypi.org/simple/ selective-json-parser
```

## Step 6: Upload to Production PyPI
⚠️ **ONLY do this after testing on TestPyPI!**

```powershell
python -m twine upload dist/*
```

## Step 7: Verify Installation
```powershell
pip install selective-json-parser
```

Test that it works:
```python
from selectivejsonparser import parse, Parser
result = parse('{"name": "test", "value": 42}')
print(result)  # Should print: {'name': 'test', 'value': 42}
```

## Step 8: Post-Release Tasks
1. **Tag the release in Git:**
   ```powershell
   git tag -a v0.0.1 -m "Release version 0.0.1"
   git push origin v0.0.1
   ```

2. **Create GitHub Release:**
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Choose the tag v0.0.1
   - Add release notes describing features

3. **Update README badges** (optional):
   Add PyPI badges to your README.md:
   ```markdown
   [![PyPI version](https://badge.fury.io/py/selective-json-parser.svg)](https://badge.fury.io/py/selective-json-parser)
   [![Downloads](https://pepy.tech/badge/selective-json-parser)](https://pepy.tech/project/selective-json-parser)
   ```

## For Future Releases:
1. Update version in `pyproject.toml`
2. Update `__version__` in `src/selectivejsonparser/__init__.py`
3. Run tests: `python -m pytest tests/`
4. Build: `python -m build`
5. Check: `python -m twine check dist/*`
6. Upload to TestPyPI first, then PyPI

## Package Information:
- **Package Name:** `selective-json-parser`
- **Import Name:** `selectivejsonparser`
- **Current Version:** 0.0.1
- **Python Requirements:** >=3.11

## Installation Command:
```bash
pip install selective-json-parser
```

## Basic Usage:
```python
# Simple usage
from selectivejsonparser import parse
result = parse('{"name": "John", "age": 30}')

# Selective parsing
result = parse('{"name": "John", "age": 30, "city": "NYC"}', pattern="name")

# Advanced usage
from selectivejsonparser import Parser, Pattern
parser = Parser('{"data": {"users": [{"name": "John"}]}}', "data.users[0].name")
result = parser.parse()
```

---
**Note:** Remember to never commit API tokens to version control!