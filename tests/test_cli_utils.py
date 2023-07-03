from cli_utils import get_filename_from_funcname


def test_get_filename_from_funcname():
    assert get_filename_from_funcname('load_iris') == 'iris.csv'
    assert get_filename_from_funcname('load_breast_cancer') == 'breast_cancer.csv'
