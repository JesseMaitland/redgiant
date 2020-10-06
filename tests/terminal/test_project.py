from unittest import TestCase
from unittest.mock import MagicMock
from pathlib import Path
from redgiant.terminal.project import RedGiantProject


class TestRedGiantProject(TestCase):

    def setUp(self) -> None:
        self.root_name = "foo"

    def test_dir_keys(self):
        redgiant_project = RedGiantProject(root_name=self.root_name)
        for key in redgiant_project.dirs.keys():
            self.assertIn(key, RedGiantProject.MODULE_NAMES + ['root'])
