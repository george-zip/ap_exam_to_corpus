import datetime
import unittest
import xml.etree.ElementTree as e_tree
import re

import xml_handling


def test_xpath_and_value(test_case, elem, xpath, value):
    target = elem.find(xpath)
    test_case.assertIsNotNone(target)
    test_case.assertEqual(target.text, value)


class XmlHandlingTest(unittest.TestCase):
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

    def test_add_or_set(self):
        parent = e_tree.Element("parent")
        elem = xml_handling.add_or_set(parent, "tag", "text", "foo", "bar")
        self.assertIs(parent.find("./tag"), elem)
        self.assertEqual(elem.tag, "tag")
        self.assertEqual(elem.text, "text")
        self.assertEqual(elem.attrib["foo"], "bar")

    def test_get_header(self):
        header = xml_handling.get_header(self.meta_data)
        self.assertIsNotNone(header)
        self.assertIsInstance(header, e_tree.Element)
        self.assertEqual(header.tag, "teiHeader")
        test_xpath_and_value(self, header, "fileDesc/titleStmt/title", self.meta_data["title"])
        test_xpath_and_value(self, header, "fileDesc/publicationStmt/publisher", self.meta_data["publisher"])
        test_xpath_and_value(self, header, "fileDesc/publicationStmt/availability/p", self.meta_data["availability"])
        test_xpath_and_value(self, header, "fileDesc/sourceDesc/p", self.meta_data["source"])
        test_xpath_and_value(self, header, "encodingDesc/p", self.meta_data["encoding"])
        lang = header.find("profileDesc/langUsage/language")
        self.assertIsNotNone(lang)
        self.assertEqual(lang.attrib["ident"], self.meta_data["language_ident"])
        self.assertEqual(lang.text, self.meta_data["language"])
        revision_date = header.find("revisionDesc/list/item/date")
        self.assertIsNotNone(revision_date)
        today = datetime.date.today()
        self.assertEqual(revision_date.attrib["when"], f"{today:%Y}-{today:%m}-{today:%d}")
        self.assertEqual(revision_date.text, f"{today:%d} {today:%b} {today:%y}")

    def test_corpus_to_xml_one_section(self):
        from text_handling import CorpusSection
        sections = [CorpusSection('start', 0, 100, [
            [('One', 'CD'), ('morning', 'NN'), (',', ','), ('when', 'WRB'), ('Gregor', 'NNP'), ('Samsa', 'NNP'),
             ('woke', 'VBD'), ('from', 'IN'), ('troubled', 'JJ'), ('dreams', 'NNS'), (',', ','), ('he', 'PRP'),
             ('found', 'VBD'), ('himself', 'PRP'), ('transformed', 'VBN'), ('in', 'IN'), ('his', 'PRP$'),
             ('bed', 'NN'),
             ('into', 'IN'), ('a', 'DT'), ('horrible', 'JJ'), ('vermin', 'NN'), ('.', '.')]])]
        xml_doc = xml_handling.corpus_to_xml(sections, self.meta_data)
        self.assertIsNotNone(xml_doc)
        self.assertIsInstance(xml_doc, e_tree.Element)
        self.assertEqual(xml_doc.tag, "TEI")
        xml_sections = xml_doc.find("text/body/list")
        self.assertIsNotNone(xml_sections)
        self.assertEqual(len(xml_sections), 1)
        item = xml_sections[0]
        self.assertEqual(item.tag, "item")
        id = item.attrib["xml:id"]
        self.assertIsNotNone(id)
        xml_span = xml_doc.find("text/body/spanGrp")
        self.assertIsNotNone(xml_span)
        self.assertEqual(len(xml_span), 1)
        self.assertEqual(xml_span[0].attrib["from"], id)

    def test_corpus_to_xml(self):
        from text_handling import CorpusSection
        sections = [
            CorpusSection('beginning', 0, 100, [
                [('One', 'CD'), ('morning', 'NN'), (',', ','), ('when', 'WRB'), ('Gregor', 'NNP'), ('Samsa', 'NNP'),
                 ('woke', 'VBD'), ('from', 'IN'), ('troubled', 'JJ'), ('dreams', 'NNS'), (',', ','), ('he', 'PRP'),
                 ('found', 'VBD'), ('himself', 'PRP'), ('transformed', 'VBN'), ('in', 'IN'), ('his', 'PRP$'),
                 ('bed', 'NN'),
                 ('into', 'IN'), ('a', 'DT'), ('horrible', 'JJ'), ('vermin', 'NN'), ('.', '.')]]),
            CorpusSection('action', 101, 200, [
                [('He', 'PRP'), ('lay', 'VBD'), ('on', 'IN'), ('his', 'PRP$'), ('armour-like', 'JJ'), ('back', 'NN'),
                 (',', ','), ('and', 'CC'), ('if', 'IN'), ('he', 'PRP'), ('lifted', 'VBD'), ('his', 'PRP$'),
                 ('head', 'NN'),
                 ('a', 'DT'), ('little', 'JJ'), ('he', 'PRP'), ('could', 'MD'), ('see', 'VB'), ('his', 'PRP$'),
                 ('brown', 'JJ'), ('belly', 'RB'), (',', ','), ('slightly', 'RB'), ('domed', 'VBN'), ('and', 'CC'),
                 ('divided', 'VBN'), ('by', 'IN'), ('arches', 'NNS'), ('into', 'IN'), ('stiff', 'JJ'),
                 ('sections', 'NNS'),
                 ('.', '.')]]),
            CorpusSection('description', 201, 300, [
                [('The', 'DT'), ('bedding', 'NN'), ('was', 'VBD'), ('hardly', 'RB'), ('able', 'JJ'), ('to', 'TO'),
                 ('cover', 'VB'), ('it', 'PRP'), ('and', 'CC'), ('seemed', 'VBD'), ('ready', 'JJ'), ('to', 'TO'),
                 ('slide', 'VB'), ('off', 'RP'), ('any', 'DT'), ('moment', 'NN'), ('.', '.')]])
        ]
        xml_doc = xml_handling.corpus_to_xml(sections, self.meta_data)
        self.assertIsNotNone(xml_doc)
        self.assertIsInstance(xml_doc, e_tree.Element)
        self.assertEqual(xml_doc.tag, "TEI")
        xml_sections = xml_doc.find("text/body/list")
        self.assertIsNotNone(xml_sections)
        self.assertEqual(len(xml_sections), 3)
        xml_span = xml_doc.find("text/body/spanGrp")
        self.assertIsNotNone(xml_span)
        self.assertEqual(len(xml_span), 3)
        for count, item in enumerate(xml_sections):
            id_str = item.attrib["xml:id"]
            self.assertIsNotNone(id_str)
            self.assertIsNotNone(xml_span.find(f"span/[@from='{id_str}']"))
            id_num = int(re.search(r"\d+$", id_str).group())
            self.assertEqual(id_num, count)



if __name__ == '__main__':
    unittest.main()
