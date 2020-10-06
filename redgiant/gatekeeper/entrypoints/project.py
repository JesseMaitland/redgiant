from redgiant.gatekeeper.project import GateKeeperEntryPoint


class Project(GateKeeperEntryPoint):
    """
    creates the necessary root directories for the gatekeeper project
    """
    def cmd_new(self) -> None:
        self.project.init_project()


