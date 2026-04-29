from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from typing import List, Optional
from app.utils.gamification_utils import get_tier, calculate_streak, get_user_badges
from app.models.user_models import User
from app.models.gamification_models import GamificationActivityModel
from app.schemas.gamification_schemas import (
    GamificationProfile, GamificationSummary, XPTransactionList, XPTransaction, 
    LeaderboardResponse, LeaderboardEntry, AdminXPTransaction, AdminAllRequestsResponse,
    GamificationSidebar
)

def get_gamification_service(db: Session):
    return GamificationService(db)

class GamificationService:
    def __init__(self, db: Session):
        self.db = db

    def award_exam_submission_xp(self, user_id: int, exam_id: int) -> int:
        """Award 20 XP for every exam submission (no cooldown)."""
        xp_amount = 20
        activity = GamificationActivityModel(
            user_id=user_id,
            activity_type='exam_submission',
            content_id=exam_id,
            content_type='exam',
            xp_awarded=xp_amount
        )
        self.db.add(activity)
        self._update_user_xp(user_id, xp_amount)
        self.db.commit()
        return xp_amount

    def award_exam_result_xp(self, user_id: int, exam_id: int, percentage: float) -> int:
        """Award XP based on score tiers: 0-40%=5, 40-60%=10, 60-90%=15, 90+%=20."""
        print(f"Gamification: Awarding exam_result XP for user {user_id}, exam {exam_id}, percentage {percentage}")
        if percentage > 90:
            xp_amount = 20
        elif percentage >= 60:
            xp_amount = 15
        elif percentage >= 40:
            xp_amount = 10
        else:
            xp_amount = 5

        print(f"Gamification: Calculated {xp_amount} XP for result")

        activity = GamificationActivityModel(
            user_id=user_id,
            activity_type='exam_result',
            content_id=exam_id,
            content_type='exam',
            xp_awarded=xp_amount
        )
        self.db.add(activity)
        print(f"Gamification: Created activity for {xp_amount} XP")
        updated = self._update_user_xp(user_id, xp_amount)
        print(f"Gamification: User XP update result: {updated}")
        self.db.commit()
        print(f"Gamification: DB committed exam_result {xp_amount} XP")
        return xp_amount

    def award_daily_login_xp(self, user_id: int) -> int:
        """Award 10 XP for daily login, supports streaks."""
        # Check if already awarded today
        today_activity = self.db.query(GamificationActivityModel).filter(
            GamificationActivityModel.user_id == user_id,
            GamificationActivityModel.activity_type == 'daily_login',
            func.date(GamificationActivityModel.created_at) == func.now()
        ).first()
        if today_activity:
            return 0  # Already logged today

        xp_amount = 10
        activity = GamificationActivityModel(
            user_id=user_id,
            activity_type='daily_login',
            xp_awarded=xp_amount
        )
        self.db.add(activity)
        self._update_user_xp(user_id, xp_amount)
        self.db.commit()
        return xp_amount

    def award_premium_purchase_xp(self, user_id: int, content_id: int) -> int:
        """Award XP for premium content purchase based on total purchases."""
        # Count total premium purchases by this user
        total_purchases = self.db.query(GamificationActivityModel).filter(
            GamificationActivityModel.user_id == user_id,
            GamificationActivityModel.activity_type == 'premium_purchase'
        ).count()

        # Calculate XP based on total purchases (including this one)
        total_purchases += 1

        if total_purchases == 1:
            xp_amount = 20
        elif total_purchases == 2:
            xp_amount = 30  # To make total 50
        elif total_purchases >= 3:
            xp_amount = 20  # Standard amount for 3+
        else:
            xp_amount = 20  # Fallback

        activity = GamificationActivityModel(
            user_id=user_id,
            activity_type='premium_purchase',
            content_id=content_id,
            content_type='premium_content',
            xp_awarded=xp_amount
        )
        self.db.add(activity)
        self._update_user_xp(user_id, xp_amount)
        self.db.commit()
        return xp_amount

    def record_activity(self, user_id: int, activity_type: str, content_id: Optional[int] = None, content_type: Optional[str] = None):
        """Record non-XP activity for streaks/badges."""
        activity = GamificationActivityModel(
            user_id=user_id,
            activity_type=activity_type,
            content_id=content_id,
            content_type=content_type,
            xp_awarded=0
        )
        self.db.add(activity)
        self.db.commit()

    def _update_user_xp(self, user_id: int, xp_amount: int):
        """Update user XP and tier."""
        print(f"Gamification _update_user_xp: user_id={user_id}, xp_amount={xp_amount}")
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            print(f"Gamification _update_user_xp: Found user {user.id} ({user.username if hasattr(user, 'username') else 'no username'}), old XP={user.xp_points}")
            user.xp_points += xp_amount
            user.xp_points = max(0, user.xp_points)
            old_tier = user.current_tier
            user.current_tier = get_tier(user.xp_points)
            self.db.flush()
            self.db.commit()
            print(f"Gamification _update_user_xp: SUCCESS new XP={user.xp_points}, tier={old_tier}->{user.current_tier}")
            return True
        else:
            print(f"Gamification _update_user_xp: User {user_id} NOT FOUND")
            return False

    def get_profile(self, user_id: int) -> GamificationProfile:
        """Get full gamification profile."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # Get activities for streak/badges
        activities = self.db.query(GamificationActivityModel).filter(
            GamificationActivityModel.user_id == user_id
        ).all()
        activities_dict = [{'activity_type': a.activity_type, 'created_at': a.created_at} for a in activities]
        streak_days = calculate_streak(activities_dict)
        total_activities = len(activities)
        badges = get_user_badges(user.xp_points, streak_days, total_activities // 2)  # Approx exams

        return GamificationProfile(
            user_id=user.id,
            xp_points=user.xp_points,
            tier=user.current_tier,
            streak_days=streak_days,
            badges=badges,
            total_activities=total_activities
        )

    def get_sidebar(self, user_id: int) -> GamificationSidebar:
        """Get gamification data for sidebar display."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        return GamificationSidebar(
            xp_points=user.xp_points,
            tier=user.current_tier
        )

    def get_summary(self, user_id: int) -> GamificationSummary:
        """Get badges and total activities summary."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return GamificationSummary(badges=[], total_activities=0)

        activities = self.db.query(GamificationActivityModel).filter(
            GamificationActivityModel.user_id == user_id
        ).all()
        activities_dict = [{'activity_type': a.activity_type, 'created_at': a.created_at} for a in activities]
        streak_days = calculate_streak(activities_dict)
        total_activities = len(activities)
        badges = get_user_badges(user.xp_points, streak_days, total_activities // 2)

        return GamificationSummary(badges=badges, total_activities=total_activities)

    def get_transactions(self, user_id: int, limit: int = 20) -> XPTransactionList:
        """Get recent XP transactions."""
        activities = self.db.query(GamificationActivityModel).filter(
            GamificationActivityModel.user_id == user_id,
            GamificationActivityModel.xp_awarded != 0
        ).order_by(desc(GamificationActivityModel.created_at)).limit(limit).all()

        transactions = []
        for a in activities:
            transactions.append(XPTransaction(
                id=a.id,
                activity_type=a.activity_type,
                content_id=a.content_id,
                xp_amount=a.xp_awarded,
                created_at=a.created_at
            ))

        return XPTransactionList(transactions=transactions)

    def get_leaderboard(self, subject: Optional[str] = None, page: int = 1, limit: int = 10) -> LeaderboardResponse:
        """Get leaderboard, filtered by subject (teacher view)."""
        query = self.db.query(
            User.id,
            User.username,
            User.xp_points,
            User.current_tier,
            User.school_id,
            func.row_number().over(order_by=desc(User.xp_points)).label('rank')
        ).filter(User.role == 'student')

        if subject:
            query = query.join(GamificationActivityModel).filter(
                GamificationActivityModel.content_type == 'exam',
                # Assume content_id maps to subject somehow, or add subject field later
            )

        leaderboard_users = query.order_by(desc(User.xp_points)).offset((page - 1) * limit).limit(limit).all()

        entries = []
        for row in leaderboard_users:
            entries.append(LeaderboardEntry(
                rank=row.rank,
                user_id=row.id,
                username=row.username,
                xp_points=row.xp_points,
                tier=row.current_tier,
                school_id=row.school_id
            ))

        return LeaderboardResponse(
            subject=subject,
            entries=entries,
            page=page,
            total_pages=1  # Calculate properly later with count query
        )

    def get_all_requests(self, page: int = 1, limit: int = 100) -> AdminAllRequestsResponse:
        """Admin: Get all gamification activities/requests across all users."""
        offset = (page - 1) * limit
        
        # Count total
        total_count = self.db.query(func.count(GamificationActivityModel.id)).scalar()
        
        # Query with join
        activities = self.db.query(
            GamificationActivityModel,
            User.id.label('user_id'),
            User.username,
            User.full_name,
            User.current_tier
        ).outerjoin(
            User, GamificationActivityModel.user_id == User.id
        ).order_by(
            desc(GamificationActivityModel.created_at)
        ).offset(offset).limit(limit).all()
        
        transactions = []
        for activity, user_id, username, full_name, tier in activities:
            transactions.append(AdminXPTransaction(
                id=activity.id,
                user_id=activity.user_id,
                username=username or f"User {activity.user_id}",
                full_name=full_name or "N/A",
                tier=tier or "none",
                activity_type=activity.activity_type,
                content_id=activity.content_id,
                content_type=activity.content_type,
                xp_amount=activity.xp_awarded,
                created_at=activity.created_at
            ))
        
        return AdminAllRequestsResponse(
            transactions=transactions,
            page=page,
            limit=limit,
            total_count=total_count
        )

