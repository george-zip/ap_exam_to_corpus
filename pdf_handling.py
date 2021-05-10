from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def extract_text(file_name, char_margin=2.0, word_margin=0.1, line_margin=0.5, vertical_detect=False,
                 line_overlap=0.5, box_flow=0.5):


    with open(file_name, "rb") as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams(char_margin=char_margin, word_margin=word_margin,
                            detect_vertical=vertical_detect, line_margin=line_margin,
                            line_overlap=line_overlap, boxes_flow=box_flow)
        with StringIO() as output_string:
            device = TextConverter(rsrcmgr, output_string, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

            return output_string.getvalue()
