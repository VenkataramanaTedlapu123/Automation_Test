# tests/test_calculator.py
import logging
from app.calculator import add, divide

logger = logging.getLogger("pytests_demo")

def test_add():
    logger.info("Running test_add")
    assert add(2, 3) == 5

def test_divide_by_zero():
    logger.info("Running test_divide_by_zero")
    try:
        divide(1, 0)
    except ZeroDivisionError:
        logger.exception("Caught ZeroDivisionError as expected")
        assert True
    else:
        assert False, "Expected ZeroDivisionError"
