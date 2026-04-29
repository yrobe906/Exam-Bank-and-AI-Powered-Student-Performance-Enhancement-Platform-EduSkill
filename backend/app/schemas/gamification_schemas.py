from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PremiumUnlockRequest(BaseModel):
    content_type: str
    content_id: int
    content_title: str
    request_reason: Optional[str] = None
    payment_proof_url: Optional[str] = None

class GamificationSidebar(BaseModel):
    xp_points: int
    tier: str  # 'bronze', 'silver', 'gold', 'diamond'

class GamificationProfile(BaseModel):
    user_id: int
    xp_points: int
    tier: str  # 'bronze', 'silver', 'gold', 'diamond'
    streak_days: int = 0
    badges: List[str] = []
    total_activities: int = 0

class GamificationSummary(BaseModel):
    badges: List[str] = []
    total_activities: int = 0

class XPTransaction(BaseModel):
    id: int
    activity_type: str
    content_id: Optional[int] = None
    xp_amount: int
    created_at: datetime

class XPTransactionList(BaseModel):
    transactions: List[XPTransaction]

class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    username: str
    xp_points: int
    tier: str
    school_id: Optional[str] = None  # For student leaderboards

class LeaderboardResponse(BaseModel):
    subject: Optional[str] = None
    entries: List[LeaderboardEntry]
    user_rank: Optional[int] = None
    page: int = 1
    total_pages: int = 1

class AdminXPTransaction(BaseModel):
    id: int
    user_id: int
    username: str
    full_name: str
    tier: str
    activity_type: str
    content_id: Optional[int] = None
    content_type: Optional[str] = None
    xp_amount: int
    is_cooldown_active: bool
    created_at: datetime

class AdminAllRequestsResponse(BaseModel):
    transactions: List[AdminXPTransaction]
    page: int = 1
    limit: int = 100
    total_count: int = 0

