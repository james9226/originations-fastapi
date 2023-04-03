import pytest
from originations.models.request import ApplicationRequestInput
from datetime import date

base_input_data = {
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com",
    "phone_number": "string",
    "date_of_birth": "2023-04-01",
    "address_history": [
        {
            "address_line_one": "string",
            "address_line_two": "string",
            "county": "string",
            "city": "string",
            "postcode": "string",
            "move_in_date": "2023-04-01",
        }
    ],
    "gross_annual_income": 60000,
    "monthly_housing_costs": 500,
    "residential_status": "renting",
    "marital_status": "married",
    "employment_status": "full_time",
    "employer_name": "string",
    "loan_amount": 1250,
    "loan_term_in_months": 24,
}


def test_application_request_works():
    ApplicationRequestInput(**base_input_data)


def test_validation():
    with pytest.raises(Exception) as e_info:
        input_data = base_input_data.copy()
        input_data["loan_amount"] = 500
        ApplicationRequestInput(**input_data)

    with pytest.raises(Exception) as e_info:
        input_data = base_input_data.copy()
        input_data["loan_amount"] = 10001
        ApplicationRequestInput(**input_data)

    with pytest.raises(Exception) as e_info:
        input_data = base_input_data.copy()
        input_data["loan_amount"] = 9223372036854775808
        ApplicationRequestInput(**input_data)

    with pytest.raises(Exception) as e_info:
        input_data = base_input_data.copy()
        input_data["loan_amount"] = "AISfhaoifao"
        ApplicationRequestInput(**input_data)
