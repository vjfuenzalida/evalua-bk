# evalua-bk
Selenium Bot built to autimatically answer Burger King (and eventually McDonald's) surveys (which gives discount codes).

## Setup
This project was built using thie [pipenv](https://pypi.org/project/pipenv/) tool, which allows to save dependencies and the python version used.  
Python version is 3.7.0, and the core library used is [Selenium](https://selenium-python.readthedocs.io/).

> NOTE: This script works with selenium chrome driver, so you must have Google Chrome installed and  [Chrome WebDriver](http://chromedriver.chromium.org/downloads).

The steps to run this script are the following (from the project directory): 

* Install pipenv
```
pip install pipenv
```

* Install dependencies
```
pipenv install
```

* Run the survey answerer
```
python main.py
```
