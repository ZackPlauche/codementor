from __future__ import annotations

from pydantic import BaseModel
from typing import Literal, Optional


class Category(BaseModel):
    name: str
    url_string: str


class JobListItemUser(BaseModel):
    name: str
    username: str
    small_avatar_url: str


class JobDetailResponseUser(BaseModel):
    name: str
    username: str
    small_avatar_url: str
    time_zone_display: str


class JobDetails(BaseModel):
    kind: str
    description: str
    estimated_length: str


class BaseJob(BaseModel):
    random_key: str
    title: str
    body: str
    request_type: Literal["one_on_one",
                          "longterm", "offline_help", "code_review"]
    aasm_state: str
    estimated_budget: str
    created_at: int
    is_featured: bool
    has_recruiter_addon: bool
    user: JobListItemUser
    categories: list[Category]


class JobListItem(BaseJob):
    interest_count: int
    read: bool


class JobDetailResponse(BaseJob):
    skipped: bool
    reported_as_homework: bool
    can_express_interest: bool
    interest: Optional[str]
    detail: JobDetails
    special_rate: Optional[str]


JobListResponse = list[JobListItem]


class JobInterestResponse(BaseModel):
    request: JobInterestRequest


class JobInterestRequest(BaseModel):
    random_key: str
    user: JobInterestUser


class JobInterestUser(BaseModel):
    online: bool
