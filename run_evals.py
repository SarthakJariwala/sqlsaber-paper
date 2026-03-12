import argparse
import asyncio
import json
import sqlite3
from pathlib import Path

from sqlsaber import SQLSaber
from sqlsaber.config.settings import ThinkingLevel
from sqlsaber.options import SQLSaberOptions
from sqlsaber.threads.manager import ThreadManager

MODELS = {
    "gpt-5.3-codex": "openai:gpt-5.3-codex",
    "opus-4-6": "anthropic:claude-opus-4-6",
    "gemini-3.1-pro": "google:gemini-3.1-pro-preview",
}

RESULTS_DIR = Path(__file__).parent / "results"


def parse_args():
    parser = argparse.ArgumentParser(description="Run SQLSaber benchmark evaluations")
    parser.add_argument(
        "--model",
        choices=list(MODELS.keys()),
        required=True,
        help="Model key to run from the MODELS dictionary.",
    )
    return parser.parse_args()


def get_results_db_path(model_key):
    safe_model_key = model_key.replace(":", "-").replace("/", "-")
    return RESULTS_DIR / f"{safe_model_key}-evaluation_results.sqlite"


def init_results_db(results_db_path):
    results_db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(results_db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            question TEXT,
            context TEXT,
            db_path TEXT,
            execution_result TEXT,
            expected_output TEXT,
            error TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_result(question_data, execution_result, results_db_path, error=None):
    conn = sqlite3.connect(results_db_path)
    cursor = conn.cursor()

    # Convert result to string if it's not already (handle None or objects)
    result_str = str(execution_result) if execution_result is not None else None

    cursor.execute(
        """
        INSERT INTO results (
            question_id, question, context, db_path,
            execution_result, expected_output, error
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            question_data["id"],
            question_data["question"],
            question_data["context"],
            question_data["db_path"],
            result_str,
            question_data["expected_output"],
            str(error) if error else None,
        ),
    )
    conn.commit()
    conn.close()
    print(f"Saved result for Question {question_data['id']} to {results_db_path}")


def load_questions():
    # Resolve paths relative to this script
    base_dir = Path(__file__).parent
    answers_path = base_dir / "answers.json"
    databases_dir = base_dir / "dev_20240627" / "dev_databases"

    if not answers_path.exists():
        print(f"Error: {answers_path} not found")
        return []

    print(f"Loading questions from {answers_path}...")
    with open(answers_path, "r", encoding="utf-8") as f:
        all_questions = json.load(f)

    # Filter for challenging questions
    challenging_questions = [
        q for q in all_questions if q.get("difficulty") == "challenging"
    ]
    print(f"Found {len(challenging_questions)} challenging questions.")

    questions = []
    for item in challenging_questions:
        question_id = item.get("question_id")
        question_text = item.get("question")
        context = item.get("evidence", "")
        db_id = item.get("db_id")

        db_path = databases_dir / db_id / f"{db_id}.sqlite"

        questions.append(
            {
                "id": question_id,
                "question": question_text,
                "context": context,
                "db_path": str(db_path),
                "expected_output": str(item.get("query_result", "[]")),
            }
        )

    return questions


async def run_question(item, model_name, results_db_path):
    question = item["question"]
    context = item["context"]
    db_path = item["db_path"]

    full_question = question
    if context:
        full_question = f"{question}\n\nContext: {context}"

    print(f"\n{'=' * 50}")
    print(f"Running Question {item['id']}")
    print(f"Question: {question}")
    print(f"Database: {db_path}")

    thread_manager = ThreadManager()
    options = SQLSaberOptions(
        database=db_path,
        model_name=model_name,
        thinking_enabled=True,
        thinking_level=ThinkingLevel.HIGH,
        thread_manager=thread_manager,
    )

    async with SQLSaber(options=options) as agent:
        try:
            result = await agent.query(full_question)
            save_result(item, result, results_db_path=results_db_path)
            return result
        except Exception as e:
            print(f"Error executing question {item['id']}: {e}")
            save_result(item, None, results_db_path=results_db_path, error=e)
            return None


async def main(model_key):
    model_name = MODELS[model_key]
    results_db_path = get_results_db_path(model_key)

    print(f"Running evaluations with model '{model_key}' ({model_name})")
    print(f"Results DB: {results_db_path}")

    init_results_db(results_db_path)
    questions = load_questions()

    if not questions:
        print("No questions found.")
        return

    print(f"Starting execution of {len(questions)} questions...")

    for q in questions:
        await run_question(q, model_name=model_name, results_db_path=results_db_path)


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.model))
