from fpdf import FPDF
from datetime import datetime
import io


class ComplianceReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(15, 40, 90)
        self.cell(0, 10, "Delta Node Advisory, LLC", ln=True, align="C")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "AI-Powered Trade Compliance Intelligence", ln=True, align="C")
        self.ln(4)
        self.set_draw_color(15, 40, 90)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Delta Node Advisory, LLC | Page {self.page_no()}", align="C")


def generate_client_report(client_name, contact_name, category, df):
    pdf = ComplianceReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title block
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Trade Compliance & Risk Brief", ln=True, align="L")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, f"Prepared for: {client_name}", ln=True)
    pdf.cell(0, 6, f"Attention: {contact_name}", ln=True)
    pdf.cell(0, 6, f"Product Category: {category}", ln=True)
    pdf.cell(0, 6, f"Date Issued: {datetime.now().strftime('%B %d, %Y')}", ln=True)
    pdf.ln(4)

    # Executive summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 40, 90)
    pdf.cell(0, 8, "Executive Summary", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 5,
        f"This brief summarizes active US trade actions and regulatory notices "
        f"affecting Egyptian imports in the {category.lower()} category as of "
        f"{datetime.now().strftime('%B %d, %Y')}. All data is sourced from the "
        f"US Federal Register (public domain)."
    )
    pdf.ln(3)

    # Data table
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(15, 40, 90)
    pdf.cell(0, 8, "Active Trade Actions", ln=True)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(15, 40, 90)

    col_widths = [22, 25, 42, 101]
    headers = ["Date", "Type", "Agency", "Title"]
    for w, h in zip(col_widths, headers):
        pdf.cell(w, 7, h, border=1, fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(0, 0, 0)

    fill = False
    for _, row in df.iterrows():
        pdf.set_fill_color(240, 245, 250) if fill else pdf.set_fill_color(255, 255, 255)

        title = str(row.get("Title", ""))[:90]
        pdf.cell(22, 6, str(row.get("Date", ""))[:10], border=1, fill=fill)
        pdf.cell(25, 6, str(row.get("Type", ""))[:12], border=1, fill=fill)
        pdf.cell(42, 6, str(row.get("Agency", ""))[:22], border=1, fill=fill)
        pdf.cell(101, 6, title, border=1, fill=fill)
        pdf.ln()
        fill = not fill

    pdf.ln(5)

    # Risk assessment
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(15, 40, 90)
    pdf.cell(0, 8, "Risk Assessment", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    risk_text = (
        f"{len(df)} active trade actions currently affect the {category.lower()} category "
        f"for Egyptian imports. Importers in this category should review the actions listed "
        f"above to assess potential tariff exposure, compliance requirements, and documentation "
        f"obligations. Products under countervailing duty or antidumping investigations may face "
        f"retroactive liability if not properly documented."
    )
    pdf.multi_cell(0, 5, risk_text)
    pdf.ln(4)

    # Recommendations
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(15, 40, 90)
    pdf.cell(0, 8, "Recommended Next Steps", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    recommendations = [
        "1. Verify supplier compliance documentation against the actions listed above.",
        "2. Confirm QIZ eligibility if applicable (minimum 10% Israeli content).",
        "3. Monitor the Federal Register weekly for changes to active cases.",
        "4. Consider engaging a customs broker to review classification and duty exposure.",
        "5. Schedule an on-site supplier audit through Delta Node Advisory's Egypt-based partner.",
    ]
    for rec in recommendations:
        pdf.multi_cell(0, 5, rec)

    pdf.ln(6)

    # Contact block
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 40, 90)
    pdf.cell(0, 6, "Contact", ln=True)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, "Delta Node Advisory, LLC", ln=True)
    pdf.cell(0, 5, "Email: info@deltanodeadvisory.com", ln=True)
    pdf.cell(0, 5, "Wyoming Registered | Serving US Importers Sourcing from Egypt", ln=True)

    return bytes(pdf.output())
