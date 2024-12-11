from pydantic import BaseModel


class ReviewWriter(BaseModel):
    username: str
    avatar_url: str
    name: str


class Review(BaseModel):
    content: str
    rating: int
    created_at: int
    writer: ReviewWriter


ReviewListResponse = list[Review]
