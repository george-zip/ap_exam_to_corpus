import pdf_handling

FILE = "./samples/ap-us-history-frq-2017.pdf"

if __name__ == '__main__':
    print(pdf_handling.extract_text(FILE, box_flow=None))
