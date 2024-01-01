from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from originations.services.applicant.hash import hash_application
from originations.models.request import ApplicationRequestInput

from originations.models.sqlmodels import Address, Applicant


class ApplicantService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_applicant_by_id(self, applicant_id: UUID) -> Optional[Applicant]:
        query = select(Applicant).where(Applicant.id == applicant_id)
        applicant = await self.db.exec(query)
        return applicant.first()

    async def get_applicants_by_hash(
        self, applicant_hash: str, min_timestamp: datetime
    ) -> list[Applicant]:
        query = select(Applicant).where(
            Applicant.applicant_hash == applicant_hash,
            Applicant.creation_timestamp >= min_timestamp,
        )
        applicants = await self.db.exec(query)
        return applicants.all()

    async def create_applicant(self, request: ApplicationRequestInput) -> Applicant:
        hash = hash_application(request)
        address_history = [
            Address(
                id=uuid4(),
                move_in_date=x.move_in_date,
                address_line_one=x.address_line_one,
                address_line_two=x.address_line_two,
                city=x.city,
                postcode=x.postcode,
            )
            for x in request.address_history
        ]
        applicant = Applicant(
            id=uuid4(),
            applicant_hash=hash,
            creation_timestamp=datetime.now(),
            first_name=request.first_name,
            middle_name=request.middle_name,
            last_name=request.last_name,
            email=request.email,
            date_of_birth=request.date_of_birth,
            nationality=request.nationality,
            declared_income=request.gross_annual_income,
            monthly_housing_costs=request.monthly_housing_costs,
            dependants=request.number_of_dependants,
            residential_status=request.residential_status,
            employment_status=request.employment_status,
            job_title=request.job_title,
            employer_name=request.employer_name,
            employer_sector=request.employer_sector,
            channel_code="uat_one",
            addresses=address_history,
        )

        self.db.add(applicant)

        return applicant
