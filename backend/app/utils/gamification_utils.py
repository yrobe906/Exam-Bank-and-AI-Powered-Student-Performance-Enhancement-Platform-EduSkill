"""Pure gamification utilities - XP tiers, streaks, badges (no downloadables)."""

from typing import Dict, List
from datetime import datetime, timedelta

TIER_THRESHOLDS = {
    "bronze": 0,
    "silver": 300,
    "gold": 600,
    "diamond": 3000
}

BADGES = {
    "daily_login": "Daily Streak Master",
    "exam_master": "Exam Completion Pro",
    "high_score": "Top Scorer"
}

def get_tier(xp_points: int) -> str:
    """Get user tier based on XP thresholds."""
    for tier, threshold in sorted(TIER_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
        if xp_points >= threshold:
            return tier
    return "bronze"

def calculate_streak(activities: List[Dict]) -> int:
    """Calculate current streak days from recent daily_login activities."""
    if not activities:
        return 0
    
    # Filter and sort recent daily_login by date desc
    recent_logins = sorted(
        [a for a in activities if a.get('activity_type') == 'daily_login' and a.get('created_at')],
        key=lambda a: a['created_at'],
        reverse=True
    )
    
    streak = 0
    expected_date = datetime.now().date()
    
    for login in recent_logins:
        login_day = login['created_at'].date()
        if login_day == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        elif login_day < expected_date:
            break
    
    return streak

def get_user_badges(xp_points: int, streak_days: int, total_exams: int) -> List[str]:
    """Award badges based on achievements."""
    badges_earned = []
    
    if streak_days >= 7:
        badges_earned.append("daily_login")
    if total_exams >= 50:
        badges_earned.append("exam_master")
    if xp_points >= 2000:
        badges_earned.append("high_score")
    
    return [BADGES[b] for b in badges_earned]

