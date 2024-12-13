import pytest
from calculator.tests.constant import DefaultCreditData


@pytest.fixture
def default_credit_data():
    """Fixture providing default credit data."""
    return {
        "initial_principal": DefaultCreditData.initial_principal,
        "term": DefaultCreditData.term,
        "bank_margin": DefaultCreditData.bank_margin,
        "base_interest_rate": DefaultCreditData.base_interest_rate,
        "penalty_rate": DefaultCreditData.penalty_rate,
        "penalty_start_month": DefaultCreditData.penalty_start_month,
        "penalty_end_month": DefaultCreditData.penalty_end_month,
        "interest_type": DefaultCreditData.interest_type,
        "rate_type": DefaultCreditData.rate_type,
        "payment_day": DefaultCreditData.payment_day,
    }