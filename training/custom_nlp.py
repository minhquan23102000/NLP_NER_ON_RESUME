from spacy.tokens import Doc
from spacy.util import DummyTokenizer, get_words_and_spaces
from spacy.vocab import Vocab
from underthesea import word_tokenize


class VietnameseTokenizer(DummyTokenizer):
    def __init__(self, vocab: Vocab):
        self.vocab = vocab

    def __reduce__(self):
        return VietnameseTokenizer, (self.vocab)

    def __call__(self, text: str) -> Doc:
        words = word_tokenize(text)
        words, spaces = get_words_and_spaces(words, text)
        return Doc(self.vocab, words=words, spaces=spaces)

