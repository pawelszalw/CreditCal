class CreditActions:
    """Provides static methods for various credit calculations."""

    @staticmethod
    def calculate_annuity_loan_payment(principal: float, annual_interest_rate: float, number_of_months: int) -> float:
        """Calculate the annuity loan payment."""
        monthly_interest_rate = annual_interest_rate / 100 / 12
        payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_months) / (
                (1 + monthly_interest_rate) ** number_of_months - 1
        )
        return round(payment, 2)

    @staticmethod
    def calculate_month_interest(principal: float, annual_interest_rate: float, days_in_month: int) -> float:
        """Calculate the interest portion for a specific month."""
        daily_interest_rate = annual_interest_rate / 100 / 365
        return round(principal * daily_interest_rate * days_in_month, 2)

    @staticmethod
    def calculate_month_principal_payment(principal: float, annual_interest_rate: float,
                                          number_of_months: int) -> float:
        """Calculate the principal portion for a specific month."""
        total_payment = CreditActions.calculate_annuity_loan_payment(
            principal, annual_interest_rate, number_of_months
        )
        monthly_interest = CreditActions.calculate_month_interest(
            principal, annual_interest_rate, 30
        )
        return round(total_payment - monthly_interest, 2)

    @staticmethod
    def calculate_variable_rate(base_rate: float, market_rate: float) -> float:
        """Calculate the variable interest rate (e.g., WIBOR/WIRON)."""
        return round(base_rate + market_rate, 2)
