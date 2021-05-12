# AP Exam Corpus Project

The AP Exam Corpus Project is a Python application for generating corpora for [AP exams](https://apstudents.collegeboard.org/ap-exams-overview).

At this point, the application generates a corpus for the US AP History Free Response section in [TEI-compliant](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-teiCorpus.html) format.

The input to the application is the path of an exam in PDF format. The default output is formatted XML to stdout.

### Future Work

1. Improve parsing robustness in order to handle other AP exam formats.
2. Adopt the [Corpus Encoding Standard](https://www.cs.vassar.edu/CES/) for the corpus.
3. Expand to more AP subjects (arts, english, math and computer science) and paper formats (multiple choice, short response questions)

## Installation

Clone the repository. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install -r requirements.txt
```

## Usage

```bash
main.py -h 
usage: main.py [-h] -f FILE [-o {xml,text,sections}] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path of PDF file
  -o {xml,text,sections}, --output {xml,text,sections}
                        Output format
  -c CONFIG, --config CONFIG
                        Path of yaml config file
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please update test cases as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)