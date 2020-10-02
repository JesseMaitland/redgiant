from redgiant.terminal.entrypoint import EntryPoint


class Project(EntryPoint):
    """
    creates the necessary root directories for the gatekeeper project
    """
    def cmd_new(self) -> None:
        self.project.init_project("gatekeeper")


