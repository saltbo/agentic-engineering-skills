import re


ETAG = '"v2"'
ENTITY_TAG = r'(?:W/)?"[\x21\x23-\x7e\x80-\xff]*"'
TAG_LIST = rf'[ \t]*(?:{ENTITY_TAG})?[ \t]*(?:,[ \t]*(?:{ENTITY_TAG})?[ \t]*)*'


def _matches(if_none_match):
    if if_none_match is None:
        return False
    if if_none_match.strip(' \t') == '*':
        return True
    if re.fullmatch(TAG_LIST, if_none_match) is None:
        return False
    return any(tag.removeprefix('W/') == ETAG
               for tag in re.findall(ENTITY_TAG, if_none_match))


def get(if_none_match=None):
    if _matches(if_none_match):
        return 304, {'ETag': ETAG}, b''
    return 200, {'ETag': ETAG}, b'current representation'
