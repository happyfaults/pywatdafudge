from ..lib.lang import LazyObject
from . import has_ntlk

class Tokenizer(LazyObject):

    def set_tokenizer(self):
        raise NotImplementedError

    def ngrams(self, words, n):
        for i in range(0, len(words)):
            yield ' '.join(words[i:i + n])

class SimpleTokenizer(Tokenizer):

    def set_tokenizer(self):
        import re
        self.tokenizer = re.compile(
            r"\w+(?:'\w+)?|[^\w\s]"
        ).findall
        return self.tokenizer

class NltkTokenizer(Tokenizer):

    def set_tokenizer(self):
        from nltk.tokenize import TweetTokenizer #word_tokenize #WhitespaceTokenizer #TweetTokenizer
        self.tokenizer = TweetTokenizer().tokenize #T().tokenize
        return self.tokenizer

if has_ntlk:
    DefaultTokenizer = NltkTokenizer

else:
    DefaultTokenizer = SimpleTokenizer