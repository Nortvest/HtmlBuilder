from html_builder.element_creator import HtmlElement


class HtmlBuilder:  # Only for python > 3.6
    """
    Build the HTML structure from class`s tags or other HtmlBuilder

    Example:
        H1 = CreateHtmlElement('h1')
        Div = CreateHtmlElement('div')
        header = HtmlBuilder(H1(text='Hello, world!')).append(Div(class_='hello')) -> HtmlBuilder

        header.to_html() -> html`s str
    """

    __slots__ = ['base', '_structure']

    def __init__(self, base: HtmlElement):
        assert isinstance(base, HtmlElement), 'Can use only HtmlElement`s object'
        self.base = base
        self._structure = {
            base: {}
        }

    def __repr__(self):
        return str(self._structure)

    def __before_after_mixin(self, key, other_element, structure):
        if key == self.base:
            if isinstance(other_element, HtmlBuilder):
                for key_b, value_b in other_element._structure.items():
                    structure[key_b] = value_b
            else:
                structure[other_element] = {}
        return structure

    def before(self, other_element):
        structure = {}
        for key, value in self._structure.items():
            structure = self.__before_after_mixin(key, other_element, structure)
            structure[key] = value
        self._structure = structure
        return self

    def after(self, other_element):
        structure = {}
        for key, value in self._structure.items():
            structure[key] = value
            structure = self.__before_after_mixin(key, other_element, structure)
        self._structure = structure
        return self

    def prepend(self, other_element):
        structure = {}
        for key, value in self._structure.items():
            if key == self.base:
                if isinstance(other_element, HtmlBuilder):
                    for key_b, value_b in other_element._structure.items():
                        value = {key_b: value_b} | value
                else:
                    value = {other_element: {}} | value
            structure[key] = value
        self._structure = structure
        return self

    def append(self, other_element):
        structure = {}
        for key, value in self._structure.items():
            if key == self.base:
                if isinstance(other_element, HtmlBuilder):
                    for key_b, value_b in other_element._structure.items():
                        value[key_b] = value_b
                else:
                    value[other_element] = {}
            structure[key] = value
        self._structure = structure
        return self

    def __recurs_get_html(self, tag: HtmlElement, nested_tags: dict, i_nested: int = 0) -> str:
        html = list()
        html.append('\t'*i_nested + tag.get_open_tag())
        for tag_, nested_tags_ in nested_tags.items():
            if not nested_tags_:
                html.append('\t'*(i_nested + 1) + tag_.to_string())
            else:
                html.append(self.__recurs_get_html(tag_, nested_tags_, i_nested + 1))
        html.append('\t'*i_nested + tag.get_close_tag())
        return '\n'.join(html)

    def get_html(self) -> str:
        html = []
        for tag, nested_tags in self._structure.items():
            if not nested_tags:
                html.append(tag.to_string())
            else:
                html.append(self.__recurs_get_html(tag, nested_tags))
        return '\n'.join(html)
