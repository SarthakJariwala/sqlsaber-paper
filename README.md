# SQLSaber Benchmark

Benchmark evaluation of [SQLSaber](https://github.com/sarthakjariwala/sqlsaber) on the [BIRD-SQL](https://bird-bench.github.io/) dev dataset (challenging subset) for ACM CAIS.

## Repository Structure

```
results-evals/          # Evaluation run results (SQLite DBs per model)
threads/                # Exported conversation threads from eval runs for all models
threads.db              # Raw conversations stored in a SQLite database
incorrect-gold-sql-analaysis/  # Analysis of questions where BIRD gold SQL is incorrect
analysis/               # Tool call and execution time analysis for benchmark runs
answers.json            # Gold SQL and execution results (regenerate with generate_gold_sql_results.py)
```

## Reproducing the Benchmark

### 1. Prerequisites

- Download the BIRD dev SQL dataset from https://bird-bench.github.io/ and place it under `dev_20240627/`
- Clone this repo
- Install [uv](https://docs.astral.sh/uv/)

### 2. Set up the environment

```bash
uv sync
```

### 3. Set API keys

Export API keys for the model providers you want to evaluate:

```bash
export ANTHROPIC_API_KEY="..."
export OPENAI_API_KEY="..."
export GOOGLE_API_KEY="..."
```

### 4. Run evaluations

```bash
uv run run_evals.py --model <model_key>
```

Available model keys: `gpt-5.3-codex`, `opus-4-6`, `gemini-3.1-pro`

### 5. Export conversation threads

After a run, export the conversation threads using:

```bash
./export_model_threads.sh [options]
```

| Option | Description | Default |
|---|---|---|
| `-m, --model MODEL` | Model name to match | `gemini-3.1-pro-preview` |
| `-o, --output-dir DIR` | Output directory | `threads` |
| `-n, --limit N` | Max threads to scan | `10000` |
| `-d, --database NAME` | Optional database filter | — |

**Examples:**

```bash
./export_model_threads.sh
./export_model_threads.sh --model gemini-3.1-pro-preview --output-dir threads
./export_model_threads.sh -d student_club --limit 500
```

## Viewing & Grading Results

Use the Streamlit viewer to inspect and grade evaluation results:

```bash
uv run streamlit run streamlit_viewer.py -- --results-db results-evals/<model>-evaluation_results.sqlite
```

For example:

```bash
uv run streamlit run streamlit_viewer.py -- --results-db results-evals/gpt-5.3-codex-evaluation_results.sqlite
```
