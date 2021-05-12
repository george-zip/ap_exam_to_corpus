"""
Library for extracting text from PDF document

Available functions:
- extract_text: extract text from PDF, preserving whitespace
"""

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def extract_text(file_name, char_margin=2.0, word_margin=0.1, line_margin=0.5, vertical_detect=False,
                 line_overlap=0.5, box_flow=None):
    """Extract text from PDF file

    The layout parameters may be overridden. The default values work for the AP US History exams tested,
    based on a lot of experimentation. Change with care, as small parameter changes reap big results.

    Args:
        file_name: Full path of PDF file
        char_margin: Max distance between characters to be considered part of the same line
        word_margin: Min distance between characters to be considered different words
        line_margin: Min distance between characters to be considered part of the same paragraph
        vertical_detect: consider vertical text during analysis
        line_overlap: max overlap between two lines to be considered separate
        box_flow: Determines how much vertical and horizontal distance of text matters the order of text boxes
        Ranges between -1.0 to 1.0 or None

    Returns:
        Unicode text with whitespace preserved
    """

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
