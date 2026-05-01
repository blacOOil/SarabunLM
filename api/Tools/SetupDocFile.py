from fpdf import FPDF
import DocFormat
import os

class SetupDocFile:

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def create_pdf(self) -> FPDF:
        # ── Setup PDF ──────────────────────────────
        pdf = FPDF("P", "mm", "A4")
        pdf.add_page()
        pdf.set_margins(DocFormat.Set_Margin_Left, DocFormat.Set_Margin_Top, DocFormat.Set_Margin_Right)
        pdf.set_auto_page_break(auto=True, margin=15)

        # ── fpdf2 add fonts (absolute path) ──────────────────────────────
        pdf.add_font("Sarabun", fname=os.path.join(self.BASE_DIR, "font\\Sarabun-Regular.ttf"))
        pdf.add_font("Sarabun", style="B", fname=os.path.join(self.BASE_DIR, "font\\Sarabun-Bold.ttf"))

        return pdf

