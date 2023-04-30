from dataclasses import dataclass


@dataclass
class TaxBands:
    basic_rate = 0.2
    basic_rate_threshold = 50_270

    higher_rate = 0.4
    higher_rate_threshold = 125_140

    additional_rate = 0.45

    personal_allowance = 12_570

    personal_allowance_lower_threshold = 100_000
    personal_allowance_upper_threshold = 125_140


def net_monthly_to_gross_annual_income(net_monthly_income: float) -> float:
    if net_monthly_income < 0:
        return 0

    annual_net_income = net_monthly_income * 12

    annual_gross_income = annual_net_income

    return annual_gross_income


def gross_annual_to_net_monthly_income(gross_annual_income: int) -> float:
    if gross_annual_income < 0:
        return 0

    return gross_annual_income / 12
