"""Class to load config files for the install procedure."""
import yaml
from typing import List


class Step:
    def __init__(
        self,
        title: str,
        type: str,
        content: str,
        command: str = None,
        allow_skip: bool = False,
    ):
        self.title = title
        self.type = type
        self.content = content
        self.command = command
        self.allow_skip = allow_skip


class InstallerConfig:
    def __init__(self, steps: List[Step]):
        self.steps = steps

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as stream:
            try:
                raw_steps = yaml.safe_load(stream)
                raw_steps = dict(raw_steps)["steps"]
            except yaml.YAMLError as exc:
                print(exc)

        steps = [Step(**raw_step) for raw_step in raw_steps]
        return cls(steps)
