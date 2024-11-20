import os
from pathlib import Path

def get_save_path(filename: str) -> str:
    filename = filename.replace("documents/", "")
    return Path.cwd().joinpath("data").joinpath(filename).__str__()

def is_already_in_fakes(filename: str) -> bool:
    filepath = Path.cwd().joinpath("fakedata").joinpath(filename)
    if filepath.exists():
        filepath.replace(Path.cwd().joinpath("data").joinpath(filename))
        return True
    else:
        Path.cwd().joinpath("data").joinpath(filename).replace(filepath)
        return False
        