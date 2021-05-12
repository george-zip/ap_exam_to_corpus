#!/usr/bin/env python
"""
Script for generating a TEI-compliant document from an AP US History Free Response Exam in PDF format.
Prints the XML document as text to stdout.
"""
import argparse
import datetime

import nltk
import yaml

import pdf_handling
import text_handling
import xml_handling


def initialize_default_tokenizer():
    """Initialize ntlk tokenizer"""
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')


def get_arg_parser():
    """Configure command line options"""
    p = argparse.ArgumentParser()
    p.add_argument("-f", "--file", help="Path of PDF file", required=True)
    p.add_argument("-o", "--output", help="Output format", choices=['xml', 'text', 'sections'], default='xml')
    p.add_argument("-c", "--config", help="Path of yaml config file", default='./ap_parser.yaml')
    return p


def get_configuration(config_path):
    """Open configuration file and return dictionary of configuration"""
    with open(config_path, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


def get_metadata(config_path):
    """Get meta-data needed to print document"""
    meta_data = get_configuration(config_path)
    meta_data['revision_date'] = str(datetime.date.today())
    return meta_data


def print_xml_doc(xml_root):
    """Pretty print xml document"""
    import xml.etree.ElementTree as ET
    from xml.dom.minidom import parseString
    s = ET.tostring(xml_root, encoding='unicode', method='xml')
    # special character not handled by dom.minidom
    s = s.replace('', '')
    nice = parseString(s)
    print(nice.toprettyxml(indent='\t'))


if __name__ == '__main__':
    parser = get_arg_parser()
    args = parser.parse_args()

    text = pdf_handling.extract_text(args.file)
    if args.output == 'text':
        print(text)
    else:
        initialize_default_tokenizer()
        filled_in_sections = text_handling.extract_all_sections(text, nltk)
        if args.output == "sections":
            for section in filled_in_sections:
                print(section)
        else:
            xml_root = xml_handling.corpus_to_xml(filled_in_sections, get_metadata(args.config))
            print_xml_doc(xml_root)
