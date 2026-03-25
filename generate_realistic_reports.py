import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.flowables import KeepTogether
from reportlab.pdfgen import canvas

def draw_header_footer(canvas, doc, hospital_name, address):
    canvas.saveState()
    
    # Draw Hospital Name
    canvas.setFont('Helvetica-Bold', 20)
    canvas.setFillColor(colors.darkblue)
    canvas.drawCentredString(letter[0] / 2.0, letter[1] - 50, hospital_name)
    
    # Draw Address
    canvas.setFont('Helvetica', 10)
    canvas.setFillColor(colors.gray)
    canvas.drawCentredString(letter[0] / 2.0, letter[1] - 70, address)
    
    # Draw Top Line
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(2)
    canvas.line(50, letter[1] - 85, letter[0] - 50, letter[1] - 85)
    
    # Draw Footer
    canvas.setLineWidth(1)
    canvas.line(50, 70, letter[0] - 50, 70)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.gray)
    canvas.drawString(50, 55, "This is an electronically generated report. No physical signature is mandatory.")
    canvas.drawString(letter[0] - 150, 55, "Page %d" % doc.page)
    
    canvas.restoreState()

def create_realistic_report(filename, patient_data, hospital_data, test_results, signature_name="Dr. Anil Medical Officer"):
    doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=100, bottomMargin=90)
    elements = []
    styles = getSampleStyleSheet()
    
    # Patient Info Table
    patient_info = [
        ["Patient Name", f": {patient_data['name']}", "Age/Sex", f": {patient_data['age']} yrs / {patient_data['sex']}"],
        ["Patient ID", f": {patient_data['id']}", "Report Date", f": {patient_data['date']}"],
        ["Referred By", f": {patient_data.get('referred_by', 'Self')}", "Sample Type", ": Blood / Serum"]
    ]
    
    pt_table = Table(patient_info, colWidths=[80, 200, 80, 150])
    pt_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
    ]))
    
    elements.append(pt_table)
    elements.append(Spacer(1, 20))
    
    # Report Title
    title_style = ParagraphStyle('Title', parent=styles['Heading2'], alignment=1, spaceAfter=15)
    elements.append(Paragraph("LABORATORY INVESTIGATION REPORT", title_style))
    
    # Table Header
    test_data = [["Test Description", "Result", "Units", "Reference Range"]]
    
    # Append results
    for t in test_results:
        # Check if out of range to bold or make red
        result_cell = t['result']
        test_data.append([t['name'], result_cell, t['unit'], t['ref']])
        
    t_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightsteelblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('TOPPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ])
    
    t_table = Table(test_data, colWidths=[200, 100, 80, 130])
    t_table.setStyle(t_style)
    elements.append(t_table)
    elements.append(Spacer(1, 50))
    
    # Mock Signature / Stamp Area
    sig_data = [
        ["Verified By:", "Authorized Signatory:"],
        ["", ""],  # Space for signature
        ["Technician", signature_name]
    ]
    sig_table = Table(sig_data, colWidths=[250, 250])
    sig_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,1), (-1,1), 40), # Create vertical space for drawing sign
    ]))
    
    elements.append(KeepTogether(sig_table))

    # Build PDF with custom header/footer
    def draw_all(canvas, doc):
        draw_header_footer(canvas, doc, hospital_data['name'], hospital_data['address'])

    doc.build(elements, onFirstPage=draw_all, onLaterPages=draw_all)


if __name__ == "__main__":
    out_dir = "Mock_Hospital_Reports"
    os.makedirs(out_dir, exist_ok=True)
    
    # ---------------- REPORT 1: ABNORMAL (Anemia & Pre-diabetes) ----------------
    create_realistic_report(
        filename=os.path.join(out_dir, "Apollo_Diagnostics_Abnormal_JohnDoe.pdf"),
        patient_data={"name": "Mr. John Doe", "age": 45, "sex": "Male", "id": "PID-90210", "date": "24 Mar 2026"},
        hospital_data={"name": "APOLLO DIAGNOSTICS CENTER", "address": "123 Health Ave, Block B, Medical District, NY"},
        test_results=[
            {"name": "Hemoglobin (HGB)", "result": "10.1 (Low)", "unit": "g/dL", "ref": "13.8 - 17.2"},
            {"name": "Total Leukocyte Count", "result": "7500", "unit": "cumm", "ref": "4000 - 10000"},
            {"name": "Fasting Blood Glucose", "result": "115 (High)", "unit": "mg/dL", "ref": "70 - 100"},
            {"name": "Total Cholesterol", "result": "170", "unit": "mg/dL", "ref": "< 200"}
        ],
        signature_name="Dr. S. K. Sharma (MD Pathology)"
    )

    # ---------------- REPORT 2: WARNING (High Cholesterol) ----------------
    create_realistic_report(
        filename=os.path.join(out_dir, "CityMax_Hospital_LipidProfile_SarahSmith.pdf"),
        patient_data={"name": "Mrs. Sarah Smith", "age": 52, "sex": "Female", "id": "PID-88321", "date": "25 Mar 2026", "referred_by": "Dr. Miller"},
        hospital_data={"name": "CITYMAX SUPER SPECIALTY LABS", "address": "Level 4, City Center Mall Complex, California"},
        test_results=[
            {"name": "Hemoglobin (HGB)", "result": "14.2", "unit": "g/dL", "ref": "12.0 - 15.5"},
            {"name": "Fasting Sugar", "result": "90", "unit": "mg/dL", "ref": "70 - 100"},
            {"name": "Total Cholesterol", "result": "245 (High)", "unit": "mg/dL", "ref": "< 200"},
            {"name": "Triglycerides", "result": "160", "unit": "mg/dL", "ref": "< 150"}
        ],
        signature_name="Dr. V. Patel (Chief Pathologist)"
    )
    
    # ---------------- REPORT 3: PERFECTLY NORMAL ----------------
    create_realistic_report(
        filename=os.path.join(out_dir, "MetroHealth_Normal_Michael.pdf"),
        patient_data={"name": "Mr. Michael Johnson", "age": 30, "sex": "Male", "id": "PID-11223", "date": "25 Mar 2026"},
        hospital_data={"name": "METROHEALTH PATHOLOGY & IMAGING", "address": "45 Park Street, Downtown Med Square"},
        test_results=[
            {"name": "Hemoglobin", "result": "15.5", "unit": "g/dL", "ref": "13.8 - 17.2"},
            {"name": "Glucose (Random)", "result": "95", "unit": "mg/dL", "ref": "70 - 140"},
            {"name": "Total Cholesterol", "result": "185", "unit": "mg/dL", "ref": "< 200"},
            {"name": "Serum Creatinine", "result": "0.9", "unit": "mg/dL", "ref": "0.7 - 1.3"}
        ],
        signature_name="Dr. Emily Chen (Lab Director)"
    )
    
    print("Successfully generated 3 highly realistic medical reports!")
