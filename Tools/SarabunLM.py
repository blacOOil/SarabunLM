import importlib
import fpdf
import DocFormat
import SetupDocFile

importlib.reload(DocFormat)
importlib.reload(fpdf)
print("fpdf version:", fpdf.__version__)
print("DocFormat version:", DocFormat.Doc_format)
setup_doc_file = SetupDocFile.SetupDocFile()
pdf = setup_doc_file.create_pdf()
