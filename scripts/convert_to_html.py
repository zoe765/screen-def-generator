#!/usr/bin/env python3
"""마크다운 화면정의서들을 하나의 HTML 파일로 변환

사용법:
  python3 scripts/convert_to_html.py
  python3 scripts/convert_to_html.py --project "프로젝트명"
  python3 scripts/convert_to_html.py --output /path/to/output.html
"""

import argparse
import os
import re
import sys
import webbrowser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "output")


def md_to_html(filepath):
    """마크다운 파일을 HTML로 변환"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    html_parts = []
    in_code = False
    in_table = False
    in_list = False
    list_type = None
    code_lines = []
    table_rows = []

    def close_list():
        nonlocal in_list, list_type
        if in_list:
            tag = "ol" if list_type == "ol" else "ul"
            html_parts.append(f"</{tag}>")
            in_list = False
            list_type = None

    def close_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            html_parts.append("<table>")
            for idx, row in enumerate(table_rows):
                cols = [c.strip() for c in row.strip("|").split("|")]
                cols = [c for c in cols if c is not None]
                tag = "th" if idx == 0 else "td"
                html_parts.append("<tr>")
                for c in cols:
                    c = inline_format(c)
                    html_parts.append(f"<{tag}>{c}</{tag}>")
                html_parts.append("</tr>")
            html_parts.append("</table>")
        in_table = False
        table_rows.clear()

    def inline_format(text):
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
        return text

    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\n")

        # 코드 블록
        if line.startswith("```"):
            if in_code:
                html_parts.append(
                    "<pre><code>" + "\n".join(code_lines) + "</code></pre>"
                )
                code_lines = []
                in_code = False
            else:
                close_list()
                close_table()
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            i += 1
            continue

        # 테이블
        stripped = line.strip()
        if (
            stripped.startswith("|")
            and stripped.endswith("|")
            and "|" in stripped[1:-1]
        ):
            if re.match(r"^\|[\s\-:|]+\|$", stripped):
                i += 1
                continue
            close_list()
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(stripped)

            if i + 1 < len(lines):
                next_l = lines[i + 1].rstrip("\n").strip()
                if not (next_l.startswith("|") and next_l.endswith("|")):
                    close_table()
            else:
                close_table()
            i += 1
            continue
        else:
            if in_table:
                close_table()

        # 빈 줄
        if not stripped:
            close_list()
            i += 1
            continue

        # 수평선
        if stripped == "---":
            close_list()
            html_parts.append("<hr>")
            i += 1
            continue

        # 인용
        if line.startswith(">"):
            close_list()
            text = inline_format(line.lstrip("> ").strip())
            html_parts.append(f"<blockquote>{text}</blockquote>")
            i += 1
            continue

        # 헤딩
        match = re.match(r"^(#{1,4})\s+(.*)", line)
        if match:
            close_list()
            level = len(match.group(1))
            text = inline_format(match.group(2).strip())
            html_parts.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # 리스트 (불릿)
        bmatch = re.match(r"^(\s*)[-*]\s+(.*)", line)
        if bmatch:
            text = inline_format(bmatch.group(2))
            if not in_list or list_type != "ul":
                close_list()
                html_parts.append("<ul>")
                in_list = True
                list_type = "ul"
            html_parts.append(f"<li>{text}</li>")
            i += 1
            continue

        # 숫자 리스트
        nmatch = re.match(r"^(\d+)\.\s+(.*)", line)
        if nmatch:
            text = inline_format(nmatch.group(2))
            if not in_list or list_type != "ol":
                close_list()
                html_parts.append("<ol>")
                in_list = True
                list_type = "ol"
            html_parts.append(f"<li>{text}</li>")
            i += 1
            continue

        # 일반 텍스트
        close_list()
        text = inline_format(stripped)
        html_parts.append(f"<p>{text}</p>")
        i += 1

    close_list()
    close_table()
    if in_code:
        html_parts.append("<pre><code>" + "\n".join(code_lines) + "</code></pre>")

    return "\n".join(html_parts)


def detect_project_info(output_dir):
    """output/ 폴더의 인덱스 파일에서 프로젝트명과 화면 수를 추출"""
    index_path = os.path.join(output_dir, "00_화면목록.md")
    project_name = "화면정의서"
    screen_count = 0

    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        # 프로젝트명 추출
        m = re.search(r"프로젝트:\s*(.+)", content)
        if m:
            project_name = m.group(1).strip()
        # 화면 수 추출
        m = re.search(r"총 화면 수:\s*(\d+)", content)
        if m:
            screen_count = int(m.group(1))

    if screen_count == 0:
        screen_count = len(
            [
                f
                for f in os.listdir(output_dir)
                if f.endswith(".md") and f != "00_화면목록.md" and not f.startswith(".")
            ]
        )

    return project_name, screen_count


def build_html(output_dir, project_name=None):
    """output/ 폴더의 md 파일들을 하나의 HTML로 변환"""
    index_path = os.path.join(output_dir, "00_화면목록.md")

    detected_name, screen_count = detect_project_info(output_dir)
    if not project_name:
        project_name = detected_name

    files = sorted(
        [
            f
            for f in os.listdir(output_dir)
            if f.endswith(".md") and f != "00_화면목록.md" and not f.startswith(".")
        ]
    )

    if not files:
        print("오류: output/ 폴더에 화면정의서 파일(.md)이 없습니다.")
        sys.exit(1)

    from datetime import date

    today = date.today().isoformat()

    sections = []

    # 표지
    sections.append(
        f"""
    <div class="cover">
        <h1 class="cover-title">{project_name} 화면정의서</h1>
        <p class="cover-meta">생성일: {today} · 총 {screen_count}개 화면</p>
    </div>
    """
    )

    # 인덱스
    if os.path.exists(index_path):
        sections.append('<div class="screen-section">')
        sections.append(md_to_html(index_path))
        sections.append("</div>")

    # 각 화면
    for f in files:
        filepath = os.path.join(output_dir, f)
        sections.append('<div class="screen-section">')
        sections.append(md_to_html(filepath))
        sections.append("</div>")

    body = "\n".join(sections)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{project_name} 화면정의서</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'Noto Sans KR', -apple-system, sans-serif;
    font-size: 15px;
    line-height: 1.7;
    color: #1a1a1a;
    background: #f5f5f5;
    padding: 20px;
  }}

  .cover {{
    background: linear-gradient(135deg, #4A90D9 0%, #7B68EE 100%);
    color: white;
    padding: 80px 40px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 32px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
  }}
  .cover-title {{ font-size: 42px; font-weight: 700; margin-bottom: 16px; }}
  .cover-meta {{ font-size: 14px; opacity: 0.7; }}

  .screen-section {{
    background: white;
    max-width: 900px;
    margin: 0 auto 32px;
    padding: 48px 56px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }}

  h1 {{
    font-size: 28px;
    font-weight: 700;
    color: #1a1a1a;
    margin: 0 0 8px;
    padding-bottom: 12px;
    border-bottom: 3px solid #4A90D9;
  }}
  h2 {{
    font-size: 20px;
    font-weight: 700;
    color: #2c3e50;
    margin: 36px 0 12px;
    padding: 8px 0 8px 14px;
    border-left: 4px solid #4A90D9;
  }}
  h3 {{
    font-size: 16px;
    font-weight: 600;
    color: #34495e;
    margin: 24px 0 8px;
  }}
  h4 {{
    font-size: 15px;
    font-weight: 600;
    color: #555;
    margin: 16px 0 8px;
  }}

  p {{ margin: 8px 0; }}

  blockquote {{
    color: #666;
    font-size: 14px;
    padding: 8px 16px;
    border-left: 3px solid #ddd;
    margin: 8px 0;
    background: #fafafa;
    border-radius: 0 6px 6px 0;
  }}

  hr {{
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 16px 0;
  }}

  ul, ol {{
    margin: 8px 0;
    padding-left: 24px;
  }}
  li {{
    margin: 4px 0;
    line-height: 1.7;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 14px;
  }}
  th {{
    background: #f0f4f8;
    font-weight: 600;
    text-align: left;
    padding: 10px 12px;
    border: 1px solid #ddd;
    white-space: nowrap;
  }}
  td {{
    padding: 10px 12px;
    border: 1px solid #ddd;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{
    background: #fafbfc;
  }}

  pre {{
    background: #f6f8fa;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 12px 0;
    font-size: 13px;
    line-height: 1.5;
    border: 1px solid #e8e8e8;
  }}
  code {{
    font-family: 'SF Mono', 'Fira Code', monospace;
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
  }}
  pre code {{
    background: none;
    padding: 0;
  }}

  strong {{ font-weight: 600; }}
  a {{ color: #4A90D9; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}

  @media print {{
    body {{ background: white; padding: 0; }}
    .cover {{ page-break-after: always; }}
    .screen-section {{
      box-shadow: none;
      page-break-before: always;
      padding: 24px;
      border: 1px solid #eee;
    }}
  }}
</style>
</head>
<body>
{body}
</body>
</html>"""

    return html


