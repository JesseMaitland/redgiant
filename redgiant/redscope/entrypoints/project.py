from redgiant.redscope.project import RedScopeEntryPoint


class Project(RedScopeEntryPoint):

    def cmd_new(self):
        self.project.init_project()
