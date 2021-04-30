import re
from collections import namedtuple
import pdf_handling
import text_handling
import xml_handling
import datetime

FILE = "./samples/ap-us-history-frq-2017.pdf"

if __name__ == '__main__':
    text = pdf_handling.extract_text(FILE, box_flow=None)
    filled_in_sections = text_handling.extract_all_sections(text)
    #TODO: Move default metadata into config file
    meta_data = {
        "title": "AP United States History Free-Response Questions",
        "publisher": "College Board",
        "document_date": "2017",
        "availability": "Freely available on a non-commercial basis",
        "source": "Exam in Adobe Portable Document Format",
        "encoding": """Basic encoding, capturing structural elements and parts of speech. 
            All punctuation is preserved.
            No formatting or layout information preserved.""",
        "language_ident": "en-US",
        "language": "English United States",
        "revision_date": str(datetime.date.today()),
        "tei_schema": "http://www.tei-c.org/ns/1.0"
    }

    xml_root = xml_handling.corpus_to_xml(filled_in_sections, meta_data)
    import xml.etree.ElementTree as ET
    from xml.dom.minidom import parseString
    s = ET.tostring(xml_root, 'unicode')
    nice = parseString(s)
    print(nice.toprettyxml(indent='\t'))