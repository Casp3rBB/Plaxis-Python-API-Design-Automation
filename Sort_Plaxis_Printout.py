import PyPDF2
import os

def Rearrange_pdf(pdf_path, txt_path, output_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Read the text file
        with open(txt_path, 'r') as txt_file:
            lines = txt_file.readlines()

        # Create a new PDF file
        pdf_writer = PyPDF2.PdfFileWriter()

        # Iterate over each line in the text file
        for line in lines:
            # Remove trailing newline character
            line = line.strip()

            # Iterate over each page in the PDF
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)

                # If the page contains the line of text, add it to the new PDF
                if line in page.extractText():
                    pdf_writer.addPage(page)
                    break

        # Write the new PDF file
        with open(output_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

# Call the function
pdf_path = r''
order_text_path = r''

if pdf_path == '': pdf_path = input('Enter pdf path:').strip("'").strip('"').strip()
if order_text_path == '': order_text_path = input('Enter order_text_file path:').strip("'").strip('"').strip()

output_path = os.path.join(os.path.dirname(pdf_path), 'rearranged.pdf')

Rearrange_pdf(pdf_path, order_text_path, output_path)


