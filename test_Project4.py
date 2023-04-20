import Project4
import pytest

# def test_getMakesByYear():
#     output = Project4.getMakesByYear()
#     assert output == "2020"

# PyTest definitions and parameters
@pytest.fixture
def a2():
    return 1

@pytest.fixture
def b2():
    return 2

def test_testForPytest():
    Project4.testForPytest(1, 2)