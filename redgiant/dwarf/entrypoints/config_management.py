from pathlib import Path
from typing import Dict
from jinja2 import Template, FileSystemLoader, Environment, PackageLoader
from rsterm import EntryPoint
from red_dwarf.project import ProjectContext, provide_project_context, RedDwarfConfig
from red_dwarf.project.enums import ExecutionMethods


class BaseConfigEntry(EntryPoint):

    entry_point_args = {
        ('config_name',): {
            'help': 'The name of the configuration in /red-dwarf/configs'
        }
    }

    def run(self) -> None:
        raise NotImplementedError

    def validate_config_name(self):
        invalid_chars = '!"#$%&\'()*+,/:;<=>?@[\\]^`{|}~ '

        try:
            for char in self.cmd_args.config_name:
                if char in invalid_chars:
                    raise ValueError(f"{invalid_chars} are not allowed in config names.")

        except ValueError as e:
            print(e.args[0])

    @staticmethod
    def render_unload_template(config: RedDwarfConfig, jinja_env: Environment) -> Dict[str, str]:
        templates = {}

        if config.execution.once == ExecutionMethods.ONCE:
            templates[ExecutionMethods.ONCE.name.lower()] = 'unload_once.sql'

        if config.execution.incremental == ExecutionMethods.INCREMENTAL:
            templates[ExecutionMethods.INCREMENTAL.name.lower()] = 'unload_incremental.sql'

        if not templates:
            raise ValueError("at least one execution method must be provided in the configuration.")

        return {key: jinja_env.get_template(value).render(config=config) for key, value in templates.items()}


class NewConfig(BaseConfigEntry):

    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        self.validate_config_name()
        project_context.create_config(self.cmd_args.config_name)


class ShowConfig(BaseConfigEntry):
    """
    TODO: remove this before deployment. Serves as a test entrypoint
    """
    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        self.validate_config_name()
        cfg_name = self.cmd_args.config_name

        raw_cfg = project_context.get_config(cfg_name)
        config: RedDwarfConfig = project_context.parse_config(raw_cfg).get(cfg_name)
        templates = {
            config.execution.once: self.render_unload_template(config.execution.once, config),
            config.execution.incremental: self.render_unload_template(config.execution.incremental, config)
        }

        for k, v in templates.items():
            print(v)


class RenderConfig(BaseConfigEntry):

    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        self.validate_config_name()
        config_name = self.cmd_args.config_name

        # create the rendered directories for this config
        project_context.create_rendered_dir(config_name)

        # get config and render the templates
        raw_config = project_context.get_config(config_name)
        red_dwarf_config: RedDwarfConfig = project_context.parse_config(raw_config).get(config_name)
        rendered_templates = self.render_unload_template(red_dwarf_config, project_context.get_jinja_env())

        # get the rendered directory for this config and save the templates
        rendered_dir = project_context.get_rendered_dir(config_name)
        print(rendered_dir.as_posix())
        project_context.save_rendered_templates(rendered_dir, rendered_templates)
