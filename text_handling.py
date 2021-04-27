import nltk

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

def find_chunk(pos_tags, grammar):
    cp = nltk.RegexpParser(grammar)
    return cp.parse(pos_tags)