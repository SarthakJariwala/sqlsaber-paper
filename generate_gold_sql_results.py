"""
Execute "Gold" SQL queries from dev.json against their respective SQLite databases
and save results to answers.json
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, List


def execute_query(db_path: Path, sql: str) -> tuple[List[Any], str | None]:
    """
    Execute a SQL query against the database and return results.

    Returns:
        Tuple of (results, error_message)
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return results, None
    except Exception as e:
        return [], str(e)


def main():
    base_dir = Path(__file__).parent / "dev_20240627"
    dev_json_path = base_dir / "dev.json"
    output_json_path = Path(__file__).parent / "answers.json"
    databases_dir = base_dir / "dev_databases"

    if not dev_json_path.exists():
        print(f"Error: {dev_json_path} not found")
        sys.exit(1)

    if not databases_dir.exists():
        print(f"Error: {databases_dir} not found")
        sys.exit(1)

    print(f"Loading questions from {dev_json_path}...")
    with open(dev_json_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    total = len(questions)
    print(f"Found {total} questions to process\n")

    answers = []
    success_count = 0
    error_count = 0
    start_time = datetime.now()

    for idx, item in enumerate(questions, 1):
        question_id = item.get("question_id")
        db_id = item.get("db_id")
        sql = item.get("SQL")

        print(
            f"[{idx}/{total}] Processing question_id={question_id}, db_id={db_id}...",
            end=" ",
        )

        db_path = databases_dir / db_id / f"{db_id}.sqlite"

        if not db_path.exists():
            print(f"❌ Database not found: {db_path}")
            answer_item = {
                **item,
                "query_result": None,
                "error": f"Database not found: {db_path}",
            }
            error_count += 1
        else:
            results, error = execute_query(db_path, sql)

            if error:
                print(f"❌ Error: {error}")
                answer_item = {**item, "query_result": None, "error": error}
                error_count += 1
            else:
                print(f"✓ Success ({len(results)} rows)")
                answer_item = {**item, "query_result": results, "error": None}
                success_count += 1

        answers.append(answer_item)

        if idx % 10 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            avg_time = elapsed / idx
            remaining = (total - idx) * avg_time
            print(
                f"  Progress: {idx}/{total} ({idx / total * 100:.1f}%) | "
                f"Success: {success_count} | Errors: {error_count} | "
                f"ETA: {remaining:.1f}s"
            )

    print(f"\n{'=' * 80}")
    print(f"Saving results to {output_json_path}...")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2, ensure_ascii=False)

    elapsed_time = (datetime.now() - start_time).total_seconds()
    print("\n✅ Complete!")
    print(f"  Total queries: {total}")
    print(f"  Successful: {success_count}")
    print(f"  Errors: {error_count}")
    print(f"  Time elapsed: {elapsed_time:.2f}s")
    print(f"  Average time per query: {elapsed_time / total:.3f}s")
    print(f"  Output saved to: {output_json_path}")


if __name__ == "__main__":
    main()
