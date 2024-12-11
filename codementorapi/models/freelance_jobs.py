from typing import Optional
from pydantic import BaseModel


class FreelanceMentee(BaseModel):
    id: int
    username: str
    name: str
    avatar_url: str
    small_avatar_url: str
    time_zone_str: str


class FreelanceMentor(BaseModel):
    id: int
    username: str
    name: str
    avatar_url: str
    small_avatar_url: str
    time_zone_str: str


class FreelanceReview(BaseModel):
    id: Optional[int] = None
    content: Optional[str] = None
    rating: Optional[int] = None


class FreelanceJobListItem(BaseModel):
    title: str
    content: str
    cost: str
    aasm_state: str
    comment: Optional[str] = None
    delay_payment: bool
    processing_payout: Optional[bool] = None
    mentor_comment: Optional[str] = None
    refund_state: str
    deliverable: Optional[str] = None
    code_review_job: bool
    random_key: str
    id: str
    created_at: int
    updated_at: int
    finished_at: int
    solved_at: int
    deadline: Optional[int] = None
    mentor_amount: str
    commission: Optional[str] = None
    mentor: FreelanceMentor
    mentee: FreelanceMentee
    auto_confirm_at: Optional[int] = None
    review: Optional[FreelanceReview] = None


FreelanceJobListResponse = list[FreelanceJobListItem]
