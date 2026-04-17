import importlib
import re
import fpdf
import DocFormat
import SetupDocFile
import Ultility

importlib.reload(DocFormat)
importlib.reload(fpdf)
print("fpdf version:", fpdf.__version__)
print("DocFormat version:", DocFormat.Doc_format)
setup_doc_file = SetupDocFile.SetupDocFile()
pdf = setup_doc_file.create_pdf()
ai_output = "This is the AI output. **This line should not be bold. **Another bold line.**"

def Generate_pdf_coverpage(pdf):
    pdf.set_font(DocFormat.SetFont_Family, style="B", size=24)
    pdf.ln(80)
    pdf.multi_cell(0, 10, Ultility.Generate_text_coverpage(), align="C", ln=True)
    pdf.ln(5)

def Generate_pdf_content(pdf):
      pdf.add_page()
      pdf.set_font(DocFormat.SetFont_Family, style=DocFormat.SetFont_Style, size=DocFormat.SetFont_Size)
      pdf.multi_cell(50, 10, "content\n", ln=True)
      pdf.multi_cell(50, 10, Ultility.Generate_text_content(), ln=True)
      pdf.ln(5)

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
if DocFormat.Doc_format == "ResearchPaper":
        Generate_pdf_coverpage(pdf)
        Generate_pdf_content(pdf)
# ── Body (AI Output) ────────────────────
pdf.add_page()
for line in ai_output.split("\n"):
    if line.strip() == "":
        pdf.ln(5)
    else:
        write_line_with_bold(pdf, line)


pdf.output("output.pdf")
