import importlib

__version__ = '1.0.0-dev6'


def _import_class_from_string(class_path):
    if not class_path:
        return None
    module_path, class_name = class_path.rsplit('.', 1)
    return getattr(importlib.import_module(module_path), class_name)
