"""
Unit tests for data models
Tests Pydantic models for ContractHeader and ServiceDetail
"""

import pytest
from pydantic import ValidationError
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from contract_extractor import ContractHeader, ServiceDetail


class TestContractHeaderModel:
    """Test ContractHeader Pydantic model"""

    def test_valid_contract_header(self):
        """Test creating a valid ContractHeader"""
        header = ContractHeader(
            contract_number="VC-2025-0001",
            vendor_name="TechSolutions Inc.",
            start_date="2025-01-01",
            end_date="2025-12-31",
            contract_value="$150,000",
            payment_terms="Net 30",
            currency="USD",
            contract_type="Service Agreement"
        )
        assert header.contract_number == "VC-2025-0001"
        assert header.vendor_name == "TechSolutions Inc."
        assert header.currency == "USD"

    def test_minimal_contract_header(self):
        """Test ContractHeader with only required fields (all are optional with defaults)"""
        header = ContractHeader()
        assert header.contract_number == ""
        assert header.vendor_name == ""
        assert header.currency == ""

    def test_partial_contract_header(self):
        """Test ContractHeader with some fields populated"""
        header = ContractHeader(
            contract_number="VC-2025-0001",
            vendor_name="TechSolutions Inc."
        )
        assert header.contract_number == "VC-2025-0001"
        assert header.vendor_name == "TechSolutions Inc."
        assert header.start_date == ""
        assert header.end_date == ""

    def test_contract_header_field_types(self):
        """Test that all fields accept strings"""
        header = ContractHeader(
            contract_number="123",
            vendor_name="Vendor A",
            start_date="2025-01-01",
            end_date="2025-12-31",
            contract_value="100000",
            payment_terms="30 days",
            currency="USD",
            contract_type="Service"
        )
        assert isinstance(header.contract_number, str)
        assert isinstance(header.vendor_name, str)
        assert isinstance(header.contract_value, str)

    def test_contract_header_to_dict(self):
        """Test conversion to dictionary"""
        header = ContractHeader(
            contract_number="VC-2025-0001",
            vendor_name="TechSolutions Inc.",
            currency="USD"
        )
        data = header.model_dump()
        assert isinstance(data, dict)
        assert data["contract_number"] == "VC-2025-0001"
        assert data["vendor_name"] == "TechSolutions Inc."

    def test_contract_header_json_serializable(self):
        """Test that model can be serialized to JSON"""
        header = ContractHeader(
            contract_number="VC-2025-0001",
            vendor_name="TechSolutions Inc."
        )
        json_str = header.model_dump_json()
        assert "VC-2025-0001" in json_str
        assert "TechSolutions Inc." in json_str


class TestServiceDetailModel:
    """Test ServiceDetail Pydantic model"""

    def test_valid_service_detail(self):
        """Test creating a valid ServiceDetail"""
        service = ServiceDetail(
            contract_number="VC-2025-0001",
            service_name="Cloud Support",
            service_description="24/7 cloud infrastructure support",
            unit="Per Month",
            rate="$5,000",
            currency="USD",
            minimum_order="1 month",
            volume_discount="10% for annual",
            effective_from="2025-01-01"
        )
        assert service.contract_number == "VC-2025-0001"
        assert service.service_name == "Cloud Support"
        assert service.rate == "$5,000"

    def test_minimal_service_detail(self):
        """Test ServiceDetail with default values"""
        service = ServiceDetail()
        assert service.contract_number == ""
        assert service.service_name == ""
        assert service.rate == ""

    def test_service_detail_partial(self):
        """Test ServiceDetail with partial data"""
        service = ServiceDetail(
            contract_number="VC-2025-0001",
            service_name="Cloud Support",
            rate="$5,000"
        )
        assert service.contract_number == "VC-2025-0001"
        assert service.service_name == "Cloud Support"
        assert service.rate == "$5,000"
        assert service.unit == ""

    def test_multiple_services_same_contract(self):
        """Test creating multiple services for same contract"""
        services = [
            ServiceDetail(
                contract_number="VC-2025-0001",
                service_name="Service 1",
                rate="$1,000"
            ),
            ServiceDetail(
                contract_number="VC-2025-0001",
                service_name="Service 2",
                rate="$2,000"
            ),
            ServiceDetail(
                contract_number="VC-2025-0001",
                service_name="Service 3",
                rate="$3,000"
            )
        ]
        assert len(services) == 3
        assert all(s.contract_number == "VC-2025-0001" for s in services)
        assert services[0].rate == "$1,000"
        assert services[2].rate == "$3,000"

    def test_service_detail_to_dict(self):
        """Test conversion to dictionary"""
        service = ServiceDetail(
            contract_number="VC-2025-0001",
            service_name="Cloud Support",
            rate="$5,000"
        )
        data = service.model_dump()
        assert data["service_name"] == "Cloud Support"
        assert data["rate"] == "$5,000"

    def test_service_detail_json_serializable(self):
        """Test JSON serialization"""
        service = ServiceDetail(
            contract_number="VC-2025-0001",
            service_name="Cloud Support",
            rate="$5,000"
        )
        json_str = service.model_dump_json()
        assert "Cloud Support" in json_str
        assert "$5,000" in json_str


class TestModelIntegration:
    """Test models working together"""

    def test_header_with_services(self):
        """Test creating header with multiple associated services"""
        header = ContractHeader(
            contract_number="VC-2025-0001",
            vendor_name="TechSolutions Inc.",
            contract_value="$150,000",
            currency="USD"
        )

        services = [
            ServiceDetail(
                contract_number=header.contract_number,
                service_name="Service 1",
                rate="$50,000"
            ),
            ServiceDetail(
                contract_number=header.contract_number,
                service_name="Service 2",
                rate="$60,000"
            ),
            ServiceDetail(
                contract_number=header.contract_number,
                service_name="Service 3",
                rate="$40,000"
            )
        ]

        assert header.contract_number == services[0].contract_number
        assert len(services) == 3
        assert sum(float(s.rate.replace("$", "").replace(",", "")) for s in services) == 150000

    def test_batch_contracts_and_services(self):
        """Test working with multiple contracts and services"""
        contracts = [
            ContractHeader(
                contract_number=f"VC-2025-000{i}",
                vendor_name=f"Vendor {i}"
            ) for i in range(1, 4)
        ]

        assert len(contracts) == 3
        assert contracts[0].vendor_name == "Vendor 1"
        assert contracts[2].vendor_name == "Vendor 3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
