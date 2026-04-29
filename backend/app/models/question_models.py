from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class QuestionModel(Base):
    # Matches your database table name (singular)
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)

    section_id = Column(
        Integer,
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False
    )

    question_text = Column(Text, nullable=False)

    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)

    correct_answer = Column(String(1), nullable=False)
    difficulty = Column(Integer, nullable=False)
    marks = Column(Integer, default=1)

    section = relationship(
        "SectionModel",
        back_populates="questions"
    )
