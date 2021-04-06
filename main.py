import pdf_handling
import text_handling

FILE = "./samples/ap-us-history-frq-2017.pdf"



if __name__ == '__main__':
    text = pdf_handling.extract_text(FILE, box_flow=None)
    sentences, words, pos_tags = text_handling.transform_text(text)
    print(pos_tags)

