import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "sqlite:///./soc_logs.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LogEvent(Base):
    __tablename__ = "log_events"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    ip = Column(String)
    user = Column(String)
    status = Column(String)

class IncidentEvent(Base):
    __tablename__ = "incident_events"
    incident_id = Column(Integer, ForeignKey("incidents.id"), primary_key=True)
    log_event_id = Column(Integer, ForeignKey("log_events.id"), primary_key=True)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String)
    severity = Column(String)
    summary = Column(Text)
    likely_cause = Column(Text)
    suggested_actions = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    events = relationship("LogEvent", secondary="incident_events")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
