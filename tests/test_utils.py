from utils import is_support_file_type


def test_is_support_file_type():

    test_path1 = "hello.jpg"
    test_path2 = "hello.png"
    test_path3 = "hello.jpeg"
    test_path4 = "hello.gif"

    assert is_support_file_type(test_path1)
    assert is_support_file_type(test_path2)
    assert is_support_file_type(test_path3)
    assert not is_support_file_type(test_path4)
