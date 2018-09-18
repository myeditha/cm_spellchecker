# Spellchecker for code-mixed text

Hi! This is a repository for implementing spellchecking on code-mixed text, currently for Hindi and Telugu (but ideally more in the future!). This repository is part of a larger group of projects aiming to implement text normalization tools for researchers working with code-mixed text in indic languages.

## Requirements

- [pyenchant](https://github.com/rfk/pyenchant)
- [fuzzy](https://pypi.org/project/Fuzzy/)

## Setup

All source files are contained with the `src/` directory. Currently, the main spellchecker module (the vast majority of which still needs to be written) is wrapped in the `Spellchecker` class.

All data is read in through `read_data.py` and all large files are in the `data/` directory. If this gets too big down the line, should most likely move to a new data repository.

Testing information and setup is in the `tests/` directory. Currently, this is how you would check functionality of the `Spellchecker` class (see the next section).

## Workflow/Running Tests

This may be streamlined down the line with a helpful command, but for right now the workflow should occur as follows:

- Write function/feature in either `spellcheck.py` or a helper file
- Test functionality of the new feature by writing a new test function in `tests.py` (see file for more details and examples).
- Run `python -m cm_spellchecker.tests.run_tests` in the same directory as `cm_spellchecker/`. 
- If you would like to see more details about passed/failed tests, run `python -m cm_spellchecker.tests.run_tests -V`

## Notes

This project is still in progress! Check back for updates during the coming months.

## Credits

Currently being worked on by Sumeet Singh (Current MLT, Carnegie Mellon) and Meheresh Yeditha (Current BS CS, Carnegie Mellon).
