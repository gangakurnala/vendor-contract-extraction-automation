# ADR 006: Use Excel Output Format for Extracted Data

**Status:** Accepted

**Date:** 2026-08-04

**Authors:** Ganga Kurnala

## Context

Extracted contract data must be exported for Maersk users in a format that:
- Works with existing Maersk workflows (Excel, SAP integration)
- Supports multiple contracts and services in single file
- Is easy to review and validate
- Integrates with Maersk's procurement systems
- Doesn't require special software beyond Excel

## Decision

Export extracted data as **Excel workbook (.xlsx)** with two sheets:

1. **Contract Headers Sheet**
   - One row per contract
   - Columns: Contract Number, Vendor Name, Start Date, End Date, Contract Value, Payment Terms, Currency, Contract Type
   - Blue header row with white text

2. **Services & Rates Sheet**
   - One row per service within contracts
   - Columns: Contract Number, Service Name, Description, Unit, Rate, Currency, Minimum Order, Volume Discount, Effective From
   - Links to Contract Headers by contract number

## Consequences

### Positive
- **Universal Compatibility** - Excel runs on every Maersk computer
- **Familiar Format** - Users already know Excel; no training needed
- **Easy Validation** - Visual review of extracted data
- **SAP Integration** - Excel files easily import to SAP procurement module
- **Multi-Contract Support** - Single file contains all extractions from a batch job
- **Formatting** - openpyxl supports colors, bold text, column widths

### Negative
- **Large Files** - Excel files larger than CSV for same data
- **No Streaming** - Must load entire workbook in memory (limits very large batches)
- **Excel Limitations** - 1M rows max per sheet (not a practical limit for contracts)
- **Not API-Friendly** - Excel format suitable for interactive use, not machine consumption

## File Structure Example

```
Constant_Staffing_Extracted.xlsx
├── Sheet: "Contract Headers"
│   └── Columns: Contract Number | Vendor Name | Start Date | End Date | Value | Terms | Currency | Type
│       Row 1:  CONST-001 | Constant Staffing LLC | 2023-09-14 | 2024-09-13 | $250,000 | Net 30 | USD | Staffing
│
└── Sheet: "Services & Rates"
    └── Columns: Contract Number | Service Name | Description | Unit | Rate | Currency | Min Order | Discount | Effective From
        Row 1:  CONST-001 | Warehouse Associate | Temporary staffing | Hour | $18.50 | USD | 160 | Tiered | 2023-09-14
        Row 2:  CONST-001 | Supervisor | Temporary supervisor | Hour | $22.00 | USD | 80 | Tiered | 2023-09-14
```

## Implementation

**Using openpyxl library:**
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
ws = wb.create_sheet("Contract Headers")

# Style header row
header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
header_font = Font(bold=True, color="FFFFFF")

# Add data
ws.append([col1, col2, col3, ...])

wb.save("extracted_contracts.xlsx")
```

## Alternatives Considered

1. **CSV Format** - No formatting; harder to review; requires manual Excel conversion
2. **JSON Format** - Machine-friendly; not suitable for Maersk user base
3. **PDF Report** - Pretty but not editable; hard to integrate with systems
4. **Direct SAP Integration** - Overcomplicated; Excel import is simpler
5. **DOCX Format** - Overkill for tabular data; not suitable for analysis

## Download and Distribution

- Users extract contracts via web app
- System generates .xlsx file
- User downloads via browser (automatic filename: `extraction_<job_id>.xlsx`)
- File stored server-side for 30 days (configurable retention)
- User can re-download from job history

## Future Enhancements

- [ ] Add templates for Maersk-specific contract formats
- [ ] Support exporting to SAP OData directly (Phase 2)
- [ ] Add PDF reports alongside Excel
- [ ] Implement Excel data validation (drop-down fields for contract type, currency)
- [ ] Add pivot tables summarizing vendor spend

## Related Decisions

- [[adr-005-claude-sonnet-integration.md]] - Data to export comes from Claude
- [[adr-007-asynchronous-processing.md]] - File generation is async job
