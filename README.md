# Spellchecker for code-mixed text

Hi! This is a repository for implementing spellchecking on code-mixed text, currently for Hindi and Telugu (but ideally more in the future!). This repository is part of a larger group of projects aiming to implement text normalization tools for researchers working with code-mixed text in indic languages.

## Requirements
After cloning, install the requirements by:

`pip install -r requirements.txt`
(Make sure you have got sufficient permissions, otherwise use '--user' option)

- [pybktree](https://pypi.org/project/pybktree/)
- [indictrans](https://pypi.org/project/indic-transliteration/)
- [codecs](https://pypi.org/project/openapi-codec/)
- [bs4](https://pypi.org/project/beautifulsoup4/)
- [metaphone](https://pypi.org/project/Metaphone/)

## Setup

Project files are contained in the `spellcheck/` directory. The README file and testing harness are in the topmost directory.

All source files are contained with the `src/` directory. Currently, the main spellchecker module (the vast majority of which still needs to be written) is wrapped in the `Spellchecker` class.

All data is read in through `read_data.py` and all large files are in the `data/` directory. If this gets too big down the line, should most likely move to a new data repository.

`DataManagement`: This folder contains the various abstractions that make up the pipeline. When you add a new implementation of some tool for the pipeline, make sure that it is always along the lines of an abstraction contained in this folder. Feel free to add new abstractions into this folder. Some of the abstractions are as follows:  
`languageUtils.py`: Classes for Langauge Specific Identifiers, Lexicons and SpellCheckers.  
`dataloader.py`: Classes for loading a corpus - mono-lingual/multi-lingual.  

Testing information and setup is in the `tests/` directory. Currently, this is how you would check functionality of the `Spellchecker` class (see the next section).

## Workflow/Running Tests

This may be streamlined down the line with a helpful command, but for right now the workflow should occur as follows:

- Write function/feature in either `spellcheck.py` or a helper file
- Test functionality of the new feature by writing a new test function in `tests.py` (see file for more details and examples).
- Run `python harness.py` in the topmost directory
- If you would like to see more details about passed/failed tests, run `python harness.py -V

## Commands

Normalization: `python normalize.py "source_hinglish.txt" "source_hinglish_lang.txt" "eng,hin" --do_repickle`

Spell check Command: `python main.py test.txt -A 1 -outputType firstOf -langTag tel`

If you want to know more about each option, just do `python main.py -h`

## Notes

This project is still in progress! Check back for updates during the coming months.

## Credits

Currently being worked on by Sumeet Singh (Current MLT, Carnegie Mellon) and Meheresh Yeditha (Current BS CS, Carnegie Mellon).

## Some Resources

- [Indian Language Corpus Repository](https://ltrc.iiit.ac.in/showfile.php?filename=ltrc/internal/nlp/corpus/index.html)

- [General Language Corpus Repository] (http://wortschatz.uni-leipzig.de/en/download/)
