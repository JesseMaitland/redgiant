from jinja2 import Environment
from redgiant.gatekeeper.project import GateKeeperEntryPoint, GateKeeper

DDL_GENERATE_OPTIONS = ['users', 'groups']


class Ddl(GateKeeperEntryPoint):

    entry_point_args = {

        ('--object', '-o'): {
            'help': 'the objects to be rendered',
            'choices': DDL_GENERATE_OPTIONS
        }
    }

    def cmd_render(self):
        gatekeeper = self.project.get_gatekeeper()
        jinja_env = self.project.get_jinja_env('gatekeeper')

        if self.args.object:
            self.save_files(self.args.object, jinja_env, gatekeeper)

        else:
            for key in DDL_GENERATE_OPTIONS:
                self.save_files(key, jinja_env, gatekeeper)

    def save_files(self, name: str, jinja_env: Environment, gatekeeper: GateKeeper):
        ddl_dir = self.project.get_dir(name)
        self.project.clean_dir(name)
        template = jinja_env.get_template(f"{name}.sql")

        for db_object in gatekeeper.db_objects[name].values():
            content = template.render(**{name.rstrip('s'): db_object})
            fp = ddl_dir / f"{db_object.name}.sql"
            fp.touch(exist_ok=True)
            fp.write_text(content)

    @staticmethod
    def print_files(name: str, jinja_env: Environment, gatekeeper: GateKeeper, obj_name: str = None):
        template = jinja_env.get_template(f"{name}.sql")
        template_var = name.rstrip('s')

        if obj_name:
            db_object = gatekeeper.db_objects[name][obj_name]
            content = template.render(**{template_var: db_object})
            print(content)

        else:
            for db_object in gatekeeper.db_objects[name]:
                content = template.render(**{template_var: db_object})
                print(content)
