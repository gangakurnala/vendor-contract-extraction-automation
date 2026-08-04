"""
Unit tests for contract extraction functionality
Tests file reading, text extraction, and data parsing
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from contract_extractor import (
    load_contract_text,
    extract_text_from_docx,
    extract_text_from_pdf,
    ContractHeader,
    ServiceDetail
)


class TestFileLoading:
    """Test file loading functionality"""

    def test_load_contract_text_docx(self):
        """Test loading text from Word document"""
        docx_path = "sample-contracts/sample_contract_1_techsolutions.docx"

        # Skip test if file doesn't exist
        if not Path(docx_path).exists():
            pytest.skip(f"Sample contract not found: {docx_path}")

        text = load_contract_text(docx_path)

        # Verify text was extracted
        assert isinstance(text, str)
        assert len(text) > 0
        # Check for expected content
        assert "TechSolutions" in text or "contract" in text.lower()

    def test_load_contract_text_pdf(self):
        """Test loading text from PDF document"""
        pdf_path = "sample-contracts/sample_contract_test.pdf"

        # This test is conditional - PDF might not exist
        if not Path(pdf_path).exists():
            pytest.skip(f"Sample PDF not found: {pdf_path}")

        text = load_contract_text(pdf_path)
        assert isinstance(text, str)

    def test_load_contract_nonexistent_file(self):
        """Test loading from non-existent file"""
        text = load_contract_text("nonexistent/contract.docx")

        # Should return empty string gracefully
        assert text == ""

    def test_load_contract_unsupported_format(self):
        """Test loading from unsupported file format"""
        text = load_contract_text("file.txt")

        # Should handle unsupported format gracefully
        assert text == ""

    def test_extract_text_from_docx_direct(self):
        """Test direct DOCX extraction"""
        docx_path = "sample-contracts/sample_contract_1_techsolutions.docx"

        if not Path(docx_path).exists():
            pytest.skip(f"Sample contract not found: {docx_path}")

        text = extract_text_from_docx(docx_path)

        assert isinstance(text, str)
        assert len(text) > 0

    def test_extract_text_from_docx_nonexistent(self):
        """Test DOCX extraction with non-existent file"""
        text = extract_text_from_docx("nonexistent.docx")

        # Should return empty string
        assert text == ""

    def test_extract_text_from_pdf_direct(self):
        """Test direct PDF extraction"""
        pdf_path = "sample-contracts/test.pdf"

        if not Path(pdf_path).exists():
            pytest.skip("Test PDF not found")

        text = extract_text_from_pdf(pdf_path)
        assert isinstance(text, str)

    def test_extract_text_from_pdf_nonexistent(self):
        """Test PDF extraction with non-existent file"""
        text = extract_text_from_pdf("nonexistent.pdf")

        # Should return empty string
        assert text == ""

    def test_load_multiple_contracts(self):
        """Test loading multiple contracts"""
        sample_dir = Path("sample-contracts")

        if not sample_dir.exists():
            pytest.skip("Sample contracts directory not found")

        files = list(sample_dir.glob("*.docx")) + list(sample_dir.glob("*.pdf"))

        assert len(files) > 0, "No sample contracts found"

        texts = [load_contract_text(str(f)) for f in files]

        # All should return text
        assert all(isinstance(t, str) for t in texts)
        # At least some should have content
        assert any(len(t) > 0 for t in texts)


class TestDataExtraction:
    """Test data extraction from contracts"""

    def test_contract_header_creation(self):
        """Test creating contract header from extracted data"""
        header_data = {
            "contract_number": "VC-2025-0001",
            "vendor_name": "Test Vendor",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "contract_value": "$100,000",
            "payment_terms": "Net 30",
            "currency": "USD",
            "contract_type": "Service Agreement"
        }

        header = ContractHeader(**header_data)

        assert header.contract_number == "VC-2025-0001"
        assert header.vendor_name == "Test Vendor"
        assert header.currency == "USD"

    def test_service_detail_creation(self):
        """Test creating service detail from extracted data"""
        service_data = {
            "contract_number": "VC-2025-0001",
            "service_name": "Cloud Support",
            "service_description": "24/7 support",
            "unit": "Per Month",
            "rate": "$5,000",
            "currency": "USD",
            "minimum_order": "1 month",
            "volume_discount": "10%",
            "effective_from": "2025-01-01"
        }

        service = ServiceDetail(**service_data)

        assert service.service_name == "Cloud Support"
        assert service.rate == "$5,000"

    def test_handle_missing_fields(self):
        """Test handling missing fields in extraction"""
        partial_header = ContractHeader(
            contract_number="VC-2025-0001"
            # Other fields omitted
        )

        assert partial_header.contract_number == "VC-2025-0001"
        assert partial_header.vendor_name == ""  # Default
        assert partial_header.currency == ""  # Default

    def test_extract_multiple_services(self):
        """Test extracting multiple services from one contract"""
        services = [
            ServiceDetail(
                contract_number="VC-2025-0001",
                service_name=f"Service {i}",
                rate=f"${1000 * i}"
            ) for i in range(1, 4)
        ]

        assert len(services) == 3
        assert services[0].service_name == "Service 1"
        assert services[2].rate == "$3000"


class TestMockExtraction:
    """Test mock extraction functionality"""

    def test_mock_extraction_data_structure(self):
        """Test that mock extraction returns correct structure"""
        from contract_extractor_test import extract_contract_info_mock

        header, services = extract_contract_info_mock(
            "sample_contract_1_techsolutions.docx"
        )

        assert header is not None
        assert isinstance(header, ContractHeader)
        assert isinstance(services, list)
        assert all(isinstance(s, ServiceDetail) for s in services)

    def test_mock_extraction_techsolutions(self):
        """Test mock extraction for TechSolutions contract"""
        from contract_extractor_test import extract_contract_info_mock

        header, services = extract_contract_info_mock(
            "sample_contract_1_techsolutions.docx"
        )

        assert header.contract_number == "VC-2025-0001"
        assert header.vendor_name == "TechSolutions Inc."
        assert len(services) == 3

    def test_mock_extraction_officeworld(self):
        """Test mock extraction for OfficeWorld contract"""
        from contract_extractor_test import extract_contract_info_mock

        header, services = extract_contract_info_mock(
            "sample_contract_2_officeworld.docx"
        )

        assert header.contract_number == "VC-2025-0002"
        assert header.vendor_name == "OfficeWorld Supplies Ltd."
        assert len(services) == 2

    def test_mock_extraction_globalship(self):
        """Test mock extraction for GlobalShip contract"""
        from contract_extractor_test import extract_contract_info_mock

        header, services = extract_contract_info_mock(
            "sample_contract_3_globalship.docx"
        )

        assert header.contract_number == "VC-2025-0003"
        assert header.vendor_name == "GlobalShip Logistics"
        assert len(services) == 3

    def test_mock_extraction_nonexistent(self):
        """Test mock extraction with non-existent contract"""
        from contract_extractor_test import extract_contract_info_mock

        header, services = extract_contract_info_mock("nonexistent.docx")

        assert header is None
        assert services == []

    def test_mock_extraction_total_services(self):
        """Test total services extracted in test mode"""
        from contract_extractor_test import extract_contract_info_mock

        files = [
            "sample_contract_1_techsolutions.docx",
            "sample_contract_2_officeworld.docx",
            "sample_contract_3_globalship.docx"
        ]

        total_services = 0
        for filename in files:
            _, services = extract_contract_info_mock(filename)
            total_services += len(services)

        # Should have 3 + 2 + 3 = 8 total services
        assert total_services == 8


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
