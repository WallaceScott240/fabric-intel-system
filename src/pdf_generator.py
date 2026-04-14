from fpdf import FPDF
import datetime

class FabricPDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 14)
        self.cell(0, 10, "Textile Intelligence Stack - Technical Report", ln=True, align="C")
        self.set_font("helvetica", "I", 9)
        self.cell(0, 5, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
        self.ln(10)

def export_to_pdf(text):
    pdf = FabricPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=11)
    
    # Remove metadata tag if present before printing to PDF
    clean_text = text.split("METRIC_DATA:")[0]
    
    # Professional Cleanup
    clean_text = clean_text.replace("🧵", "Fabric:").replace("📈", "Data:").replace("🌍", "Eco:")
    clean_text = clean_text.replace("✨", "").replace("🛠️", "Process:").replace("🟢", "-")
    clean_text = clean_text.replace("**", "").replace("### ", "")
    
    # Safe encoding for Latin-1
    clean_text = clean_text.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 8, txt=clean_text)
    
    return bytes(pdf.output())