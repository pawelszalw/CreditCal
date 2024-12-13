from datetime import date


def days_in_month(year: int, month: int) -> int:
    """Returns the number of days in a given month."""
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    return (next_month - date(year, month, 1)).days


class Validator:
    @staticmethod
    def validate_positive(value, field_name):
        if value <= 0:
            raise ValueError(f"{field_name} must be a positive value. Got: {value}")

    @staticmethod
    def validate_non_negative_value(value, field_name):
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative. Got: {value}")

    @staticmethod
    def validate_payment_day(payment_day):
        if not (1 <= payment_day <= 31):
            raise ValueError(f"payment_day must be between 1 and 31. Got: {payment_day}")

    @staticmethod
    def validate_enum(value, enum_class, field_name):
        if not isinstance(value, enum_class):
            valid_values = [e.name for e in enum_class]
            raise ValueError(f"{field_name} must be one of {valid_values}. Got: {value}")
