import importlib


def load_class_from_path(class_path):
    conf = None
    if ";" in class_path:
        parts = class_path.split(";")
        class_path = parts[0]
        conf = {p.split("=")[0]: p.split("=")[1] for p in parts[1:]}
    module_parts = class_path.split(".")
    module = importlib.import_module(".".join(module_parts[:-1]))
    class_ = getattr(module, module_parts[-1])
    if conf is not None:
        return class_(**conf)
    else:
        return class_()
