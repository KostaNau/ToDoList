# -*- coding: utf-8 -*-

"""
This module contains all the commands we work with.
If you want to create a new command it should be placed here.
"""


from __future__ import print_function

import sys
import inspect
import json
import pickle

# import custom_exceptions
from custom_exceptions import (
    UserExitException
    # ModelEncoder
)

from models import (
    BaseItem,
    ToDoItem,
    ToBuyItem,
    ToReadItem,
    Storage,
)
from utils import get_input_function

ENCODING = 'utf-8'
JSON_INDENT = 4

__author__ = 'sobolevn & Konstanin Naumov'


class BaseCommand(object):
    """
    Main class for all the commands.
    Defines basic method and values for all of them.
    Should be subclassed to create new commands.
    """

    @staticmethod
    def label():
        """
        This method is called to get the commands short name:
        like `new` or `list`.
        """
        raise NotImplemented()

    def perform(self, objects, *args, **kwargs):
        """
        This method is called to run the command's logic.
        """
        raise NotImplemented()


class ListCommand(BaseCommand):
    @staticmethod
    def label():
        return 'list'

    def perform(self, objects, *args, **kwargs):
        if len(objects) == 0:
            print('There are no items in storage.')
            return

        for index, obj in enumerate(objects):
            print('{}: {}'.format(index, str(obj)))


class NewCommand(BaseCommand):
    @staticmethod
    def label():
        return 'new'

    @staticmethod
    def _load_item_classes():
        # Dynamic load:
        # def class_filter(klass):
        #     return inspect.isclass(klass) \
        #            and klass.__module__ == BaseItem.__module__ \
        #            and issubclass(klass, BaseItem) \
        #            and klass is not BaseItem
        #
        # classes = inspect.getmembers(
        #         sys.modules[BaseItem.__module__],
        #         class_filter,
        # )
        classes = {
            'ToDoItem': ToDoItem,
            'ToBuyItem': ToBuyItem,
            'ToReadItem': ToReadItem,
        }
        return dict(classes)

    def perform(self, objects, *args, **kwargs):
        classes = self._load_item_classes()

        print('Select item type:')
        for index, name in enumerate(classes.keys()):
            print('{}: {}'.format(index, name))

        input_function = get_input_function()
        selection = None

        while True:
            try:
                selection = int(input_function('Input number: '))
                break
            except ValueError:
                print('Bad input, try again.')

        selected_key = list(classes.keys())[selection]
        selected_class = classes[selected_key]
        print('Selected: {}'.format(selected_class.__name__))
        print()

        new_object = selected_class.construct()

        objects.append(new_object)
        print('Added {}'.format(str(new_object)))
        print()
        return new_object


class ExitCommand(BaseCommand):
    @staticmethod
    def label():
        return 'exit'

    def perform(self, objects, *args, **kwargs):
        raise UserExitException('See you next time!')


class DoneCommand(BaseCommand):
    @staticmethod
    def label():
        return 'done'

    def perform(self, objects, *args, **kwargs):
        items = [obj for obj in objects if obj.done is False]
        if len(items) == 0:
            print('There are no undone tasks')
            return

        print('Select task:')
        for index, item in enumerate(items):
            print('{}: {}'.format(index, item))

        selector = None
        input_function = get_input_function()

        while True:
            try:
                selector = int(input_function('Input number: ')[0])
                break
            except ValueError:
                print('Bad input, try again.')

        items[selector].done = True

        print("Task '{}' marked as Done(+)\n".format(str(objects[selector])[2:]))


class UndoneCommand(BaseCommand):
    @staticmethod
    def label():
        return 'undone'

    def perform(self, objects, *args, **kwargs):
        items = [obj for obj in objects if obj.done is True]
        if len(items) == 0:
            print('There are no undone tasks')
            return

        print('Select task:')
        for index, item in enumerate(items):
            print('{}: {}'.format(index, item))

        selector = None
        input_function = get_input_function()

        while True:
            try:
                selector = int(input_function('Input number: ')[0])
                break
            except ValueError:
                print('Bad input, try again.')

        items[selector].done = False

        print("Task '{}' marked as unDone(+)\n".format(str(objects[selector])[2:]))


class SaveCommand(BaseCommand):
    @staticmethod
    def label():
        return 'save'

    def perform(self, objects, *args, **kwargs):
        if args[0] == None:
            print("Can't save. For activate save option you should restart program with optional key --storage")
        else:
            # with open(args[0], 'w', encoding=ENCODING) as storage_file:
            #     json.dump(item=objects, cls=ModelEncoder, ensure_ascii=False, indent=JSON_INDENT)
            dump_for_save = tuple()
            for obj in objects:
                _dump_for_save = (obj.__dir__(), )
                dump_for_save += _dump_for_save
            with open(args[0], 'w', encoding=ENCODING) as storage_file:
                json.dump(dump_for_save, storage_file,  ensure_ascii=False, indent=JSON_INDENT)
            print('Your ToDo list have successfully saved into file: {}.'.format(args[0]))


class OpenCommand(BaseCommand):
    @staticmethod
    def label():
        return 'open'

    @staticmethod
    def _load_item_classes():

        classes = {
                'ToDoItem': ToDoItem,
                'ToBuyItem': ToBuyItem,
                'ToReadItem': ToReadItem,
        }
        return classes

    def perform(self, objects, *args, **kwargs):
        if args[0] == None:
            print('No file for load data')
        else:
            classes = self._load_item_classes()
            storage = Storage()
            with open(args[0], 'r', encoding=ENCODING) as _file:
                user_data = json.load(_file)
                for obj in user_data:
                    obj_class = classes[obj[0]]
                    cls_atr = obj[1:]
                    instance = obj_class.append_previous_obj(cls_atr)
                    objects.append(instance)
        return
