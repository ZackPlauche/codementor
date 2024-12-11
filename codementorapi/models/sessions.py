from typing import Optional
from pydantic import BaseModel


class SessionMentee(BaseModel):
    small_avatar_url: str
    name: str
    username: str


class SessionUser(BaseModel):
    name: str
    username: str
    small_avatar_url: str
    first_name: str
    time_zone_region: str
    time_zone_offset: int


class ReviewFromMentor(BaseModel):
    rating: int
    content: str


class SessionReview(BaseModel):
    rating: int
    content: str
    random_key: str
    success_review: Optional[str] = None


class BaseSession(BaseModel):
    length: int
    legacy: bool
    id: str
    aasm_state: str
    init_cost: str
    cost: str


class SessionListItem(BaseSession):
    free_length: int
    created_at: int
    mentee: SessionMentee


class SessionDetailResponse(BaseSession):
    finished_at: int
    started_at: int
    schedule_rate: str
    paid: bool
    has_invoice_question: bool
    total_cost: str
    tip_amount: str
    payment_failure: bool
    survey_is_filled: bool
    review: Optional[SessionReview] = None
    review_from_mentor: Optional[ReviewFromMentor] = None
    mentor: SessionUser
    mentee: SessionUser
    earnings: str
    is_partial_refundable: bool
    is_full_refundable: bool
    is_refunded: bool


SessionListResponse = list[SessionListItem]
