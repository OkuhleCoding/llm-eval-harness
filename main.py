from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from harness.db import init_db, SessionLocal, EvalRun, EvalResultRow
from harness.evaluator import evaluate_suite

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="LLM Eval Harness", lifespan=lifespan)

@app.post("/evals/run")
def trigger_run(suite_name: str = "reasoning"):
    db = SessionLocal()
    try:
        results = evaluate_suite(f"benchmarks/{suite_name}.json")

        run = EvalRun(suite_name=suite_name)
        db.add(run)
        db.commit()
        db.refresh(run)

        for r in results:
            db.add(EvalResultRow(
                run_id=run.id,
                test_id=r.test_id,
                category=r.category,
                prompt=r.prompt,
                expected=r.expected,
                actual=r.actual,
                score=r.score,
                passed=r.passed,
                scoring_method=r.scoring_method,
            ))
        db.commit()

        return {
            "run_id": run.id,
            "suite_name": suite_name,
            "results_count": len(results),
            "pass_rate": sum(1 for r in results if r.passed) / len(results),
        }
    finally:
        db.close()

@app.get("/evals")
def list_runs():
    db = SessionLocal()
    try:
        runs = db.query(EvalRun).all()
        return [{"id": r.id, "suite_name": r.suite_name, "started_at": r.started_at} for r in runs]
    finally:
        db.close()

@app.get("/evals/{run_id}")
def get_run_detail(run_id: int):
    db = SessionLocal()
    try:
        run = db.query(EvalRun).filter(EvalRun.id == run_id).first()
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        results = db.query(EvalResultRow).filter(EvalResultRow.run_id == run_id).all()
        return {
            "run_id": run.id,
            "suite_name": run.suite_name,
            "started_at": run.started_at,
            "results": [
                {
                    "test_id": r.test_id,
                    "category": r.category,
                    "score": r.score,
                    "passed": r.passed,
                    "actual": r.actual,
                }
                for r in results
            ],
        }
    finally:
        db.close()