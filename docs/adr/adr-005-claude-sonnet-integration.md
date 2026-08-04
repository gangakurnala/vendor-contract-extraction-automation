# ADR 005: Use Claude Sonnet 5.0 for Contract Extraction (with Regex Fallback)

**Status:** Accepted

**Date:** 2026-08-04

**Authors:** Ganga Kurnala

## Context

Contract extraction requires intelligent understanding of:
- Complex PDF layouts with forms, tables, attachments
- Unstructured text in different languages
- Context-dependent values (e.g., "Payment terms: Net 30" vs form fields)
- Service rates and volume discounts with various formats

Initial regex-based extraction worked for simple, structured contracts but failed on complex real-world Maersk vendor contracts (e.g., Constant Staffing Agreement with forms and attachments).

## Decision

Use **Claude Sonnet 5.0 API** for intelligent extraction, with **regex fallback** when API is unavailable.

### Hybrid Approach

1. **Primary:** Claude Sonnet 5.0 extracts from contract text (first 5000 chars)
   - Returns JSON with contract headers and services
   - Handles complex layouts, forms, attachments
   - Accurate vendor names, dates, values, terms

2. **Fallback:** Smart regex extraction when API unavailable
   - Pattern matching for contract numbers, dates, values
   - Returns partial data (graceful degradation)
   - Works without API key (development mode)

### Configuration

```python
# .env.web
ANTHROPIC_API_KEY=sk-ant-xxxxx  # API key required for production

# Code
model="claude-sonnet-5"
max_tokens=2048
```

## Consequences

### Positive
- **Accuracy** - Claude understands complex contract structures
- **Resilience** - Works without API key (regex fallback)
- **Cost Effective** - $3-5 per 1000 contracts (reasonable for Maersk)
- **Future Proof** - Can upgrade to Claude 5 or later models
- **Handles Real Contracts** - Solves the "realistic contracts" problem

### Negative
- **API Dependency** - Requires Anthropic API credentials and network
- **Billing Required** - Needs credits in Anthropic account
- **SSL Certificate Issues** - Corporate environments may require cert configuration
- **Token Consumption** - Each contract costs API tokens (~1000-3000 per contract)
- **Latency** - ~30-60 seconds per contract (network dependent)

## Extraction Prompt

```python
extraction_prompt = """
Analyze this vendor contract and extract:
{
    "contract_header": {
        "contract_number": "",
        "vendor_name": "",
        "start_date": "",
        "end_date": "",
        "contract_value": "",
        "payment_terms": "",
        "currency": "",
        "contract_type": ""
    },
    "services": [
        {
            "service_name": "",
            "service_description": "",
            "unit": "",
            "rate": "",
            "currency": "",
            "minimum_order": "",
            "volume_discount": "",
            "effective_from": ""
        }
    ]
}
"""
```

## Fallback Regex Patterns

When Claude is unavailable, extract using patterns:
- Contract Number: `CONTRACT\s*(?:NUMBER|NO\.?|#)\s*[:=\s]*([A-Z0-9\-]+)`
- Vendor Name: `VENDOR\s*[:=]\s*([^\n]+)`
- Dates: `\d{1,2}[-/]\d{1,2}[-/]\d{2,4}`
- Value: `([$€£]\s*[\d,]+(?:\.\d{2})?)`
- Currency: "USD", "EUR", "GBP" (pattern match)

## Limitations

- **Cannot Process:** Scanned PDFs (no OCR); encrypted PDFs
- **Text Extraction Required:** Contracts must have extractable text (not images)
- **First 5000 Chars:** Only analyzes first part of contract (adjustable)
- **No Real-Time:** Batch processing only; not suitable for <1 second responses

## Cost Estimation

- **Per Contract:** ~1,500 tokens = ~$0.005 (Sonnet 5.0 pricing)
- **100 Contracts:** ~$0.50
- **1000 Contracts:** ~$5.00
- **10000 Contracts:** ~$50.00

This is acceptable for Maersk's vendor management use case.

## Future Enhancements

- [ ] Add OCR preprocessing for scanned PDFs
- [ ] Implement caching to avoid re-extraction of identical contracts
- [ ] Add extraction confidence scoring
- [ ] Support multiple contract analysis (full text, not just first 5000 chars)
- [ ] Consider Claude API Batch Processing for cost optimization

## Related Decisions

- [[adr-006-excel-output-format.md]] - Extracted data exported to Excel
- [[adr-007-asynchronous-processing.md]] - Jobs track extraction status
