from tree_sitter import Parser
from tree_sitter_languages import get_language

PARSERS = {}

def get_parser(language_name):
    if language_name not in PARSERS:
        lang = get_language(language_name)
        parser = Parser()
        parser.set_language(lang)
        PARSERS[language_name] = parser
    return PARSERS[language_name]
