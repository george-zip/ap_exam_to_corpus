import re
from collections import namedtuple

CorpusSection = namedtuple('CorpusSection', ('type', 'start_position', 'end_position', 'contents'))


def tokenize_text(text, tokenizer):
    sentences = tokenizer.sent_tokenize(text)
    words = [tokenizer.word_tokenize(s) for s in sentences]
    pos_tags = [tokenizer.pos_tag(w) for w in words]
    return sentences, words, pos_tags


def extract_section_reg_exp(text, reg_exp, section_name, tokenizer):
    matches = re.finditer(reg_exp, text, flags=re.MULTILINE)
    for match in matches:
        (start, end) = match.span()
        _, _, words_with_pos_tags = tokenize_text(text[start:end], tokenizer)
        yield CorpusSection(section_name, start, end, words_with_pos_tags)


def extract_named_sections(text, tokenizer):
    regular_expressions = {
        "directions": "^Directions: [\w\d\s;.,:-]+\n",
        "questions": "^\d+\..*\n"
    }
    # TODO: Add more sections
    for name in regular_expressions:
        for section in extract_section_reg_exp(text, regular_expressions[name], name, tokenizer):
            yield section


def fill_in_all_sections(named_sections, text, tokenizer):
    current_position = 0
    for section in named_sections:
        if section.start_position > current_position:
            _, _, words_with_pos_tags = tokenize_text(text[current_position:section.start_position - 1], tokenizer)
            yield CorpusSection("general", current_position, section.start_position - 1, words_with_pos_tags)
        yield section
        current_position = section.end_position + 1
    if current_position < len(text):
        _, _, words_with_pos_tags = tokenize_text \
            (text[current_position:len(text) - 1], tokenizer)
        yield CorpusSection("general", current_position, len(text) - 1, words_with_pos_tags)


def extract_all_sections(text, tokenizer):
    named_sections = extract_named_sections(text, tokenizer)
    return fill_in_all_sections(sorted(named_sections, key=lambda t: t[1]), text, tokenizer)
