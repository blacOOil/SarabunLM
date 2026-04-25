Doc_format = "ResearchPaper" 
FormatPromting = ""

Section_Number = 0
Section_Name = ""
# Document Format Property
SetFont_Family = ""
SetFont_Size = 0
SetFont_Style = ""
SetText_Transform = ""

#Paragraph Properties
Text_Alignment =""
Paragraph_Spacing_Before = 0
Paragraph_Spacing_After = 0
Line_Spacing = 0
Indentation_Left = 0
Indentation_Right = 0
First_Line_Indent = 0
Set_Margin_Left = 15
Set_Margin_Right = 15
Set_Margin_Top = 15
Set_Margin_Bottom = 15

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