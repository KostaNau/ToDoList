# -*- coding: utf-8 -*-

"""
Main file. Contains program execution logic.
"""

from __future__ import print_function

import inspect
import sys
import argparse
import json
import collections

from commands import (
    ListCommand,
    NewCommand,
    ExitCommand,
    DoneCommand,
    UndoneCommand,
    UserExitException,
    SaveCommand,
    OpenCommand,
)
from models import (
    Storage,
)
from utils import get_input_function

ENCODING = 'utf-8'
JSON_INDENT = 4

__author__ = 'sobolevn &  kostanau'


def get_routes():
    """
    This function contains the dictionary of possible commands.
    :return: `dict` of possible commands, with the format: `name -> class`
    """

    # Dynamic load:
    # def class_filter(klass):
    #     return inspect.isclass(klass) \
    #            and klass.__module__ == BaseCommand.__module__ \
    #            and issubclass(klass, BaseCommand) \
    #            and klass is not BaseCommand
    #
    # routes = inspect.getmembers(
    #     sys.modules[BaseCommand.__module__],
    #     class_filter
    # )
    # return dict((route.label(), route) for _, route in routes)

    return {
        ListCommand.label(): ListCommand,
        NewCommand.label(): NewCommand,
        ExitCommand.label(): ExitCommand,
        DoneCommand.label(): DoneCommand,
        UndoneCommand.label(): UndoneCommand,
        SaveCommand.label(): SaveCommand,
        OpenCommand.label(): OpenCommand,
    }


def perform_command(command, *args):
    """
    Performs the command by name.
    Stores the result in `Storage()`.
    :param command: command name, selected by user.
    """

    command = command.lower()
    routes = get_routes()

    try:
        command_class = routes[command]
        command_inst = command_class()

        storage = Storage()
        command_inst.perform(storage.items, args[0])

    except KeyError:
        print('Bad command, try again.')
    except UserExitException as ex:
        print(ex)
        raise


def parse_user_input():
    """
    Gets the user input.
    :return: `str` with the user input.
    """

    input_function = get_input_function()

    message = 'Input your command: (%s): ' % '|'.join(
            get_routes().keys())
    return input_function(message)


def main():
    """
    Main method, works infinitelly until user runs `exit` command.
    Or hits `Ctrl+C` in the console.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--storage', help='name of storage file for save data')
    args = parser.parse_args()

    perform_command('open', args.storage)

    while True:
        try:
            command = parse_user_input()
            perform_command(command, args.storage)
        except UserExitException:
            break
        except KeyboardInterrupt:
            print('Shutting down, bye!')
            break


if __name__ == '__main__':
    main()
