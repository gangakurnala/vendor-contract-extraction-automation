# Vendor Contract Extraction Automation

Extract services, rates, and contract information from 500+ vendor contracts (PDF & Word) using Claude AI. Automatically consolidate data into Excel format with SAP purchase information records.

## Problem Statement

Organizations receive hundreds of vendor contracts in various formats (PDF, Word). Manual extraction of:
- Vendor names and contract details
- Services offered
- Rates and pricing terms
- Payment terms and validity periods

...is time-consuming, error-prone, and difficult to consolidate into structured data for SAP systems.

## Solution

Automated extraction pipeline using Claude AI that:
1. **Processes** multiple contracts simultaneously
2. **Extracts** structured information intelligently
3. **Consolidates** data into Excel with 2 sheets
4. **Validates** data using Pydantic models
5. **Generates** SAP-ready purchase records

## Project Status

- ✅ Core extraction pipeline built
- ✅ Sample contracts created
- ✅ Test mode operational
- ⏳ API integration ready (awaiting API key)
- ⏳ Production deployment

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/gangakurnala/vendor-contract-extraction-automation.git
cd vendor-contract-extraction-automation

# Install dependencies
pip install -r requirements.txt
```

### Test Mode (No API Key Required)

Test the entire pipeline with mock data:

```bash
python contract_extractor_test.py
```

Output: `extracted_contracts_test.xlsx`

### Production Mode (Requires API Key)

1. **Get API Key:**
   - Visit https://console.anthropic.com/api-keys
   - Create a new API key
   - Copy the key

2. **Set Up Environment:**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env and add your API key
   # ANTHROPIC_API_KEY=your_api_key_here
   ```

3. **Run Extraction:**
   ```bash
   python contract_extractor.py
   ```

Output: `extracted_contracts.xlsx`

## File Structure

```
vendor-contract-extraction-automation/
├── README_DETAILED.md              # This file
├── SETUP_GUIDE.md                  # Detailed setup instructions
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
│
├── contract_extractor.py           # Production extraction script
├── contract_extractor_test.py      # Test mode (no API calls)
├── create_sample_contracts.py      # Sample contract generator
│
├── sample-contracts/               # Test contracts
│   ├── sample_contract_1_techsolutions.docx
│   ├── sample_contract_2_officeworld.docx
│   └── sample_contract_3_globalship.docx
│
└── tests/                          # Unit tests
    ├── test_extraction.py
    ├── test_data_models.py
    └── test_excel_generation.py
```

## Usage Guide

### Basic Usage

```python
from contract_extractor import process_contracts

# Process all contracts in sample-contracts/ folder
process_contracts(
    input_folder="sample-contracts",
    output_file="extracted_contracts.xlsx"
)
```

### Advanced Usage

```python
from contract_extractor import (
    load_contract_text,
    extract_contract_info,
    create_excel_output,
    ContractHeader,
    ServiceDetail
)

# Process single contract
contract_text = load_contract_text("path/to/contract.pdf")
header, services = extract_contract_info(contract_text, "contract.pdf")

# Create custom Excel output
all_headers = [header]
all_services = services
create_excel_output(all_headers, all_services, "custom_output.xlsx")
```

## Data Models

### ContractHeader

Extracted contract-level information:

```python
{
    "contract_number": str,      # Contract reference ID
    "vendor_name": str,           # Vendor/supplier name
    "start_date": str,            # Contract start date
    "end_date": str,              # Contract end date
    "contract_value": str,        # Total contract value
    "payment_terms": str,         # Payment terms (e.g., Net 30)
    "currency": str,              # Currency code
    "contract_type": str          # Service/Supply/Logistics agreement
}
```

### ServiceDetail

Service or product information within a contract:

```python
{
    "contract_number": str,       # Reference to contract
    "service_name": str,          # Service/product name
    "service_description": str,   # Detailed description
    "unit": str,                  # Unit of measurement
    "rate": str,                  # Price/rate
    "currency": str,              # Currency
    "minimum_order": str,         # Minimum order quantity/value
    "volume_discount": str,       # Discount terms
    "effective_from": str         # Effective date
}
```

## Excel Output Format

### Sheet 1: Contract Headers

| Column | Description |
|--------|-------------|
| Contract Number | Unique contract identifier |
| Vendor Name | Supplier/vendor name |
| Start Date | Contract effective start date |
| End Date | Contract expiration date |
| Contract Value | Total contract value |
| Payment Terms | Payment conditions |
| Currency | Currency of contract |
| Contract Type | Type of agreement |

