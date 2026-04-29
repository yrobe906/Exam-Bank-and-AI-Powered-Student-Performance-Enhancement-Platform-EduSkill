from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime
from database import Base

class AIChatHistory(Base):
    __tablename__ = "ai_chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    context = Column(Text, default="general")
    created_at = Column(DateTime, default=datetime.utcnow)