#!/bin/bash
function get_relative_path() {
  local root=$1
  local full_path=$2
  echo ${full_path#*$root}
}

function compile() {
  local path=$1
  local entrypoint=${2:-"main"}
  local root=${3:-"^"}
  local output="${path%.*}.tz"
  local filename=$(basename $path)
  local pp_file="${PWD}/${filename%.*}.pp.ligo"

  # ... log
  bash ./scripts/print.sh h2 "Compiling Ligo smart contract ..." "LIGHT_GREY"; echo ""
  bash ./scripts/print.sh h2 "<" "GREY"
  bash ./scripts/print.sh h3 "$(get_relative_path $root $path)"; echo ""

  # ... compile .ligo file and output to .tz file
  ligo compile-contract "${path}" "${entrypoint}" --michelson-format="text" > "${output}"

  # ... remove .pp.ligo that ligo creates
  if [[ -f "${pp_file}" ]]; then
    rm -f $pp_file
  fi

  # ... log
  bash ./scripts/print.sh h2 ">" "GREY"
  bash ./scripts/print.sh h3 "$(get_relative_path $root $output)"; echo ""
}

function compile_all() {
  local root=$1
  # ... log
  bash ./scripts/print.sh h1 "Compiling Ligo smart contracts ..."; echo ""
  bash ./scripts/print.sh h3 "${root}"; echo ""

  # ... compile all .ligo files in root
  for path in $(find $root -name "*.ligo" -type f); do
    compile $path "main" $root
  done
}

function compile_all_watch() {
  local root=$1
  # ... log
  bash ./scripts/print.sh h1 "Compiling Ligo smart contracts on change ..."; echo ""
  bash ./scripts/print.sh h3 "${root}"; echo ""

  # ... watch all .ligo files in root and compile when they change
  fswatch -e ".*" -i "\\.ligo$" -0 $root | while read -d "" full_path; do
    compile $full_path "main" $root
  done
}

"$@"
