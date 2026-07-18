from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey

from app.database import Base


class Application(Base):

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String)

    position = Column(String)

    location = Column(String)

    status = Column(String)

    date_applied = Column(Date)

    feedback = Column(Text)

    notes = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"))

