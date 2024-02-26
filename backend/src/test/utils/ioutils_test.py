import os.path
import pytest

from dataclasses import dataclass
from typing import Optional, Dict

from dataclasses_json import dataclass_json

from resources.resources import get_test_resource
from resticdash.resticdashexception import ResticDashException
from resticdash.utils.ioutils import create_temp_file, remove_files, grant_password_file, load_yaml


@dataclass_json
@dataclass
class Person:

    full_name: str
    age: Optional[int] = None


@dataclass_json
@dataclass
class Contacts:

    contacts: Dict[str, Person]


def test_create_temp_file():

    filename = create_temp_file('')
    assert os.path.isfile(filename)


def test_load_yaml():

    invalid = get_test_resource('invalid.yaml')

    with pytest.raises(ResticDashException) as exc_info:
        load_yaml(Contacts, invalid)
    assert str(exc_info.value).startswith(f"Failed to parse '{invalid}'!: (Cause: while parsing a flow node")

    simple = get_test_resource('simple.yaml')
    contacts = load_yaml(Contacts, simple)
    assert str(contacts) == ("Contacts(contacts={'jeff': Person(full_name='Jeff Simeones', age=None), 'beau': "
                             "Person(full_name='Beau Pantalones', age=18)})")


def test_remove_files():

    files = [create_temp_file('') for x in range(10)]
    for file in files:
        assert os.path.isfile(file)

    remove_files(files)
    for file in files:
        assert not os.path.isfile(file)


def test_grant_password_file():

    # 1. created password file
    password_file1, created1 = grant_password_file('mypassword')
    assert os.path.isfile(password_file1)
    assert created1
    assert password_file1 != 'mypassword'

    # 2. don't create a password file
    password_file2, created2 = grant_password_file(password_file1)
    assert os.path.isfile(password_file2)
    assert created2 == False
    assert password_file1 == password_file2



