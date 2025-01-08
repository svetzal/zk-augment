import re
import textwrap


def rewrap(content: str, width=80, indent=0) -> str:
    stripped = content.strip()
    unwrapped = stripped.replace("\n", " ")
    condensed = re.sub(r'\s+', ' ', unwrapped)
    return "\n".join(textwrap.wrap(condensed, width=width, initial_indent=" "*indent, subsequent_indent=" "*indent, replace_whitespace=True, drop_whitespace=True))
