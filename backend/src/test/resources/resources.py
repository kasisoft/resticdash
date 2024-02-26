import os.path


def get_test_resource(filename: str) -> str:
    dir = os.path.dirname(__file__)
    result = os.path.join(dir, filename)
    return result
