#!/usr/bin/env python

"""

Manage environment variables like a pro.

1. Install

pip install -U python-dotenv

2. Create .env file at the same level, with content

SECRET_KEY="This is the Secret!"
SECRET_TOO=Message: ${SECRET_KEY} Now with additions!
CONFIG_PATH=${HOME}/.config/foo

3. Use


Docs:
https://github.com/theskumar/python-dotenv
"""

import os
from dotenv import load_dotenv


class imdict(dict):
    """
    https://stackoverflow.com/questions/11014262/how-to-create-an-immutable-dictionary-in-python
    https://www.python.org/dev/peps/pep-0351/
    """
    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

""" Read all system environment variables and also from .env """
_vars = {}
for key in os.environ.keys():
    # print(f'{key}: {os.environ.get(key)}')
    _vars[key] = os.environ.get(key)

""" Make them immutable """
env_vars = imdict(_vars)
