#!/usr/bin/python3

from PyPDF2 import PdfReader
from PdfOut import PdfOut

reader = PdfReader("source.pdf")

page = reader.pages[0]
fields = reader.get_fields()

# for field in fields:
#     print(field+"\n");
    
pdfWriter = PdfOut()
pdfWriter.write(reader.pages, "filled-out.pdf")
