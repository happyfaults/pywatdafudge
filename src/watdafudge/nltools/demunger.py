from ..lib.lang import LazyObject

class TextDemunger(LazyObject):

    @classmethod
    def Default(cls, additional_chars_map=None):
        # (char, replace_char)
        from collections import OrderedDict
        chars_map = OrderedDict([
            ('0','o'),
            ('$','s'),
            ('@', 'a'),
            ('3', 'e'),
            ('!', 'i'),
            ('*', 'u')
        ])
        if additional_chars_map:
            chars_map.update(additional_chars_map)
        return cls(chars_map)

    def __init__(self, chars_map):
        self.chars_map = chars_map

    def process(self, text):
        for char,repl_char in self.chars_map.items():
            text = text.replace(char, repl_char)
        return text
