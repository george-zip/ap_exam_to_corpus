import datetime
import unittest
import xml.etree.ElementTree as e_tree

import xml_handling


def test_xpath_and_value(test_case, elem, xpath, value):
    target = elem.find(xpath)
    test_case.assertIsNotNone(target)
    test_case.assertEqual(target.text, value)


class XmlHandlingTest(unittest.TestCase):

    def test_add_or_set(self):
        parent = e_tree.Element("parent")
        elem = xml_handling.add_or_set(parent, "tag", "text", "foo", "bar")
        self.assertIs(parent.find("./tag"), elem)
        self.assertEqual(elem.tag, "tag")
        self.assertEqual(elem.text, "text")
        self.assertEqual(elem.attrib["foo"], "bar")

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
            "revision_date": str(datetime.date.today())
        }
        header = xml_handling.get_header(meta_data)
        self.assertIsNotNone(header)
        self.assertIsInstance(header, e_tree.Element)
        self.assertEqual(header.tag, "teiHeader")
        test_xpath_and_value(self, header, "fileDesc/titleStmt/title", meta_data["title"])
        test_xpath_and_value(self, header, "fileDesc/publicationStmt/publisher", meta_data["publisher"])
        test_xpath_and_value(self, header, "fileDesc/publicationStmt/availability/p", meta_data["availability"])
        test_xpath_and_value(self, header, "fileDesc/sourceDesc/p", meta_data["source"])
        test_xpath_and_value(self, header, "encodingDesc/p", meta_data["encoding"])
        lang = header.find("profileDesc/langUsage/language")
        self.assertIsNotNone(lang)
        self.assertEqual(lang.attrib["ident"], meta_data["language_ident"])
        self.assertEqual(lang.text, meta_data["language"])
        revision_date = header.find("revisionDesc/list/item/date")
        self.assertIsNotNone(revision_date)
        today = datetime.date.today()
        self.assertEqual(revision_date.attrib["when"], f"{today:%Y}-{today:%m}-{today:%d}")
        self.assertEqual(revision_date.text, f"{today:%d} {today:%b} {today:%y}")


if __name__ == '__main__':
    unittest.main()
