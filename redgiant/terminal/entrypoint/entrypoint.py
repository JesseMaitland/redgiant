import sys
from typing import Dict, Tuple, List
from abc import ABC
from argparse import ArgumentParser, Namespace
from redgiant.terminal.config import RedGiantConfig
from redgiant.terminal.project import RedGiantProject


def parse_cmd_args(args_config: Dict[Tuple[str, str], Dict[str, str]], arg_index: int = 0) -> Namespace:
    """
    Parse command line args in one call, using a dict as a configuration.
    Args:
        args_config: Dict[Tuple, Dict[str, Any]] according to standard lib ArgumentParser kwargs
        arg_index:   int starting index of the arguments to be parsed from sys.argv

    Returns: Namespace
    """
    arg_parser = ArgumentParser()

    for command, options in args_config.items():
        arg_parser.add_argument(*command, **options)
    return arg_parser.parse_args(sys.argv[arg_index:])


class EntryPoint(ABC):
    """
    Base class to be used by all program entry points. If specific arguments are to be used for the
    inheriting child class, then the entry_point_args dictionary can be overridden with the format
    below

    entry_point_args = {
        ('arg or --flag', None or -f): {
            'ArgumentParser kwargs': 'ArgumentParser values'
        }
    }

    """

    # override this class dict with any arguments which apply only to this entry point
    # or which would otherwise apply to all descendant EntryPoint objects.
    entry_point_args = {}

    def __init__(self):

        self.config: RedGiantConfig = RedGiantConfig()
        self.args: Namespace = parse_cmd_args(self.entry_point_args, arg_index=3)
        self.project = RedGiantProject(self.config.get_project_root())

    def run(self, action_name: str) -> None:

        try:
            action = getattr(self, f"cmd_{action_name}")
            action()
        except IndexError:
            print("A verb must be provided as the second argument")
            print(f"For object {self.name()} the actions are {action_name}")
            exit()

        except AttributeError:
            print(f"{action_name} is not a valid action for object {self.name()}")
            print(f"For object {self.name()} the actions are {action_name}")
            exit()

    @classmethod
    def get_actions(cls) -> List[str]:
        return [a.replace('cmd_', '') for a in cls.__dict__.keys() if a.startswith('cmd_')]

    @classmethod
    def name(cls) -> str:
        """
        Returns: str the name of this class in snake case
        """
        name = cls.__name__
        snake = ''.join([f'_{c.lower()}' if c.isupper() else c for c in name])
        return snake.lstrip('_')

    @classmethod
    def validate_class_name(cls) -> None:
        """
        Will raise an Exception if the class name is more than 2 words.
        """
        underscores = 0
        for char in cls.name():
            if char == '_':
                underscores += 1

        if underscores > 1:
            raise Exception("Class names must consists of 2 words, ideally in the format VerbNoun.")

    @classmethod
    def is_entry_point(cls) -> bool:
        """
        Used for discovery
        Returns: True if this is a child class
        """
        return False if cls.__name__ == 'EntryPoint' else True
