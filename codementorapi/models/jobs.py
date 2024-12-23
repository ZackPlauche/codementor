from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Optional, Union, Annotated


class Category(BaseModel):
    name: str
    url_string: str


class BaseUser(BaseModel):
    name: str
    username: str
    small_avatar_url: str


class JobListItemUser(BaseUser):
    pass


class JobDetailResponseUser(BaseUser):
    time_zone_display: str
    is_student: bool


class TutoringDetails(BaseModel):
    kind: Literal["tutoring"]
    description: str
    estimated_length: Optional[str] = None
    estimated_hours_per_week: Optional[int] = None
    estimated_weeks: Optional[int] = None


class ProjectDetails(BaseModel):
    kind: Literal["existing-project", "new-project"]
    description: str
    tech_family: str
    deliverables: str
    estimated_completion_date: int


class TroubleshootingDetails(BaseModel):
    kind: Literal["troubleshooting", "debugging"]
    description: str
    estimated_length: str


JobDetails = Annotated[
    Union[TutoringDetails, ProjectDetails, TroubleshootingDetails],
    Field(discriminator='kind')
]


class BaseJob(BaseModel):
    random_key: str
    title: str
    body: str
    request_type: Literal["one_on_one", "longterm", "offline_help", "code_review"]
    aasm_state: str
    estimated_budget: str
    created_at: int
    is_featured: bool
    has_recruiter_addon: bool
    categories: list[Category]


class JobListItem(BaseJob):
    interest_count: int
    read: bool
    user: JobListItemUser


class JobDetailResponse(BaseJob):
    skipped: bool
    reported_as_homework: bool
    can_express_interest: bool
    interest: Optional[str]
    detail: JobDetails
    special_rate: Optional[str]
    user: JobDetailResponseUser


JobListResponse = list[JobListItem]


class JobInterestResponse(BaseModel):
    request: JobInterestRequest


class JobInterestRequest(BaseModel):
    random_key: str
    user: JobInterestUser


class JobInterestUser(BaseModel):
    online: bool
