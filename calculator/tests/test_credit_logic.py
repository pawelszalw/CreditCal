import pytest
from calculator.models.credit_details import CreditDetails, CreditType, InterestRate


@pytest.mark.parametrize("field, value, expected_error", [
    ("initial_principal", -1, ValueError),  # Negative value for principal
    ("initial_principal", 0, ValueError),  # Zero value for principal
    ("initial_principal", 1000, None),  # Valid value for principal
    ("term", -1, ValueError),  # Negative value for term
    ("term", 0, ValueError),  # Zero value for term
    ("term", 12, None),  # Valid value for term
    ("bank_margin", -1, ValueError),  # Negative value for bank_margin
    ("bank_margin", 0, None),  # Valid value for bank_margin
    ("base_interest_rate", -0.1, ValueError),  # Negative value for base_interest_rate
    ("base_interest_rate", 0, None),  # Valid value for base_interest_rate
    ("payment_day", 0, ValueError),  # Too small value for payment_day
    ("payment_day", 32, ValueError),  # Too large value for payment_day
    ("payment_day", 15, None),  # Valid value for payment_day
    ("interest_type", "InvalidValue", ValueError),  # Invalid type for interest_type
    ("interest_type", 999, ValueError),
    ("interest_type", CreditType.FIXED, None),  # Valid type for interest_type
    ("rate_type", "InvalidValue", ValueError),  # Invalid type for rate_type
    ("rate_type", 999, ValueError),
    ("rate_type", InterestRate.CONSTANT, None)  # Valid type for rate_type
])
def test_credit_details_validation(default_credit_data, field, value, expected_error):
    """Test validation for various fields in CreditDetails."""
    data = default_credit_data.copy()  # Copy default data - memory issue
    data[field] = value  # Change only one value
    # Check if it raises an error or initializes correctly
    if expected_error:
        with pytest.raises(expected_error):
            CreditDetails(**data)
    else:
        credit = CreditDetails(**data)
        assert getattr(credit, field) == value
