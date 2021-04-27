import datetime
import unittest
import xml.etree.ElementTree as ET

import xml_handling


def test_xpath_and_value(test_case, elem, xpath, value):
    target = elem.find(xpath)
    test_case.assertIsNotNone(target)
    test_case.assertEqual(target.text, value)


class XmlHandlingTest(unittest.TestCase):

    def test_get_header(self):
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
            "revision_date": datetime.datetime.now()
        }
        header = xml_handling.get_header(meta_data)
        self.assertIsNotNone(header)
        self.assertIsInstance(header, ET.Element)
        self.assertEqual(header.tag, "teiHeader")
        test_xpath_and_value(self, header, "fileDesc/titleStmt/title", meta_data["title"])
        test_xpath_and_value(self, header, "fileDesc/publicationStmt/publisher", meta_data["publisher"])
        test_xpath_and_value(self, header, "fileDesc/publicationStmt/availability/p", meta_data["availability"])
        test_xpath_and_value(self, header, "fileDesc/sourceDesc/p", meta_data["source"])
        test_xpath_and_value(self, header, "encodingDesc/p", meta_data["encoding"])
        test_xpath_and_value(self, header, "profileDesc/langUsage/language/@ident", meta_data["language_ident"])


if __name__ == '__main__':
    unittest.main()
