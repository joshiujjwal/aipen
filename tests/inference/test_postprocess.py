import pytest
from app.utils.postprocess import normalize_whitespace, capitalize_sentences, remove_stray_characters, postprocess


class TestNormalizeWhitespace:
    def test_collapses_multiple_spaces(self):
        assert normalize_whitespace("hello   world") == "hello world"

    def test_strips_leading_trailing(self):
        assert normalize_whitespace("  hello  ") == "hello"

    def test_handles_newlines(self):
        assert normalize_whitespace("hello\n\nworld") == "hello world"


class TestCapitalizeSentences:
    def test_capitalizes_first_word(self):
        result = capitalize_sentences("hello world")
        assert result[0].isupper()

    def test_capitalizes_after_period(self):
        result = capitalize_sentences("hello world. how are you")
        assert "How" in result


class TestPostprocess:
    def test_full_pipeline(self):
        raw = "  hello   world.  how are you  "
        result = postprocess(raw)
        assert result == "Hello world. How are you"

    def test_empty_string(self):
        assert postprocess("") == ""
