import nltk

def transform_text(text):
    # TODO: Move these out of function into module or class initialization
    nltk.download('punkt')
    # TODO: Modularize so that other POS taggers can be used
    nltk.download('averaged_perceptron_tagger')
    sentences = nltk.sent_tokenize(text)
    words = [nltk.word_tokenize(s) for s in sentences]
    pos_tags = [nltk.pos_tag(w) for w in words]
    return sentences, words, pos_tags