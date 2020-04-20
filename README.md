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

You should see output like this:

```
(venv) laptop:fyle-www-tests siva$ python -m pytest
============================================= test session starts =============================================
platform darwin -- Python 3.7.4, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /Users/siva/src/fyle-www-tests, inifile: pytest.ini
collected 3 items                                                                                             

homepage/test_getdemo.py::test_bad_email PASSED                                                         [ 33%]
homepage/test_getdemo.py::test_missing_firstname PASSED                                                 [ 66%]
homepage/test_getdemo.py::test_success PASSED                                                           [100%]

============================================= 3 passed in 40.07s ==============================================
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