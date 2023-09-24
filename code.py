import os
import PyPDF2
from PyPDF2 import PdfReader , PdfWriter

current_directory = os.getcwd()
output_directory = os.path.join(current_directory, "output")


def find_pdf_file():
    pdf_files = [file for file in os.listdir(current_directory) if file.endswith(".pdf")]
    
    if pdf_files:
        pdf_file_path = os.path.join(current_directory, pdf_files[0])
        return pdf_file_path
    else:
        return None
        
        

# Input PDF file path (assuming it's in the current directory)
input_pdf_file = find_pdf_file()



# Create an "output" directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Open the input PDF file
with open(input_pdf_file, "rb") as pdf_file:
    pdf_reader = PdfReader(pdf_file)
    
    page_count = 0
    
    # Iterate through each page in the PDF
    for page in pdf_reader.pages:
        page_count += 1
        # Create a new PDF writer
        pdf_writer = PdfWriter()
        
        # Add the current page to the writer
        pdf_writer.add_page(page)
        
        # Output PDF file path for the current page inside the "output" directory
        output_pdf_file = os.path.join(output_directory, f"{page_count}.pdf")
        
        # Write the current page to a separate PDF file
        with open(output_pdf_file, "wb") as output_file:
            pdf_writer.write(output_file)

print("PDF split into individual pages and saved in the 'output' directory.")
