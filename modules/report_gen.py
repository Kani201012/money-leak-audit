from weasyprint import HTML

def generate_pdf(business_name, audit, roi, currency):
    # Create a simple HTML string
    html_content = f"""
    <h1>Audit Report: {business_name}</h1>
    <h2 style="color: red;">Revenue Leakage Score: {audit['score']}/100</h2>
    <p>Severity: <strong>{audit['severity']}</strong></p>
    
    <h3>Issues Found:</h3>
    <ul>
    """
    
    for issue in audit['issues']:
        html_content += f"<li>{issue}</li>"
        
    html_content += f"""
    </ul>
    <hr>
    <h3>Financial Impact</h3>
    <p>Estimated Monthly Loss: <strong>{currency} {roi['min_revenue_loss']}</strong></p>
    <p>Estimated Annual Loss: <strong>{currency} {roi['annual_loss']}</strong></p>
    """
    
    # Convert HTML to PDF
    pdf = HTML(string=html_content).write_pdf()
    return pdf
