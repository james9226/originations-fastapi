from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import EmailStr, condecimal
from sqlmodel import Field, Relationship, SQLModel, Index

from originations.enums.enums import EmploymentStatus, ResidentialStatus
from originations.enums.policy import PolicyOutcome, PolicyPhase


class Applicant(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    applicant_hash: str = Field(index=True)
    creation_timestamp: datetime
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: EmailStr
    date_of_birth: date
    nationality: Optional[str]
    declared_income: int
    monthly_housing_costs: int
    dependants: int
    residential_status: ResidentialStatus
    employment_status: EmploymentStatus
    job_title: str
    employer_name: str
    employer_sector: str
    channel_code: str

    addresses: list["Address"] = Relationship(back_populates="applicant")


class Address(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    move_in_date: date
    address_line_one: str
    address_line_two: str
    city: Optional[str]
    postcode: str
    applicant: Applicant = Relationship(back_populates="addresses")

    applicant_id: UUID = Field(foreign_key="applicant.id")  # This is the foreign key


class ApplicationDecision(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    event_time: datetime
    decision: PolicyOutcome
    reason: str
    applicant_id: Optional[UUID] = Field(foreign_key="applicant.id")
    credit_profile_id: Optional[UUID] = Field(foreign_key="creditprofile.id")
    customer_id: Optional[UUID]
    quotes: list["Quote"] = Relationship(back_populates="applicationdecision")
    __table_args__ = (
        Index("index_customer_id_event_time", "customer_id", "event_time"),
    )


class Quote(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    application_id: UUID = Field(foreign_key="applicationdecision.id")
    is_requested: bool
    amount: int
    term: int
    is_approved: bool
    apr: Optional[condecimal(max_digits=24, decimal_places=8)]
    monthly_payment: Optional[condecimal(max_digits=24, decimal_places=8)]
    total_repayable: Optional[condecimal(max_digits=24, decimal_places=8)]
    di: Optional[condecimal(max_digits=24, decimal_places=8)]
    dti: Optional[condecimal(max_digits=24, decimal_places=8)]
    min_income_required: Optional[condecimal(max_digits=24, decimal_places=8)]

    applicationdecision: ApplicationDecision = Relationship(back_populates="quotes")


class CreditProfile(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    file_id: UUID
    outstanding_balance: int
    outstanding_revolving_balance: int
    num_missed_payments_last_12m: int
    monthly_fixed_term_payments_excluding_mortgage: int
    monthly_mortgage_cost: int
    credit_score: int


class ApplicationTriggers(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    event_time: datetime
    applicant_hash: str
    phase: PolicyPhase
    triggered_codes: list[str]
    __table_args__ = (
        Index("index_applicant_hash_event_time", "applicant_hash", "event_time"),
    )


class CreditVariables(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    application_id: UUID
    event_time: datetime
    total_unsecured_balance: int
    total_revolving_credit_balance: int
    total_monthly_fixed_term_loan_payments: int
    total_mortgage_balance: int
    total_monthly_mortgage_payments: int
    number_of_missed_payments_last_12_months: int
    number_of_missed_payments_last_6_months: int
    number_of_missed_payments_last_3_months: int
    number_of_missed_payments_last_month: int
