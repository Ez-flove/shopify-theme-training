#!/usr/bin/env bash
# Description: syntax-check every assets/*.js with node --check — Theme Check does not parse JS
#
# The theme has no build, so a syntax error in an asset ships silently and only shows as a dead
# feature in the browser. This names each broken file rather than counting them.
set -uo pipefail
cd "${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
shopt -s nullglob
files=(assets/*.js)

if [ ${#files[@]} -eq 0 ]; then
  echo "js-syntax: no assets/*.js found — nowhere to look is not the same as clean" >&2
  exit 2
fi

broken=()
for f in "${files[@]}"; do
  if ! out="$(node --check "$f" 2>&1)"; then
    broken+=("$f")
    printf '%s\n\n' "$out"
  fi
done

if [ ${#broken[@]} -eq 0 ]; then
  echo "js-syntax: clean (${#files[@]} file(s) in assets/)"
  exit 0
fi
echo "js-syntax: ${#broken[@]} file(s) do not parse"
printf '  %s\n' "${broken[@]}"
exit 1
