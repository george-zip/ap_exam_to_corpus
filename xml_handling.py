"""
Library for creating TEI document

Available functions:
- corpus_to_xml: generate TEI document
- get_header: generate teiHeader
- add_or_set: add child tag or set value
"""

import datetime
import xml.etree.ElementTree as ET


def add_or_set(parent, tag_name, text=None, attribute_name=None, attribute_val=None):
    """Add child tag or set value if already present"""
    tmp = parent.find(tag_name)
    if not tmp:
        tmp = ET.Element(tag_name)
        parent.append(tmp)
    if text is not None:
        tmp.text = text
    if attribute_name is not None and attribute_val is not None:
        tmp.attrib[attribute_name] = attribute_val
    return tmp


def get_header(meta_data):
    """Generate teiHeader"""
    header = ET.Element("teiHeader")
    add_or_set(add_or_set(add_or_set(header, "fileDesc"), "titleStmt"), "title", meta_data["title"])
    add_or_set(add_or_set(add_or_set(header, "fileDesc"), "publicationStmt"), "publisher", meta_data["publisher"])
    add_or_set(add_or_set(
        add_or_set(add_or_set(header, "fileDesc"), "publicationStmt"),
        "availability"
    ), "p", meta_data["availability"])
    add_or_set(add_or_set(add_or_set(header, "fileDesc"), "sourceDesc"), "p", meta_data["source"])
    add_or_set(add_or_set(header, "encodingDesc"), "p", meta_data["encoding"])
    add_or_set(add_or_set(add_or_set(header, "profileDesc"), "langUsage"), "language", meta_data["language"], "ident",
               meta_data["language_ident"])
    item = add_or_set(add_or_set(add_or_set(header, "revisionDesc"), "list"), "item")
    dt = datetime.datetime.strptime(meta_data["revision_date"], "%Y-%m-%d")
    add_or_set(item, "date", f"{dt:%d} {dt:%b} {dt:%y}", "when", meta_data["revision_date"])
    return header


def corpus_to_xml(sections, meta_data):
    """Generate TEI document based on list of CorpusSection tuples

    Args:
        sections: list of CorpusSection tuples
        meta_data: dictionary of document and invocation-related meta-data

    Returns:
        xml.etree.Element
    """
    root = ET.Element("TEI")
    root.attrib["xmlns:ns"] = meta_data["tei_schema"]
    root.append(get_header(meta_data))
    body = add_or_set(add_or_set(root, "text"), "body")
    list_elem = add_or_set(body, "list")
    span_grp = add_or_set(body, "spanGrp", attribute_name="type", attribute_val="structure")
    for idx, section in enumerate(sections):
        # for each corpus section, we add:
        # 1. An item element containing the section contents broken down hierarchically into sentences and words.
        # Each section is uniquely identified by the 'xml:id' attribute.
        # 2. A span element that describes the item.
        # See https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-span.html
        section_id = f"s{idx}"
        item = ET.Element("item", {"xml:id": section_id})
        list_elem.append(item)
        for sentence in section.contents:
            s = add_or_set(add_or_set(item, "l"), "s")
            for word, pos_tag in sentence:
                if len(word) == 1 and not pos_tag.isalnum():
                    add_or_set(s, "pc", word)
                else:
                    add_or_set(s, "w", word, "pos", pos_tag)
        add_or_set(span_grp, "span", section.type, "from", section_id)
    return root
