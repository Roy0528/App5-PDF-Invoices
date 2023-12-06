import pandas as pd
import glob
import re
from fpdf import FPDF

filepaths = glob.glob("Invoices/*.xlsx")

for filepath in filepaths:
    df = pd.read_excel(filepath, sheet_name="Sheet 1")
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    invoice_number = re.search(r"\d{5}", filepath).group()
    date = re.search(r"\d{4}\.\d*.\d{2}", filepath).group()

    pdf.set_font(family="Times", style="B", size=16)
    pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_number}", align="L", ln=1)
    pdf.cell(w=0, h=8, txt=f"Date {date}", align="L", ln=1)

    pdf.output(f"PDFs/{invoice_number}-{date}.pdf")

