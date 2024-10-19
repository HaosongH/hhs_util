import yaml
import os

def read_yaml(path):
    # Read configurations
    with open(path, 'r', encoding='utf-8') as stream:
        configs = yaml.safe_load(stream)
        return configs
