# WIP: fii-webcrawler

This project was created to consume data from the internet to help investors to make better decisions with their investments focused on Real State Funds.

## Prerequisites

What things you need to install the software and how to install them

* Python 3.x
* Geckodriver
* Firefox (you can use another browser)
* Some Python libraries following

## Installing

Create the environment

```
virtualenv --python='/usr/bin/python3' venv
```

Activate it
```
source venv/bin/activate
```

A step by step series of examples that tell you how to get a development env running

### Install the following Python libraries:

 * **requests2** - Requests is the only Non-GMO HTTP library for Python, safe for human consumption;
 * **pandas** - A great Python Data Analysis Library;
 * **lxml** - Library for processing XML and HTML;
 * **beautfulsoup4** - Library for pulling data out of HTML and XML files;
 * **selenium** - An API to write functional/acceptance tests using Selenium WebDriver.

With:
```
pip install -r requirements.txt
```

### Geckodriver

[You can find install instructions in the official repository.](https://github.com/mozilla/geckodriver/releases)

## Running the code

```
python crawler.py
```

## To-Do

[x] Finishing implementing the data collector

[x] Implement logging

[ ] Turn the settings module into a Singleton

[ ] Treat the output generated before send to the API

[ ] Implement the API integration

[ ] Unit tests
