from unittest import TestCase

import nltk

import text_handling


class TextHandlingTest(TestCase):
    text = "One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed " \
           "into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could " \
           "see his brown belly, slightly domed and divided by arches into stiff sections."

    def __init__(self, *args, **kwargs):
        super(TextHandlingTest, self).__init__(*args, **kwargs)
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

    def test_transform_text(self):
        # Reference: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        sentences, words, pos_tags = text_handling.tokenize_text(self.text, nltk)
        self.assertIsNotNone(sentences)
        self.assertIsNotNone(words)
        self.assertIsNotNone(pos_tags)
        self.assertEqual(len(sentences), 2)
        self.assertEqual(len(words[0]), 23)
        self.assertEqual(len(pos_tags[0]), 23)
        self.assertEqual(len(pos_tags[0]), 23)
        self.assertIsInstance(pos_tags[0][0], tuple)
        # these tags may have to change if a different tagger is used
        self.assertEqual(pos_tags[0][0][1], "CD")
        self.assertEqual(pos_tags[0][1][1], "NN")
        self.assertEqual(pos_tags[0][2][1], ",")

    def test_extract_section_reg_exp(self):
        itr = text_handling.extract_section_reg_exp(self.text, "\sarmour\-like\sback\,", "description", nltk)
        self.assertIsNotNone(itr)
        try:
            s = next(itr)
            self.assertIsInstance(s, tuple)
            self.assertEqual(s.type, "description")
            self.assertEqual(s.start_position, 135)
            self.assertEqual(s.end_position, 153)
            self.assertEqual(len(s.contents[0]), 3)
            self.assertEqual(s.contents[0][0][0], "armour-like")
            self.assertEqual(s.contents[0][0][1], "JJ")
        except StopIteration:
            self.fail("No values returned")
