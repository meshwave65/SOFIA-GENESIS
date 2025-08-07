from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from engine.backend.app.database.connect_db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum("pending", "in_progress", "managing", "on_hold", "completed", "cancelled"), default="pending", nullable=False)
    priority = Column(Enum("critical", "high", "medium", "low"), default="medium", nullable=False)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    wbs_tag = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    parent_task = relationship("Task", remote_side=[id])
    metadata_entries = relationship("TaskMetadata", back_populates="task")
    history_entries = relationship("TaskHistory", back_populates="task")

class MetadataType(Base):
    __tablename__ = "metadata_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    metadata_values = relationship("MetadataValue", back_populates="type")

class MetadataValue(Base):
    __tablename__ = "metadata_values"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("metadata_types.id"), nullable=False)
    value = Column(String(255), nullable=False)

    type = relationship("MetadataType", back_populates="metadata_values")
    task_metadata = relationship("TaskMetadata", back_populates="metadata_value")

class TaskMetadata(Base):
    __tablename__ = "task_metadata"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    metadata_id = Column(Integer, ForeignKey("metadata_values.id"), primary_key=True)

    task = relationship("Task", back_populates="metadata_entries")
    metadata_value = relationship("MetadataValue", back_populates="task_metadata")

class TaskHistory(Base):
    __tablename__ = "task_history"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    author_id = Column(String(100))
    event_type = Column(Enum("created", "status_change", "comment", "assignment", "metadata_change", "desmembered"), nullable=False)
    details = Column(Text) # Using Text for JSON, will be handled as JSON in FastAPI

    task = relationship("Task", back_populates="history_entries")


