from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, Text, DateTime, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
import enum


class ExerciseCategory(enum.Enum):
    """Exercise category enumeration"""
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    BALANCE = "balance"
    SPORTS = "sports"
    OTHER = "other"


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    workouts: Mapped[list["Workout"]] = relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    runs: Mapped[list["Run"]] = relationship("Run", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"


class Exercise(Base):
    """Exercise model for workout exercises catalog"""
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[ExerciseCategory] = mapped_column(Enum(ExerciseCategory), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Exercise(id={self.id}, name='{self.name}', category='{self.category.value}')>"


class Workout(Base):
    """Workout model for tracking workout sessions"""
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="workouts")

    def __repr__(self) -> str:
        return f"<Workout(id={self.id}, user_id={self.user_id}, date='{self.date}')>"


class Run(Base):
    """Run model for tracking running sessions"""
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="runs")

    def __repr__(self) -> str:
        return f"<Run(id={self.id}, user_id={self.user_id}, distance={self.distance_km}km, date='{self.date}')>"