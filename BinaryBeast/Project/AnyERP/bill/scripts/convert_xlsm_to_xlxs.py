import win32com.client as win32

excel = win32.gencache.EnsureDispatch('Excel.Application')

# Load the .XLSM file into Excel
wb = excel.Workbooks.Open(r'C:\Users\bashi\Jupyter\INV036.xlsm')

# Save it in .XLSX format to a different filename
excel.DisplayAlerts = False
wb.DoNotPromptForConvert = True
wb.CheckCompatibility = False
wb.SaveAs(r"C:\Users\bashi\Jupyter\test5.xlsx", FileFormat=51, ConflictResolution=2)
excel.Application.Quit()