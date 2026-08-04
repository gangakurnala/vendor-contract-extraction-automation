# Vendor Contract Extraction - Setup Guide

Complete step-by-step guide to set up and run the project.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Test Mode Setup](#test-mode-setup)
4. [Production Setup](#production-setup)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

---

## Prerequisites

### Required Software

- **Python 3.8+** - Download from https://www.python.org/downloads/
- **Git** - Download from https://git-scm.com/
- **Text Editor** - VS Code, Notepad++, or any text editor

### Required Accounts

- **GitHub Account** - For cloning and pushing code (optional if just testing locally)
- **Anthropic API Key** - For production use only (get from https://console.anthropic.com/api-keys)

### Verify Installation

```bash
# Check Python version
python --version
# Should show: Python 3.x.x

# Check Git version
git --version
# Should show: git version x.x.x
```

---

## Installation

### Step 1: Clone the Repository

```bash
# Navigate to your desired directory
cd C:\Users\YourName\Downloads

# Clone the repository
git clone https://github.com/gangakurnala/vendor-contract-extraction-automation.git

# Enter project directory
cd vendor-contract-extraction-automation
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

**macOS/Linux:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install from requirements.txt
pip install -r requirements.txt

# Verify installation
pip list
# Should show: anthropic, python-docx, pypdf, openpyxl, python-dotenv, pydantic
```

---

## Test Mode Setup

Test the entire pipeline WITHOUT needing an API key.

### Step 1: Verify Sample Contracts

```bash
# Check if sample contracts exist
ls sample-contracts/

# You should see:
# - sample_contract_1_techsolutions.docx
# - sample_contract_2_officeworld.docx
# - sample_contract_3_globalship.docx
```

If contracts are missing:

```bash
# Generate them
python create_sample_contracts.py
```

### Step 2: Run Test Mode

```bash
# Execute test script
python contract_extractor_test.py

# You should see output like:
# ============================================================
# CONTRACT EXTRACTION - TEST MODE (No API calls)
# ============================================================
# Found 3 contract(s) to process
# [1/3] Processing: sample_contract_1_techsolutions.docx
# [TEST MODE] Using mock data for sample_contract_1_techsolutions.docx
# ✓ Extracted: VC-2025-0001 - TechSolutions Inc.
#   Services found: 3
# ...
# ✓ Test complete!
#   Total contracts: 3
#   Total services: 8
# 📊 Output file: extracted_contracts_test.xlsx
```

### Step 3: Verify Output

```bash
# Check if Excel file was created
ls extracted_contracts_test.xlsx

# File should be created with test data
```

✅ **Test mode is working!** Proceed to production setup for API-powered extraction.

---

## Production Setup

Production mode uses Claude AI to extract real contract information.

### Step 1: Get API Key

**Option A: Direct Access**
1. Go to https://console.anthropic.com/api-keys
2. Click "Create Key"
3. Copy the API key (starts with `sk-ant-`)
4. **Keep this safe!** Never share or commit it

**Option B: Ask Your Organization**
If you cannot access the console:
1. Contact your IT/Admin team
2. Request an Anthropic API key or organizational access
3. They may need to whitelist the domain or provide proxy access

### Step 2: Create Environment File

```bash
# Copy the example file
cp .env.example .env

# On Windows:
# copy .env.example .env
```

### Step 3: Configure API Key

Edit the `.env` file:

```bash
# Option 1: Use your text editor
# - Open .env in your editor
# - Replace "your_api_key_here" with your actual key
# - Save file

# Option 2: Use command line
# Windows:
echo ANTHROPIC_API_KEY=sk-ant-your-actual-key-here > .env

# macOS/Linux:
echo "ANTHROPIC_API_KEY=sk-ant-your-actual-key-here" > .env
```

### Step 4: Verify Setup

```bash
# Test that Python can read your API key
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key loaded!' if os.getenv('ANTHROPIC_API_KEY') else 'ERROR: API Key not found')"

# You should see: "API Key loaded!"
```

---

## Running the Application

### Test Mode (No API Needed)

```bash
# From project root directory
python contract_extractor_test.py

# Output file: extracted_contracts_test.xlsx
```

### Production Mode (Requires API Key)

```bash
# Ensure .env file is set up first!
python contract_extractor.py

# Output file: extracted_contracts.xlsx
```

### Processing Your Own Contracts

```bash
# 1. Create folder for your contracts
mkdir my-contracts

# 2. Add your PDF or Word files to the folder
# Copy your contract files here:
# my-contracts/vendor1.pdf
# my-contracts/vendor2.docx
# etc.

# 3. Modify contract_extractor.py
# Change the input folder in the main section:
# process_contracts(
#     input_folder="my-contracts",
#     output_file="my_extraction_results.xlsx"
# )

# 4. Run extraction
python contract_extractor.py
```

---

## Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
# Run tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=contract_extractor --cov-report=html

# Run specific test file
pytest tests/test_extraction.py -v

# Run specific test
pytest tests/test_extraction.py::test_load_contract_text -v
```

### Test Output Example

```
tests/test_data_models.py::test_contract_header_model PASSED
tests/test_data_models.py::test_service_detail_model PASSED
tests/test_extraction.py::test_load_contract_text PASSED
tests/test_extraction.py::test_extract_contract_info_mock PASSED
tests/test_excel_generation.py::test_create_excel_output PASSED

======================== 5 passed in 0.42s ========================
```

---

## Troubleshooting

### Python Issues

#### "Python command not found"

**Solution:**
- Add Python to PATH: https://docs.python.org/3/using/windows.html#getting-and-installing-the-latest-version-of-python
- Or use full path: `C:\Python312\python.exe contract_extractor.py`

#### "ModuleNotFoundError: No module named 'docx'"

**Solution:**
```bash
pip install --upgrade python-docx
```

#### Virtual environment not activating

**Solution:**
```bash
# Windows - check if you have execution permission
# Try PowerShell with admin rights
# Or use: python -m venv venv

# macOS/Linux - ensure correct syntax
source venv/bin/activate
```

### API Key Issues

#### "ANTHROPIC_API_KEY not found"

**Solution:**
1. Verify `.env` file exists in project root
2. Check it contains: `ANTHROPIC_API_KEY=sk-ant-xxxxx`
3. Restart your terminal after creating `.env`
4. Verify file is not corrupted

#### "Invalid API Key"

**Solution:**
1. Verify key starts with `sk-ant-`
2. Check no extra spaces or quotes
3. Regenerate key from console if needed
4. Verify key hasn't expired

#### "Rate limit exceeded"

**Solution:**
- Wait before processing more contracts
- Reduce batch size
- Process contracts sequentially

### File Issues

#### "No such file or directory: sample-contracts"

**Solution:**
```bash
# Generate sample contracts
python create_sample_contracts.py

# Or create folder manually
mkdir sample-contracts
```

#### "Cannot extract text from PDF"

**Solution:**
- Verify PDF is not password protected
- Try opening PDF in your reader first
- Some scanned PDFs may not support text extraction
- Update pypdf: `pip install --upgrade pypdf`

#### "Empty Excel file generated"

**Solution:**
1. Check input folder has files
2. Run test mode first: `python contract_extractor_test.py`
3. Verify file formats are .pdf or .docx
4. Check Claude extracted valid data

### Network/Permission Issues

#### "Cannot connect to Anthropic API"

**Solution:**
- Check internet connection
- Verify firewall allows connection to api.anthropic.com
- If behind proxy, configure Python:
  ```bash
  pip install requests[socks]
  # Then set proxy in your script
  ```

#### "Permission denied when accessing file"

**Solution:**
- Close the Excel file if it's open
- Check folder permissions: `ls -l folder_name`
- Run terminal as administrator if needed

### Git Issues

#### "Repository not found"

**Solution:**
```bash
# Verify you're in the right directory
pwd

# Verify git is initialized
git status

# If not a repo, clone it:
git clone https://github.com/gangakurnala/vendor-contract-extraction-automation.git
```

---

## Next Steps

### After Setup is Complete

1. **Run Test Mode**
   ```bash
   python contract_extractor_test.py
   ```
   This verifies your Python and file handling setup.

2. **Get API Key** (if not already done)
   - Visit https://console.anthropic.com/api-keys
   - Create a key
   - Set up `.env` file

3. **Run Production Mode**
   ```bash
   python contract_extractor.py
   ```

4. **Process Your Own Contracts**
   - Copy your contracts to input folder
   - Update script to use your folder
   - Run extraction

5. **Run Unit Tests**
   ```bash
   pytest tests/ -v
   ```

6. **Review Output**
   - Open `extracted_contracts.xlsx`
   - Verify data accuracy
   - Check for missing fields

7. **Customize Extraction** (Optional)
   - Edit extraction prompt in `contract_extractor.py`
   - Adjust for your specific needs
   - Test with small batch first

### Common Workflows

**Workflow 1: One-time Extraction**
```bash
# Copy contracts to sample-contracts/
# Run: python contract_extractor.py
# Get results in extracted_contracts.xlsx
```

**Workflow 2: Batch Processing**
```bash
# Create multiple input folders
# Run extraction on each folder with different output
python contract_extractor.py  # batch1
python contract_extractor_batch2.py  # batch2
# Combine results manually or with script
```

**Workflow 3: Scheduled Daily Processing**
```bash
# Add to system scheduler (Windows Task Scheduler or cron)
# Configure to run daily at specific time
# Results emailed automatically (requires additional setup)
```

---

## Getting Help

### Resources

- **GitHub Issues:** Report bugs at https://github.com/gangakurnala/vendor-contract-extraction-automation/issues
- **Anthropic Docs:** https://docs.anthropic.com/
- **Python Docs:** https://docs.python.org/
- **Project README:** See [README_DETAILED.md](README_DETAILED.md)

### Common Questions

**Q: How much does Claude API cost?**
- A: Check https://www.anthropic.com/pricing for current rates (typically $3-20 per million input tokens)

**Q: Can I use free tier?**
- A: Free tier has limitations. Check Anthropic website for current free tier details.

**Q: How long does extraction take?**
- A: Typically 30-60 seconds per contract depending on length and API load

**Q: Can I process encrypted PDFs?**
- A: No. Decrypt them first using a PDF tool.

**Q: Does it work with scanned documents?**
- A: Not automatically. OCR requires additional setup.

---

## Verification Checklist

Before proceeding to production, verify:

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list` shows required packages)
- [ ] Sample contracts exist in `sample-contracts/` folder
- [ ] Test mode runs successfully (`python contract_extractor_test.py`)
- [ ] `extracted_contracts_test.xlsx` was created
- [ ] `.env` file created with API key (for production)
- [ ] API key verified (test with simple request if possible)
- [ ] Git repository cloned and working
- [ ] Unit tests pass (`pytest tests/ -v`)

✅ **Ready to use!** Start with test mode, then move to production.

---

**Last Updated:** August 2026
**Version:** 1.0
