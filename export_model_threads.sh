#!/usr/bin/env bash

set -euo pipefail

DEFAULT_MODEL="gemini-3.1-pro-preview"
DEFAULT_OUTPUT_DIR="threads"
DEFAULT_LIMIT="10000"

model="$DEFAULT_MODEL"
output_dir="$DEFAULT_OUTPUT_DIR"
limit="$DEFAULT_LIMIT"
database=""

usage() {
  cat <<'EOF'
Usage: ./export_model_threads.sh [options]

Export SQLsaber threads for a specific model to HTML and Markdown.

Options:
  -m, --model MODEL          Model name to match (default: gemini-3.1-pro-preview)
  -o, --output-dir DIR       Output directory (default: threads)
  -n, --limit N              Max threads to scan from `saber threads list` (default: 10000)
  -d, --database NAME        Optional database filter for list/show/export
  -h, --help                 Show this help

Examples:
  ./export_model_threads.sh
  ./export_model_threads.sh --model gemini-3.1-pro-preview --output-dir threads
  ./export_model_threads.sh -d student_club --limit 500
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -m|--model)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for $1" >&2
        exit 1
      fi
      model="$2"
      shift 2
      ;;
    -o|--output-dir)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for $1" >&2
        exit 1
      fi
      output_dir="$2"
      shift 2
      ;;
    -n|--limit)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for $1" >&2
        exit 1
      fi
      limit="$2"
      shift 2
      ;;
    -d|--database)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for $1" >&2
        exit 1
      fi
      database="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

mkdir -p "$output_dir"

list_cmd=(saber threads list --limit "$limit")
if [[ -n "$database" ]]; then
  list_cmd+=(--database "$database")
fi

echo "Listing threads (limit=$limit)..."
thread_ids="$("${list_cmd[@]}" | rg -o '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | sort -u || true)"

if [[ -z "$thread_ids" ]]; then
  echo "No thread IDs found."
  exit 0
fi

scanned=0
exported=0

while IFS= read -r thread_id; do
  [[ -z "$thread_id" ]] && continue
  scanned=$((scanned + 1))

  show_cmd=(saber threads show)
  if [[ -n "$database" ]]; then
    show_cmd+=(--database "$database")
  fi
  show_cmd+=("$thread_id")

  header="$(COLUMNS=240 "${show_cmd[@]}" | sed -n '1,20p')"
  thread_model="$(printf '%s\n' "$header" | awk -F': ' '/^Model:/ {print $2; exit}')"

  if [[ "$thread_model" != "$model" ]]; then
    continue
  fi

  html_path="$output_dir/${thread_id}.html"
  md_path="$output_dir/${thread_id}.md"

  export_cmd=(saber threads export)
  if [[ -n "$database" ]]; then
    export_cmd+=(--database "$database")
  fi
  export_cmd+=("$thread_id" --output "$html_path")

  echo "Exporting thread $thread_id"
  "${export_cmd[@]}"

  # Intentionally uses a pipe so markdown goes through stdout before file write.
  COLUMNS=240 "${show_cmd[@]}" | tee "$md_path" >/dev/null

  exported=$((exported + 1))
done <<< "$thread_ids"

echo "Done. Scanned $scanned thread(s); exported $exported thread(s) for model '$model' into '$output_dir/'."
