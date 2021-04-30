import re
from collections import namedtuple
import pdf_handling
import text_handling
import xml_handling
import datetime

FILE = "./samples/ap-us-history-frq-2017.pdf"

CorpusSection = namedtuple('CorpusSection', ('type', 'start_position', 'end_position', 'contents'))

if __name__ == '__main__':
    text = pdf_handling.extract_text(FILE, box_flow=None)
    # directions_regex = "^Directions: [\w\d\s;.,:-]+\n"
    # question_regex = "^\d+\..*\n"
    # sections = []
    # matches = re.finditer(directions_regex, text, flags=re.MULTILINE)
    # for match in matches:
    #     (start, end) = match.span()
    #     _, _, words_with_pos_tags = text_handling.transform_text(text[start:end])
    #     sections.append(CorpusSection('instructions.section', start, end, words_with_pos_tags))
    # matches = re.finditer(question_regex, text, flags=re.MULTILINE)
    # for match in matches:
    #     (start, end) = match.span()
    #     _, _, words_with_pos_tags = text_handling.transform_text(text[start:end])
    #     sections.append(CorpusSection('instructions.question', start, end, words_with_pos_tags))
    # filled_in_sections = []
    # current_idx = 0
    # for sec in sorted(sections, key=lambda tup: tup[1]):
    #     if sec.start_position > current_idx:
    #         _, _, words_with_pos_tags = text_handling.transform_text\
    #             (text[current_idx:sec.start_position - 1])
    #         filled_in_sections.append\
    #             (CorpusSection("general", current_idx, sec.start_position - 1, words_with_pos_tags))
    #     filled_in_sections.append(sec)
    #     current_idx = sec.end_position + 1
    # if current_idx < len(text):
    #     _, _, words_with_pos_tags = text_handling.transform_text \
    #         (text[current_idx:len(text) - 1])
    #     filled_in_sections.append(CorpusSection("general", current_idx, len(text) - 1, words_with_pos_tags))

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

    # maintain list of regular expressions for structural elements
    # for each one, call re.finditer to find all instances within text
    # sort all instances by start position within text
    # throw exception if there is overlap between structural elements
    # iterate through sections of text, including sections between elements
    # text_handling.transform_text for each section
    # form tuple of (structural element or None, pos_tags)
    # iterate through and create XML
    # will be tricky because xml document is recursive

    # next steps: create by hand xml for sample document
