import pkgutil
import inspect
from typing import Dict
from importlib import import_module
from redgiant.terminal.entrypoint import EntryPoint, parse_cmd_args


def collect_entry_points(module_name: str) -> Dict[str, EntryPoint]:

    entrypoints = []
    for _, name, _ in pkgutil.iter_modules(path=[f"redgiant/{module_name}/entrypoints"]):

        module = import_module(name=f"redgiant.{module_name}.entrypoints.{name}")

        for mod_name, obj in inspect.getmembers(module):

            if inspect.isclass(obj) and issubclass(obj, EntryPoint):

                if obj.is_entry_point():
                    entrypoints.append(obj)
    return {entrypoint.name(): entrypoint for entrypoint in entrypoints}


def run_entrypoint(module_name: str) -> None:

    entrypoints = collect_entry_points(module_name)
    actions = {key: value.get_actions() for key, value in entrypoints.items()}
    verb_help = ""

    for key, value in actions.items():
        key_msg = f"{key}:\n"
        value_msg = ""
        for a in value:
            value_msg = value_msg + f"\t{a}\n"
        verb_help = verb_help + key_msg
        verb_help = verb_help + value_msg

    cmds = {
        ('command',): {
            'help': f"available commands are {list(entrypoints.keys())}"
        },

        ('action', ): {
            'help': f"""available actions for each command are \n {verb_help}"""
        }
    }

    ns = parse_cmd_args(cmds, 1)

    entrypoint = entrypoints[ns.command]

    entrypoint().run(ns.action)
