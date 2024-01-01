from datetime import datetime
from uuid import UUID, uuid4

from originations.models.sqlmodels import CreditVariables


def calculate_credit_variables(credit_file, application_id: UUID) -> CreditVariables:
    return CreditVariables(
        id=uuid4(),
        application_id=application_id,
        event_time=datetime.now(),
        total_unsecured_balance=2500,
        total_revolving_credit_balance=2500,
        total_monthly_fixed_term_loan_payments=0,
        total_mortgage_balance=175000,
        total_monthly_mortgage_payments=1200,
        number_of_missed_payments_last_12_months=2,
        number_of_missed_payments_last_6_months=1,
        number_of_missed_payments_last_3_months=1,
        number_of_missed_payments_last_month=0,
    )
