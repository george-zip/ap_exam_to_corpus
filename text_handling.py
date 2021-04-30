import nltk
from collections import namedtuple
import re

CorpusSection = namedtuple('CorpusSection', ('type', 'start_position', 'end_position', 'contents'))


# Reference: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

def transform_text(text):
    # TODO: Move these out of function into module or class initialization
    # TODO: Don't download unless missing
    nltk.download('punkt')
    # TODO: Modularize so that other POS taggers can be used
    nltk.download('averaged_perceptron_tagger')
    # TODO: Do my own tokenizing based on white space (see https://lost-contact.mit.edu/afs/cs.pitt.edu/projects/nltk/docs/tutorial/chunking/nochunks.html)
    sentences = nltk.sent_tokenize(text)
    # TODO: Figure out if I need to remove whitespace at this point - probably Yes if being done after searching for structural elements
    words = [nltk.word_tokenize(s) for s in sentences]
    pos_tags = [nltk.pos_tag(w) for w in words]
    return sentences, words, pos_tags


def extract_section_reg_exp(text, reg_exp, section_name):
    matches = re.finditer(reg_exp, text, flags=re.MULTILINE)
    for match in matches:
        (start, end) = match.span()
        _, _, words_with_pos_tags = transform_text(text[start:end])
        yield CorpusSection(section_name, start, end, words_with_pos_tags)


def extract_named_sections(text):
    regular_expressions = {
        "directions": "^Directions: [\w\d\s;.,:-]+\n",
        "questions": "^\d+\..*\n"
    }
    for name in regular_expressions:
        for section in extract_section_reg_exp(text, regular_expressions[name], name):
            yield section

def fill_in_all_sections(named_sections, text):
    current_position = 0
    for section in named_sections:
        if section.start_position > current_position:
            _, _, words_with_pos_tags = transform_text(text[current_position:section.start_position - 1])
            yield CorpusSection("general", current_position, section.start_position - 1, words_with_pos_tags)
        yield section
        current_position = section.end_position + 1
    if current_position < len(text):
        _, _, words_with_pos_tags = transform_text \
            (text[current_position:len(text) - 1])
        yield CorpusSection("general", current_position, len(text) - 1, words_with_pos_tags)


def extract_all_sections(text):
    named_sections = extract_named_sections(text)
    return fill_in_all_sections(sorted(named_sections, key=lambda t : t[1]), text)
