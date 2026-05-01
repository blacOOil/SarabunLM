Doc_format = "ResearchPaper" 
FormatPromting = "Not Available"

Section_Number = 5
Section_Name = {"1": "Introduction", "2": "Methodology", "3": "Results", "4": "Discussion", "5": "Conclusion"}
# Document Format Property
SetFont_Family = "Sarabun"
SetFont_Size = 16
SetFont_Style = "B"
SetText_Transform = ""

#Paragraph Properties
Text_Alignment ="Justify"

Paragraph_Spacing_Before = 0
Paragraph_Spacing_After = 0
Line_Spacing = 1.5

Indentation_Left = 0
Indentation_Right = 0
First_Line_Indent = 1.25

Set_Margin_Left = 38
Set_Margin_Right = 25
Set_Margin_Top = 25
Set_Margin_Bottom = 25

if Doc_format == "Default":
  SetFont_Family = "Sarabun"
  SetFont_Size = 12
elif  Doc_format == "B":
  SetFont_Family = "Sarabun"
  SetFont_Size = 14
elif Doc_format == "ResearchPaper":
  SetFont_Family = "Sarabun"
  SetFont_Size = 10
  SetFont_Style = "B"
  Set_Margin_Left = 38.1
  Set_Margin_Right = 25.4
  Set_Margin_Top = 25.4
  FormatPromting = "answers with the same language of the question & act as a professional researcher and output to following question as you writing a rearching report so the question is :"