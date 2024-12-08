class CreditDetails:
    """This class defines an active credit"""
    def __init__(
            self,
            principal: int,
            term: int,
            bank_margin: float,
            base_interest_rate: float,
            penalty_rate: float | None = None,
            penalty_start_month: int | None = None,
            penalty_end_month: int | None = None,
    ):
        self._principal = principal
        self._term = term
        self.paid_month = 0
        self._bank_margin = bank_margin  # Bank margin
        self._base_interest_rate = base_interest_rate  # Base interest rate
        self._penalty_rate = penalty_rate
        self._penalty_start_month = penalty_start_month
        self._penalty_end_month = penalty_end_month
        self._total_interest_payed = 0
        self._total_principal_payed = 0
        self._total_penalty_payed = 0
        self._total_payed = 0
        self._total_extra_payed = 0

    @property
    def principal(self):
        return self._principal

    @property
    def term(self):
        return self._term

    @property
    def bank_margin(self):
        return self._bank_margin

    @property
    def base_interest_rate(self):
        return self._base_interest_rate

    @property
    def penalty_rate(self):
        return self._penalty_rate

    @property
    def total_interest_payed(self):
        return self._total_interest_payed

    @property
    def total_principal_payed(self):
        return self._total_principal_payed

    @property
    def total_penalty_payed(self):
        return self._total_penalty_payed

    @property
    def total_payed(self):
        return self._total_payed

    def credit_summary(self):
        return (f"Current paid {self.paid_month} from {self._term} months:\n"
                f"You still have {round(self._principal,2)} PLN to pay.\n"
                f"You already paid:\n"
                f"{round(self._total_interest_payed,2)} PLN intereset\n"
                f"{round(self._total_principal_payed,2)} PLN principal ({round(self._total_extra_payed,2)} thanks to extra pays)\n"
                f"{round(self._total_penalty_payed,2)} PLN penelty\n")

    @property
    def total_interest_rate(self) -> float:
        """Returns a total interest rate which is sum of base_interest_rate and bank margin"""
        return self._base_interest_rate + self._bank_margin

    @property
    def current_expected_loan_rate(self):
        return CreditActions.calculate_annuity_loan_payment(
            self._principal,
            self.total_interest_rate,
            self._term-self.paid_month
        )

    def change_bank(self, new_bank_margin: float, new_interest_rate: float):
        self._bank_margin = new_bank_margin
        self._base_interest_rate = new_interest_rate

    def month_payment(self, paid_value: float):
        normal_month_principal_payment = CreditActions.calculate_month_principal_payment(
            principal=self._principal,
            annual_interest_rate=self.total_interest_rate,
            number_of_months=self._term-self.paid_month
        )
        normal_month_interest_payment = CreditActions.calculate_month_interest(
            principal=self._principal,
            annual_interest_rate=self.total_interest_rate
        )
        if paid_value >= self.current_expected_loan_rate:
            self._total_interest_payed += normal_month_interest_payment
            self._total_payed += paid_value

            if paid_value > self.current_expected_loan_rate:
                # Extra payment
                extra_payment = round(paid_value - self.current_expected_loan_rate, 2)
                penalty_payment = 0
                if self._penalty_rate and self.paid_month in range(self._penalty_start_day,
                                                                   self._penalty_end_month + 1):
                    penalty_payment = extra_payment * (self._penalty_rate / 100)
                    extra_payment -= penalty_payment

                self._total_penalty_payed += penalty_payment
                self._total_extra_payed += extra_payment
                self._principal -= normal_month_principal_payment + extra_payment
                self._total_principal_payed += normal_month_principal_payment + extra_payment
            else:
                # Normal payment
                self._principal -= normal_month_principal_payment
                self._total_principal_payed += normal_month_principal_payment

            self.paid_month += 1

            # Adjust for loan overpayment
            if self._principal < 0:
                overpayment = -self._principal
                self._total_principal_payed -= overpayment
                self._total_extra_payed -= overpayment
                self._total_payed -= overpayment
                self._principal = 0
        else:
            print("Didn't pay enough in this month - bank doesn't like it")


class CreditActions:
    @staticmethod
    def calculate_annuity_loan_payment(principal: float, annual_interest_rate: float, number_of_months: int) -> float:
        """Returns a annuity month loan payment"""
        monthly_interest_rate = annual_interest_rate / 100 / 12
        payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_months) / (
                    (1 + monthly_interest_rate) ** number_of_months - 1)
        return round(payment, 2)

    @staticmethod
    def calculate_month_interest(principal: float, annual_interest_rate: float) -> float:
        """returns a month interest payment"""
        monthly_interest_rate = annual_interest_rate / 100 / 12
        return round(principal * monthly_interest_rate, 2)

    @staticmethod
    def calculate_month_principal_payment(
            principal: float, annual_interest_rate: float, number_of_months: float) -> float:
        """returns a month principal payment"""
        month_principal_payment = (
                CreditActions.calculate_annuity_loan_payment(principal, annual_interest_rate, number_of_months) -
                CreditActions.calculate_month_interest(principal, annual_interest_rate))
        return round(month_principal_payment, 2)