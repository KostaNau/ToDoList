# -*- coding: utf-8 -*-

"""
This module contains all the models we work with.
"""

__author__ = 'sobolevn'

from utils import get_input_function


class Storage(object):
    """
    Singleton class to store the current state. Read about it:
    https://ru.wikipedia.org/wiki/%D0%9E%D0%B4%D0%B8%D0%BD%D0%BE%D1%87%D0%BA%D0%B0_(%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)
    """

    obj = None
    items = None

    @classmethod
    def __new__(cls, *args):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
            cls.items = []
        return cls.obj


class BaseItem(object):
    """
    Basic class for all items, provides basic methods and values.
    This class has to be subclassed in order to create new items.
    """

    def __init__(self, heading):
        self.heading = heading
        self.done = False

    def __repr__(self):
        """
        Magic method. Returns basic representation for the command instance.
        https://habrahabr.ru/sandbox/82471/
        """
        return self.__class__

    def __dir__(self):

        return self.__dir__

    @classmethod
    def construct(cls):
        """
        Factory method to create new instances of the class. Read about it:
        https://ru.wikipedia.org/wiki/%D0%A4%D0%B0%D0%B1%D1%80%D0%B8%D1%87%D0%BD%D1%8B%D0%B9_%D0%BC%D0%B5%D1%82%D0%BE%D0%B4_(%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)
        """
        raise NotImplemented()

    @classmethod
    def append_previous_obj(cls):

        raise NotImplemented()


class ToDoItem(BaseItem):
    def __str__(self):
        return '{} ToDo: {}'.format(
                '+' if self.done else '-',
                self.heading
        )

    def __dir__(self):
        return(self.__class__.__name__, self.done, self.heading)

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        heading = input_function('Input heading: ')
        return ToDoItem(heading)

    @classmethod
    def append_previous_obj(cls, *args):
        cls.done = args[0][0]
        heading = args[0][1]
        return ToDoItem(heading)




class ToBuyItem(BaseItem):
    def __init__(self, heading, price):
        super(ToBuyItem, self).__init__(heading)
        self.price = price

    def __str__(self):
        return '{} ToBuy: {} for {}'.format(
                '+' if self.done else '-',
                self.heading,
                self.price,
        )

    def __dir__(self):
        return(self.__class__.__name__, self.done, self.heading, self.price)

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        heading = input_function('Input heading: ')
        price = input_function('Input price: ')
        return ToBuyItem(heading, price)

    @classmethod
    def append_previous_obj(cls, *args):
        cls.done = args[0][0]
        heading = args[0][1]
        price = args[0][2]
        return ToBuyItem(heading, price)

class ToReadItem(BaseItem):
    def __init__(self, heading, author):
        super(ToReadItem, self).__init__(heading)
        self.author = author

    def __str__(self):
        return '{} ToRead: {} by {}'.format('+' if self.done else '-', self.heading, self.author)

    def __dir__(self):
        return(self.__class__.__name__, self.done, self.heading, self.author)

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        heading = input_function('Input Title: ')
        author = input_function('Input Author: ')
        return ToReadItem(heading, author)


    @classmethod
    def append_previous_obj(cls, *args):
        cls.done = args[0][0]
        heading = args[0][1]
        author = args[0][2]
        return ToReadItem(heading, author)
