from sqlalchemy import create_engine, Column, String, Float, Boolean, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

DATABASE_URL = "sqlite:///./eval_results.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class EvalRun(Base):
    __tablename__ = "eval_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    suite_name = Column(String, nullable=False)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class EvalResultRow(Base):
    __tablename__ = "eval_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(Integer, nullable=False)
    test_id = Column(String, nullable=False)
    category = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    expected = Column(String, nullable=False)
    actual = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=False)
    scoring_method = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)
