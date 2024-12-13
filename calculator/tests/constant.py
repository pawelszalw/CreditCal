from calculator.models.credit_details import CreditType, InterestRate


class DefaultCreditData:
    """Class holding default valid values for CreditDetails."""
    initial_principal = 500000
    term = 360
    bank_margin = 1.5
    base_interest_rate = 2.0
    penalty_rate = None
    penalty_start_month = None
    penalty_end_month = None
    interest_type = CreditType.FIXED
    rate_type = InterestRate.CONSTANT
    payment_day = 10