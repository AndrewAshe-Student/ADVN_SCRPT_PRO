import Project4

# def test_getMakesByYear():
#     output = Project4.getMakesByYear()
#     assert output == "2020"

def test_getMakesByYear():
    output = Project4.testForPytest(1, 2)
    assert output == "Code Pass"