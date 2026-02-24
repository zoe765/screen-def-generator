#!/bin/bash
# convert_docx.sh — input/ 폴더의 .docx 파일을 .txt로 변환 (macOS textutil 사용)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INPUT_DIR="$SCRIPT_DIR/../input"

if [ ! -d "$INPUT_DIR" ]; then
  echo "오류: input/ 폴더를 찾을 수 없습니다."
  exit 1
fi

found=0
for docx_file in "$INPUT_DIR"/*.docx; do
  [ -f "$docx_file" ] || continue
  found=1
  txt_file="${docx_file%.docx}.txt"
  echo "변환 중: $(basename "$docx_file") → $(basename "$txt_file")"
  textutil -convert txt "$docx_file" -output "$txt_file"
done

if [ $found -eq 0 ]; then
  echo "input/ 폴더에 .docx 파일이 없습니다."
  exit 0
fi

echo "변환 완료."
