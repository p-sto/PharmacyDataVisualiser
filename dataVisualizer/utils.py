"""Stores different functions used to internal data manipulation"""


def replace_special_signs(str_to_change: str) -> str:
    """Replace special signs in given string"""
    replacements = {
        '*': '_',
        '.': '_',
        ',': '_',
        '-': '_',
        '__': '_',
        ' ': ''
    }
    replaced = str(str_to_change)
    for key, value in replacements.items():
        replaced = replaced.strip(key).replace(key, value)
    return replaced