### Sheet 2: Services & Rates

| Column | Description |
|--------|-------------|
| Contract Number | Reference to contract |
| Service Name | Service/product name |
| Description | Detailed service description |
| Unit | Unit of measurement |
| Rate | Cost per unit |
| Currency | Currency |
| Minimum Order | Minimum purchase requirement |
| Volume Discount | Discount structure |
| Effective From | Rate effective date |

## Sample Output

### Example Contract 1: TechSolutions Inc.
- **Contract:** VC-2025-0001
- **Value:** $150,000 USD
- **Services:**
  - Cloud Infrastructure Support: $5,000/month
  - Security Audit & Penetration Testing: $8,000/quarter
  - On-Site Technical Support: $150/hour

### Example Contract 2: OfficeWorld Supplies Ltd.
- **Contract:** VC-2025-0002
- **Value:** $45,000 USD
- **Services:**
  - Premium Printer Paper: $5.50/ream
  - Ballpoint Pens: $12.00/box

### Example Contract 3: GlobalShip Logistics
- **Contract:** VC-2025-0003
- **Value:** $250,000 USD
- **Services:**
  - Domestic Ground Shipping: $0.85/pound
  - International Express Shipping: $2.50/pound
  - Warehouse Storage: $75/pallet/month

## Features

### ✅ Current Features

- **Multi-format Support:** PDF and Word (.docx) contracts
- **AI-Powered Extraction:** Claude AI for intelligent data parsing
- **Structured Output:** Pydantic validation for data consistency
- **Excel Generation:** Formatted 2-sheet workbooks
- **Test Mode:** Full pipeline testing without API calls
- **Sample Data:** 3 realistic vendor contracts included
- **Error Handling:** Graceful failure with informative messages

### 🚀 Planned Features

- Direct SAP integration
- Duplicate contract detection
- Contract comparison and change tracking
- Scheduled batch processing
- Web dashboard for monitoring
- Audit trail and logging
- Multi-language support

## Configuration

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx

# Optional (defaults shown)
INPUT_FOLDER=sample-contracts
OUTPUT_FILE=extracted_contracts.xlsx
LOG_LEVEL=INFO
```

### Adjusting Extraction Behavior

Edit `contract_extractor.py`:

```python
# Change extraction prompt
extraction_prompt = f"""
... customize the prompt ...
"""

# Change model
response = client.messages.create(
    model="claude-opus-5",  # Change to different model
    max_tokens=2048,        # Adjust token limit
    ...
)
```

## Running Tests

```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_extraction.py -v

# Run with coverage
pytest tests/ --cov=contract_extractor
```

## Troubleshooting

### Issue: "No module named 'docx'"

```bash
pip install python-docx
```

### Issue: "ANTHROPIC_API_KEY not found"

1. Create `.env` file in project root
2. Add: `ANTHROPIC_API_KEY=your_key_here`
3. Restart your IDE/terminal

### Issue: "Cannot extract text from PDF"

- Check PDF is not encrypted
- Try `pypdf` installation: `pip install --upgrade pypdf`
- Some scanned PDFs may need OCR (not supported by default)

### Issue: "Empty Excel output"

- Verify contracts are in `sample-contracts/` folder
- Check contract format (must be .pdf or .docx)
- Run in test mode first: `python contract_extractor_test.py`

## Performance Notes

- **Processing Speed:** ~30-60 seconds per contract (depends on length and API)
- **Token Usage:** ~1,000-3,000 tokens per contract
- **Memory:** ~100MB for typical batch
- **Batch Processing:** Can process multiple contracts sequentially

## Security Considerations

- ✅ **API Key:** Store securely in `.env` (never commit)
- ✅ **Input Validation:** All data validated with Pydantic
- ✅ **Error Messages:** Don't expose sensitive details
- ✅ **File Access:** Only read from specified folder

### Before Production:

- [ ] Add authentication for file uploads
- [ ] Encrypt stored API keys
- [ ] Implement audit logging
- [ ] Add rate limiting
- [ ] Validate file types and sizes
- [ ] Scan files for malware

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open Pull Request

## Support

For issues or questions:
1. Check SETUP_GUIDE.md for detailed instructions
2. Review sample contracts for format examples
3. Run tests to verify setup
4. Check API key validity

## License

Internal project - Not for external distribution

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | Aug 2026 | Initial release with test mode |
| 0.2.0 | TBD | Production API integration |
| 0.3.0 | TBD | SAP integration |
| 1.0.0 | TBD | First stable release |

---

**Ready to start?** See [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step instructions.
