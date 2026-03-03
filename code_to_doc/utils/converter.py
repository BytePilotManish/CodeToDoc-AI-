import markdown
from xhtml2pdf import pisa
import os

def md_to_pdf(md_content, output_pdf_path):
    """
    Converts Markdown content to a PDF file.
    """
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'tables'])
    
    # Add some basic CSS for the PDF
    styled_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Helvetica, Arial, sans-serif; font-size: 10pt; line-height: 1.5; color: #333; }}
            h1 {{ color: #4f46e5; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            h2 {{ color: #6366f1; margin-top: 20px; }}
            h3 {{ color: #818cf8; }}
            code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px; font-family: monospace; }}
            pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 8px; font-family: monospace; overflow: hidden; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f8fafc; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Create PDF
    with open(output_pdf_path, "wb") as f:
        pisa_status = pisa.CreatePDF(styled_html, dest=f)
        
    return not pisa_status.err
