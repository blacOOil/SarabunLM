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
ai_output = "Test **bold** and normal text.\nNew line with **bold** word.\nAnother line without bold."

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


# Pre Body Output
if DocFormat.Section_Number > 0:
     print (f"Section {DocFormat.Section_Number}: {DocFormat.Section_Name}")     
if DocFormat.Doc_format == "ResearchPaper":
        Ultility.Generate_text_coverpage(pdf)
        Ultility.Generate_text_content(pdf)
# ── Body (AI Output) ────────────────────
pdf.add_page()
for line in ai_output.split("\n"):
    if line.strip() == "":
        pdf.ln(5)
    else:
        write_line_with_bold(pdf, line)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(BASE_DIR, "LLM","DataStorage", "outputs")
os.makedirs(output_folder, exist_ok=True)
pdf.output(os.path.join(output_folder, "output.pdf"))
print("Saved to:", os.path.join(output_folder, "output.pdf"))
