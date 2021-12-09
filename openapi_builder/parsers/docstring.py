import ast
import inspect
import os
import sys


class DocStringParser:
    """Parses a python file and returns the docstring.

    This class can be instantiated from a given class, or from a given filename.

    Usage:
    >>> parser = DocStringParser.from_class(Class)
    >>> parser.parse()

    Retrieving the results:
    >>> parser.result
    """

    def __init__(self, module, prefix=None):
        self.module = module
        self.prefix = prefix
        self.import_names = {}
        self.result = {}

    @classmethod
    def from_class(cls, class_to_process, prefix=None):
        filename = inspect.getfile(class_to_process)
        return cls.from_file(filename=filename, prefix=prefix)

    @classmethod
    def from_file(cls, filename, prefix=None):
        filename = os.path.splitext(filename)[0] + ".py"  # convert .pyc to .py
        with open(filename, "r") as f:
            file_contents = f.read()

        return cls(module=ast.parse(file_contents), prefix=prefix)

    def get_name(self, node):
        prefix = "" if self.prefix is None else f"{self.prefix}."

        if hasattr(node, "name"):
            return prefix + node.name
        else:
            return prefix + node.id

    def parse(self):
        for index, node in enumerate(self.module.body):
            next_node = (
                self.module.body[index + 1]
                if len(self.module.body) > index + 1
                else None
            )
            if isinstance(node, ast.ClassDef):
                for base in node.bases:  # parse super classes
                    full_name = self.import_names[base.id]  # e.g. 'package.sub.ClassA'
                    real_class_name = full_name.split(".")[-1]  # e.g. 'ClassA'.
                    module_name = ".".join(
                        full_name.split(".")[:-1]
                    )  # e.g. 'package.sub'
                    super_class_parser = DocStringParser.from_file(
                        sys.modules[module_name].__file__
                    )
                    super_class_parser.parse()
                    for key, docstring in super_class_parser.result.items():
                        # e.g. key='ClassA.attr_a'
                        if key.startswith(f"{real_class_name}."):  # 'ClassA.'
                            attribute_name = key.split(".")[-1]  # e.g. 'attr_a'
                            own_class_name = f"{node.name}.{attribute_name}"
                            # e.g. own_class_name = 'package.sub.ClassA'
                            self.result[own_class_name] = docstring

                # docstring from class attributes
                current_class_parser = DocStringParser(module=node, prefix=node.name)
                current_class_parser.parse()
                for key, value in current_class_parser.result.items():
                    self.result[key] = value

                # docstring from class definition.
                self.result[self.get_name(node)] = ast.get_docstring(node)
            if isinstance(node, ast.Assign) and isinstance(next_node, ast.Expr):
                self.result[self.get_name(node.targets[0])] = next_node.value.value
            if isinstance(node, ast.ImportFrom):
                for name in node.names:
                    import_name = name.asname if name.asname is not None else name.name
                    self.import_names[import_name] = f"{node.module}.{name.name}"
