# -*- coding: utf-8 -*-

import json

from models import (
    Storage,
)

__author__ = 'sobolevn'


class UserExitException(KeyboardInterrupt):
    pass

class ModelEncoder(json.JSONEncoder):
    def default(self, object):
        storage = Storage
        if isinstance(object, storage):
            return



