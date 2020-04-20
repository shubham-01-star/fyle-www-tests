# fyle-www-tests

This repository contains tests for Fyle's website (https://www.fylehq.com). This is under active development.
This is a public repository - please do not check in any passwords or keys.

# Development

* Download and install Chrome webdriver from https://chromedriver.chromium.org/downloads
* Create virtualenv and install requirements using:

```
    virtualenv venv --python=python3.7
    source venv/bin/activate
    pip install -r requirements.txt
```

# Running tests

To run all tests:

```
    python -m pytest
```

To run only tests for homepage:

```
    python -m pytest homepage/
```

To run only getdemo tests in homepage:

```
    python -m pytest homepage/test_getdemo.py
```

To run only one specific test:

```    
    python -m pytest homepage/test_getdemo.py::test_success
```