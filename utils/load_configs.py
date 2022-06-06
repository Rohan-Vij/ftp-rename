"""Importing data from .yaml configuration files"""
import yaml

def load_file(filename):
    """
    Loads a yaml file.

    :returns: a dictionary of the data in the file
    """
    with open(filename, "r", encoding="utf-8") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            return {"error": exc}
            