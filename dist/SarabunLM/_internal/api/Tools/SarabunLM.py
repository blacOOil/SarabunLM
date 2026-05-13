import importlib
import re
import sys
import fpdf
import DocFormat
import SetupDocFile
import Ultility
import os

importlib.reload(DocFormat)
importlib.reload(fpdf)
print("fpdf version:", fpdf.__version__)
print("DocFormat version:", DocFormat.Doc_format)

setup_doc_file = SetupDocFile.SetupDocFile()
pdf = setup_doc_file.create_pdf()

# ── Read ENV vars ────────────────────────────────────────────
ai_output    = os.environ.get("AI_OUTPUT", "")
template_key = os.environ.get("TEMPLATE_KEY", "Default")

if not ai_output:
    print("ERROR: No AI_OUTPUT provided.")
    sys.exit(1)

# ── Parse sections from AI_OUTPUT ───────────────────────────
# Format: "[HEADER]\ncontent\n\n[BODY]\ncontent..."
sections = []
for block in ai_output.split('\n\n'):
    block = block.strip()
    if not block:
        continue
    lines = block.split('\n', 1)
    if len(lines) == 2 and lines[0].startswith('[') and lines[0].endswith(']'):
        section_type    = lines[0].strip('[]').lower()  # "header", "body", "footer"
        section_content = lines[1].strip()
    else:
        # No type tag — treat entire block as body
        section_type    = "body"
        section_content = block

    sections.append({"type": section_type, "content": section_content})

print(f"Template   : {template_key}")
print(f"Sections   : {len(sections)}")

# ── Bold writer (unchanged) ──────────────────────────────────
def write_line_with_bold(pdf, line, line_height=8):
    segments = re.split(r'(\*\*)', line)
    bold = False
    for segment in segments:
        if segment == '**':
            bold = not bold
            continue
        if not segment:
            continue
        font_style = "B" if bold else ""
        pdf.set_font(DocFormat.SetFont_Family, style=font_style, size=DocFormat.SetFont_Size)
        pdf.write(line_height, segment)
    pdf.ln(line_height)

# ── Section writers ──────────────────────────────────────────
def write_header(pdf, content):
    pdf.set_font(DocFormat.SetFont_Family, style="B", size=DocFormat.SetFont_Size + 4)
    pdf.cell(0, 12, content, ln=True, align="C")   # Centered bold header
    pdf.ln(4)

def write_body(pdf, content):
    pdf.add_page()
    for line in content.split("\n"):
        if line.strip() == "":
            pdf.ln(5)
        else:
            write_line_with_bold(pdf, line)

def write_footer(pdf, content):
    pdf.set_font(DocFormat.SetFont_Family, style="I", size=DocFormat.SetFont_Size - 2)
    pdf.ln(10)
    pdf.cell(0, 8, content, ln=True, align="C")    # Centered italic footer

# ── Pre-body (cover page etc.) ───────────────────────────────
if DocFormat.Section_Number > 0:
    print(f"Section {DocFormat.Section_Number}: {DocFormat.Section_Name}")

if template_key == "ResearchPaper" or DocFormat.Doc_format == "ResearchPaper":
    Ultility.Generate_text_coverpage(pdf)
    Ultility.Generate_text_content(pdf)

# ── Render each section ──────────────────────────────────────
for i, section in enumerate(sections):
    stype   = section["type"]
    content = section["content"]
    print(f"  Rendering [{stype}]: {content[:60]}...")

    if stype == "header":
        write_header(pdf, content)
    elif stype == "footer":
        write_footer(pdf, content)
    else:
        write_body(pdf, content)   # default → body

# ── Save output ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(BASE_DIR, "LLM", "DataStorage", "outputs")
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "output.pdf")
pdf.output(output_path)
print("Saved to:", output_path)