import enum
from calculator.models.utils import Validator


class CreditType(enum.Enum):
    FIXED = 1  # Fixed rate
    VARIABLE = 2  # Variable rate


class InterestRate(enum.Enum):
    CONSTANT = 0  # Fixed interest rate
    WIBOR1M = 1   # 1-month WIBOR
    WIBOR3M = 2   # 3-month WIBOR
    WIBOR6M = 3   # 6-month WIBOR


class CreditDetails:
    """This class defines an active loan and calculates installments."""
    def __init__(
        self,
        initial_principal: int,
        term: int,
        bank_margin: float,
        base_interest_rate: float,
        penalty_rate: float | None = None,
        penalty_start_month: int | None = None,
        penalty_end_month: int | None = None,
        interest_type: CreditType = CreditType.FIXED,
        rate_type: InterestRate = InterestRate.CONSTANT,
        payment_day: int = 10
    ):
        # Use the Validator class for validation
        Validator.validate_positive(initial_principal, "initial_principal")
        Validator.validate_positive(term, "term")
        Validator.validate_non_negative_value(bank_margin, "bank_margin")
        Validator.validate_non_negative_value(base_interest_rate, "base_interest_rate")
        if penalty_rate is not None:
            Validator.validate_non_negative_value(penalty_rate, "penalty_rate")
        if penalty_start_month is not None and penalty_end_month is not None:
            if penalty_start_month > penalty_end_month:
                raise ValueError("penalty_start_month cannot be greater than penalty_end_month")
        Validator.validate_payment_day(payment_day)
        Validator.validate_enum(interest_type, CreditType, "interest_type")
        Validator.validate_enum(rate_type, InterestRate, "rate_type")

        # Initialize attributes
        self._initial_principal = initial_principal
        self._current_principal = initial_principal
        self._term = term
        self.paid_month = 0
        self._bank_margin = bank_margin
        self._base_interest_rate = base_interest_rate
        self._penalty_rate = penalty_rate
        self._penalty_start_month = penalty_start_month
        self._penalty_end_month = penalty_end_month
        self._total_interest_paid = 0
        self._total_principal_paid = 0
        self._total_penalty_paid = 0
        self._total_paid = 0
        self._total_extra_paid = 0
        self._interest_type = interest_type
        self._rate_type = rate_type
        self._payment_day = payment_day  # Day of the month when payment is due

    @property
    def initial_principal(self):
        """Initial loan amount."""
        return self._initial_principal

    @property
    def current_principal(self):
        """Current remaining loan principal."""
        return self._current_principal

    @property
    def term(self):
        """Remaining loan term (in months)."""
        return self._term

    @property
    def bank_margin(self):
        """Bank margin, relevant for variable interest rates."""
        return self._bank_margin

    @property
    def base_interest_rate(self):
        """Base interest rate (fixed or variable)."""
        return self._base_interest_rate

    @property
    def penalty_rate(self):
        """Penalty rate for early repayment, if applicable."""
        return self._penalty_rate

    @property
    def payment_day(self):
        """Penalty rate for early repayment, if applicable."""
        return self._payment_day

    @property
    def interest_type(self):
        """Type of interest (Fixed or Variable)."""
        return self._interest_type

    @property
    def rate_type(self):
        """Type of rate (e.g., CONSTANT, WIBOR1M)."""
        return self._rate_type

    @property
    def total_interest_rate(self) -> float:
        """Returns the total interest rate (base + bank margin)."""
        return self._base_interest_rate + self._bank_margin

    def change_bank(self, new_bank_margin: float, new_interest_rate: float):
        """Change the bank's interest terms."""
        self._bank_margin = new_bank_margin
        self._base_interest_rate = new_interest_rate