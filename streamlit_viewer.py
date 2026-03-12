import argparse
import json
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--results-db",
        type=Path,
        help="Path to the evaluation results SQLite database.",
    )
    args, _ = parser.parse_known_args()
    return args


def resolve_results_db_path(results_db_arg):
    db_path = results_db_arg.expanduser()
    if not db_path.is_absolute():
        db_path = (Path.cwd() / db_path).resolve()
    return db_path


def init_db(results_db_path):
    conn = sqlite3.connect(results_db_path)
    cursor = conn.cursor()
    # Add grading columns if they don't exist
    try:
        cursor.execute("ALTER TABLE results ADD COLUMN is_correct BOOLEAN")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE results ADD COLUMN grading_notes TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


def load_results(results_db_path):
    conn = sqlite3.connect(results_db_path)
    df = pd.read_sql_query("SELECT * FROM results", conn)
    conn.close()
    return df


def update_grading(result_id, is_correct, notes, results_db_path):
    conn = sqlite3.connect(results_db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE results
        SET is_correct = ?, grading_notes = ?
        WHERE id = ?
    """,
        (is_correct, notes, result_id),
    )
    conn.commit()
    conn.close()


def main():
    st.set_page_config(page_title="SQLSaber Evaluation Viewer", layout="wide")
    st.title("SQLSaber Evaluation Viewer")

    args = parse_args()
    if not args.results_db:
        st.error("Missing required argument: --results-db")
        st.code(
            "streamlit run streamlit_viewer.py -- --results-db results/gpt-5.3-codex-evaluation_results.sqlite"
        )
        st.stop()

    results_db_path = resolve_results_db_path(args.results_db)
    if not results_db_path.exists():
        st.error(f"Results DB not found: {results_db_path}")
        st.stop()

    st.caption(f"Results DB: `{results_db_path}`")

    init_db(results_db_path)

    # Load data
    df = load_results(results_db_path)

    if df.empty:
        st.warning("No results found in database.")
        return

    # Sidebar for navigation
    st.sidebar.header("Navigation")

    # Filter options
    filter_status = st.sidebar.radio(
        "Filter by Status", ["All", "Ungraded", "Correct", "Incorrect"]
    )

    filtered_df = df.copy()
    if filter_status == "Ungraded":
        filtered_df = filtered_df[filtered_df["is_correct"].isna()]
    elif filter_status == "Correct":
        filtered_df = filtered_df[filtered_df["is_correct"] == 1]
    elif filter_status == "Incorrect":
        filtered_df = filtered_df[filtered_df["is_correct"] == 0]

    st.sidebar.text(f"Showing {len(filtered_df)} / {len(df)} results")

    if len(filtered_df) == 0:
        st.info("No results match the current filter.")
        return

    # Allow selecting a specific question result to grade
    # Use session state to handle programmatic selection updates
    if "selected_idx" not in st.session_state:
        st.session_state["selected_idx"] = filtered_df.index[0]

    # Ensure selected_idx is valid for current filter
    if st.session_state["selected_idx"] not in filtered_df.index:
        st.session_state["selected_idx"] = filtered_df.index[0]

    selected_idx = st.sidebar.selectbox(
        "Select Question",
        filtered_df.index,
        format_func=lambda x: (
            f"ID: {filtered_df.loc[x, 'question_id']} (Result #{filtered_df.loc[x, 'id']})"
        ),
        index=list(filtered_df.index).index(st.session_state["selected_idx"]),
    )
    st.session_state["selected_idx"] = selected_idx

    row = filtered_df.loc[selected_idx]

    # Display content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Question {row['question_id']}")
        st.markdown(f"**Question:** {row['question']}")

        if row["context"]:
            st.info(f"**Context:**\n\n{row['context']}")

        st.markdown("---")

        st.subheader("Expected Output")
        try:
            # Parse JSON if it's a string
            expected_json = (
                json.loads(row["expected_output"])
                if isinstance(row["expected_output"], str)
                else row["expected_output"]
            )

            if isinstance(expected_json, list):
                # Convert to DataFrame for nicer display
                if expected_json and isinstance(expected_json[0], (list, dict)):
                    st.dataframe(pd.DataFrame(expected_json), use_container_width=True)
                else:
                    # Simple list
                    st.dataframe(
                        pd.DataFrame(expected_json, columns=["Value"]),
                        use_container_width=True,
                    )
            else:
                st.code(row["expected_output"], language="json")
        except Exception:
            st.code(row["expected_output"], language="json")

        st.subheader("Execution Result")
        if row["error"]:
            st.error(f"Error:\n{row['error']}")
        else:
            try:
                # Try to pretty print JSON results if possible
                res_json = row["execution_result"]

                if isinstance(res_json, list):
                    # Convert to DataFrame for nicer display
                    if res_json and isinstance(res_json[0], (list, dict)):
                        st.dataframe(pd.DataFrame(res_json), width="stretch")
                    else:
                        # Simple list
                        st.dataframe(
                            pd.DataFrame(res_json, columns=["Value"]), width="stretch"
                        )
                elif isinstance(res_json, dict):
                    st.code(json.dumps(res_json, indent=2), language="json")
                else:
                    st.markdown(row["execution_result"])
            except Exception:
                # Fallback to raw string
                st.code(row["execution_result"])

    with col2:
        st.subheader("Grading")

        # Navigation buttons
        nav_col1, nav_col2 = st.columns(2)

        # Find current position in filtered list
        current_pos = list(filtered_df.index).index(selected_idx)

        with nav_col1:
            if current_pos > 0:
                prev_idx = filtered_df.index[current_pos - 1]
                if st.button("← Previous", use_container_width=True):
                    st.session_state["selected_idx"] = prev_idx
                    st.rerun()

        with nav_col2:
            if current_pos < len(filtered_df) - 1:
                next_idx = filtered_df.index[current_pos + 1]
                if st.button("Next →", use_container_width=True):
                    st.session_state["selected_idx"] = next_idx
                    st.rerun()

        st.markdown("---")

        with st.form(key=f"grading_form_{row['id']}"):
            current_correct = row["is_correct"]
            # Convert 1/0/None to boolean for default index
            default_idx = 0

            # Important: row["is_correct"] could be 1.0/0.0 (floats) from pandas
            if current_correct == 1:
                default_idx = 1
            elif current_correct == 0 and pd.notna(current_correct):
                default_idx = 2

            status = st.radio(
                "Is the result correct?",
                ["Ungraded", "Correct", "Incorrect"],
                index=default_idx,
            )

            notes = st.text_area(
                "Notes", value=row["grading_notes"] if row["grading_notes"] else ""
            )

            submit = st.form_submit_button("Update Grading", use_container_width=True)

            if submit:
                is_correct = None
                if status == "Correct":
                    is_correct = 1
                elif status == "Incorrect":
                    is_correct = 0

                update_grading(
                    int(row["id"]),
                    is_correct,
                    notes,
                    results_db_path=results_db_path,
                )
                st.success("Grading updated!")

                # Auto-advance to next if available
                if current_pos < len(filtered_df) - 1:
                    next_idx = filtered_df.index[current_pos + 1]
                    st.session_state["selected_idx"] = next_idx

                st.rerun()

    # Summary metrics
    st.markdown("---")
    st.subheader("Summary Stats")
    total = len(df)
    graded = df["is_correct"].notna().sum()
    correct = df[df["is_correct"] == 1].shape[0]
    incorrect = df[df["is_correct"] == 0].shape[0]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total", total)
    m2.metric("Graded", f"{graded} ({graded / total:.1%})" if total > 0 else 0)
    m3.metric("Correct", f"{correct} ({correct / graded:.1%})" if graded > 0 else 0)
    m4.metric("Incorrect", incorrect)


if __name__ == "__main__":
    main()
