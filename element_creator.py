class HtmlElement:
    """The base class of all Tags"""

    name = ""
    self_dict = {}

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.name

    def to_string(self):
        """Get full node. Example: <h1>Hello, world!</h1>"""
        return f'{self.get_open_tag()}{self.get_test()}{self.get_close_tag()}'

    def get_test(self):
        """Get a text from a tag if it there is one"""
        return self.self_dict["text"] if "text" in self.self_dict else ""

    def get_open_tag(self):
        """Get the opener tag. Example: <h1>"""
        args = " ".join([f"{var}={self.self_dict[var]}" for var in self.self_dict if var not in ('text', 'name', 'self_dict')])
        args = args.replace('class_', 'class', 1)
        return f'<{self.name} {args}>'

    def get_close_tag(self):
        """Get the closing tag. Example: </h1>"""
        return f'</{self.name}>'


class CreateHtmlElement(type):
    """
    Metaclass for create any tags with attributes

    Example:
        CreateHtmlElement('h1') -> <class '__main__.h1'>
    """

    def __new__(mcs, name: str):
        assert isinstance(name, str), 'Can use only a string'
        return type(name, (HtmlElement, ), {
            '__init__': mcs.__init
        })

    @staticmethod
    def __init(self, **kwargs):
        self.__dict__ = kwargs
        self.name = type(self).__name__
        self.self_dict = self.__dict__
