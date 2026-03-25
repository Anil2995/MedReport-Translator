from reportlab.pdfgen import canvas

def create_mock_report(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "MOCK CLINICAL LAB REPORT")
    c.drawString(100, 730, "--------------------------------------------------")
    c.drawString(100, 710, "Patient Name: John Doe")
    c.drawString(100, 690, "Date: 2026-03-25")
    c.drawString(100, 670, "--------------------------------------------------")
    c.drawString(100, 640, "Test Results:")
    c.drawString(100, 620, "Hemoglobin (HGB): 11.2 g/dL")
    c.drawString(100, 600, "Fasting Blood Sugar (Glucose): 105 mg/dL")
    c.drawString(100, 580, "Total Cholesterol: 180 mg/dL")
    c.drawString(100, 550, "--------------------------------------------------")
    c.drawString(100, 530, "End of Report")
    c.save()

if __name__ == "__main__":
    create_mock_report("mock_report.pdf")
    print(f"Created mock_report.pdf")
