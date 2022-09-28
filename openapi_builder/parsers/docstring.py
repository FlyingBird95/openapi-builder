import ast
import inspect
import os
import sys


class DocStringParser:
    """
    Parses a python file and returns the docstring.

    This class can be instantiated from a given class, or from a given filename.
    Usage:
    >>> class A:
    >>>    '''Some docstring for this class.'''
    >>>
    >>>    a = 42
    >>>    '''Description of A.'''
    >>> parser = DocStringParser.from_class(A)
    >>> parser.parse()

    Retrieving the results:
    >>> parser.result
    >>> {}

    Limitations:
    - The class must be placed in a file (doesn't work from a python shell)
    - The class must be defined in the root content of a file (a class
      definition in a function is not supported).
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
            if isinstance(node, ast.ImportFrom):
                self._process_import_from(node=node)
            elif isinstance(node, ast.Import):
                self._process_import(node=node)
            elif isinstance(node, ast.ClassDef):
                self._process_class_definition(node=node)
            elif isinstance(node, ast.Assign) and isinstance(next_node, ast.Expr):
                self._process_docstring_from_assignment(node=node, next_node=next_node)

    def _process_import_from(self, node: ast.ImportFrom):
        """Processes 'from package import class' statements."""
        for name in node.names:
            import_name = name.asname if name.asname is not None else name.name
            self.import_names[import_name] = f"{node.module}.{name.name}"

    def _process_import(self, node: ast.Import):
        """Processes 'import package' statements."""
        for name in node.names:
            import_name = name.asname if name.asname is not None else name.name
            self.import_names[import_name] = import_name

    def _process_class_definition(self, node: ast.ClassDef):
        """Processes 'class A(Base): ... definitions."""
        for base in node.bases:  # parse super classes
            try:
                if isinstance(base, ast.Name):
                    if base.id == "object":
                        return
                    full_name = self.import_names[base.id]
                else:
                    full_name = (
                        self.import_names[base.value.id] + "." + base.attr
                    )  # e.g. 'package.sub.ClassA'
            except KeyError:
                print(f"Don't know how to process this. {base}")
                return
            real_class_name = full_name.split(".")[-1]  # e.g. 'ClassA'.
            module_name = ".".join(full_name.split(".")[:-1])  # e.g. 'package.sub'
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

    def _process_docstring_from_assignment(self, node: ast.Assign, next_node: ast.Expr):
        """
        Processes the following lines.

        >>> answer_of_life = 42
        >>> '''Description why the answer of life = 42.'''
        """
        self.result[self.get_name(node.targets[0])] = next_node.value.value
