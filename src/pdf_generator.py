from fpdf import FPDF
import datetime

class FabricPDF(FPDF):
    def header(self):
        # Top Logo/Title area
        self.set_fill_color(46, 64, 83) # Dark Navy
        self.rect(0, 0, 210, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 16)
        self.cell(0, 20, "FABRIC INTEL AI - TECHNICAL SPEC SHEET", ln=True, align="C")
        self.set_font("helvetica", "I", 10)
        self.cell(0, -5, f"Industrial Grade Report | Generated: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
        self.ln(20)

    def draw_metric_bar(self, label, value):
        # Draw a visual bar chart inside the PDF
        self.set_text_color(0, 0, 0)
        self.set_font("helvetica", "B", 10)
        self.cell(40, 10, f"{label}:", ln=False)
        
        # Background Bar
        self.set_fill_color(240, 240, 240)
        self.rect(50, self.get_y() + 2, 100, 6, "F")
        
        # Value Bar (Blue)
        self.set_fill_color(46, 64, 83)
        self.rect(50, self.get_y() + 2, max(value, 5), 6, "F")
        
        self.set_x(155)
        self.cell(20, 10, f"{value}/100", ln=True)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Proprietary Textile Intelligence Stack - Page {self.page_no()}", align="C")

def export_to_pdf(text, metrics=None):
    pdf = FabricPDF()
    pdf.add_page()
    
    # 1. Visual Charts Section (If metrics exist)
    if metrics:
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(46, 64, 83)
        pdf.cell(0, 10, "PERFORMANCE ARCHITECTURE", ln=True)
        pdf.ln(2)
        pdf.draw_metric_bar("Durability", metrics.get("DUR", 0))
        pdf.draw_metric_bar("Breathability", metrics.get("BRE", 0))
        pdf.draw_metric_bar("Eco-Score", metrics.get("SUS", 0))
        pdf.draw_metric_bar("Cost Efficiency", metrics.get("COST", 0))
        pdf.ln(10)

    # 2. Market Placement & Buyer Matching
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(211, 84, 0) # Orange tone for market data
    pdf.cell(0, 10, "INDIAN MARKET PLACEMENT", ln=True)
    pdf.set_font("helvetica", "I", 10)
    
    # Extract just the market intelligence part for a special box
    market_info = "Market analysis included in the technical breakdown below."
    if "MARKET INTELLIGENCE" in text:
        market_info = text.split("MARKET INTELLIGENCE")[1].split("6.")[0].strip()
    
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, txt=market_info.encode('latin-1', 'replace').decode('latin-1'), border=1)
    pdf.ln(5)

    # 3. Main Technical Report
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(46, 64, 83)
    pdf.cell(0, 10, "PRODUCTION ANALYSIS", ln=True)
    pdf.set_font("helvetica", size=10)
    pdf.set_text_color(0, 0, 0)
    
    clean_text = text.split("METRIC_DATA:")[0]
    replacements = {"🧵": "FABRIC:", "📈": "METRICS:", "🌍": "ECO:", "🛠️": "MFG:", "**": "", "###": ""}
    for old, new in replacements.items():
        clean_text = clean_text.replace(old, new)
        
    clean_text = clean_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, txt=clean_text, border=0)
    
    return bytes(pdf.output())