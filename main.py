import pandas as pd
import glob
import re
from fpdf import FPDF

filepaths = glob.glob("Invoices/*.xlsx")

for filepath in filepaths:

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    invoice_number = re.search(r"\d{5}", filepath).group()
    date = re.search(r"\d{4}\.\d*.\d{2}", filepath).group()

    pdf.set_font(family="Times", style="B", size=16)
    pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_number}", align="L", ln=1)
    pdf.cell(w=50, h=8, txt=f"Date: {date}", align="L", ln=1)
    pdf.cell(w=50, h=8, ln=1)
    df = pd.read_excel(filepath, sheet_name="Sheet 1")

    # Add a header
    columns = list(df.columns)
    columns = [item.replace("_", " ").title() for item in columns]
    pdf.set_font(family="Times", size=10, style="B")
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt=columns[0].replace("Id", "ID"), border=1)
    pdf.cell(w=70, h=8, txt=columns[1], border=1)
    pdf.cell(w=30, h=8, txt=columns[2][:6], border=1)
    pdf.cell(w=30, h=8, txt=columns[3], border=1)
    pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

    # Add rows to the table
    for index, row in df.iterrows():
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
        pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

    total_sum = df["total_price"].sum()
    pdf.set_font(family="Times", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=70, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

    pdf.cell(w=0, h=10, ln=1)
    # Add total sum sentence
    pdf.set_font(family="Times", size=10, style="B")
    pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)

    # Add company name and logo
    pdf.set_font(family="Times", size=14, style="B")
    pdf.cell(w=25, h=8, txt=f"PythonHow")
    pdf.image("pythonhow.png", w=10)

    pdf.output(f"PDFs/{invoice_number}-{date}.pdf")
