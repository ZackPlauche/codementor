from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional, Union, Dict, Any


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


class JobDetails(BaseModel):
    """Base model for all job details"""
    kind: str  # More flexible, accept any kind
    description: str
    # Common optional fields
    estimated_length: Optional[str] = None
    estimated_hours_per_week: Optional[int] = None
    estimated_weeks: Optional[int] = None
    tech_family: Optional[str] = None
    deliverables: Optional[str] = None
    estimated_completion_date: Optional[int] = None


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


class JobInterest(BaseModel):
    """Model for job interest data"""
    message: str
    # Add other fields as needed based on the actual response
    # Using dict for flexibility until we know all possible fields
    additional_fields: Dict[str, Any] = Field(default_factory=dict)


class JobDetailResponse(BaseJob):
    model_config = ConfigDict(
        # Increase max_length for error messages
        str_max_length=4096,  # or however long you need
        # Show all validation errors
        validate_assignment=True,
        # Include more context in errors
        extra='forbid'
    )
    skipped: bool
    reported_as_homework: bool
    can_express_interest: bool
    interest: Optional[Union[str, JobInterest]] = None  # Can be string or interest object
    detail: JobDetails
    special_rate: Optional[str]
    user: JobDetailResponseUser


JobListResponse = list[JobListItem]


class JobInterestRequest(BaseModel):
    random_key: str
    user: JobInterestUser


class JobInterestUser(BaseModel):
    online: bool


class JobInterestResponse(BaseModel):
    request: JobInterestRequest
