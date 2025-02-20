import os

def getSubFilePaths(dir_path: str) -> list[str]:
    if dir_path[-1] != "/": dir_path += "/"
    return [dir_path + path for path in os.listdir(dir_path)]