def main():
    parser = argparse.ArgumentParser(description="화면정의서 MD → HTML 변환")
    parser.add_argument(
        "--project", "-p", help="프로젝트명 (미지정 시 인덱스 파일에서 자동 추출)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="출력 HTML 파일 경로 (미지정 시 output/ 폴더에 저장)",
    )
    parser.add_argument(
        "--input-dir",
        "-i",
        help="화면정의서 MD 파일이 있는 폴더 (기본: ../output/)",
        default=os.path.normpath(DEFAULT_OUTPUT_DIR),
    )
    parser.add_argument(
        "--open", action="store_true", help="변환 후 브라우저에서 열기"
    )
    args = parser.parse_args()

    output_dir = os.path.normpath(args.input_dir)
    if not os.path.isdir(output_dir):
        print(f"오류: 폴더를 찾을 수 없습니다: {output_dir}")
        sys.exit(1)

    html = build_html(output_dir, args.project)

    # 출력 경로 결정
    if args.output:
        html_path = args.output
    else:
        project_name = args.project or detect_project_info(output_dir)[0]
        safe_name = re.sub(r"[^\w가-힣]", "_", project_name)
        html_path = os.path.join(output_dir, f"{safe_name}_화면정의서.html")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"변환 완료: {html_path}")
    print(f"Google Docs로 옮기려면:")
    print(f"  1. 브라우저에서 파일 열기")
    print(f"  2. Cmd+A (전체 선택) → Cmd+C (복사)")
    print(f"  3. Google Docs에서 Cmd+V (붙여넣기)")

    if args.open:
        webbrowser.open(f"file://{os.path.abspath(html_path)}")


if __name__ == "__main__":
    main()
