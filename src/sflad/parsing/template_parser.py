"""Log template parser: the template of a line is the line with its variable tokens masked."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Iterable, List, Tuple


_HEX = re.compile(r"\b[0-9a-fA-F]{8,}\b")
_UUID = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
)
# ISO-8601 first so CloudWatch timestamps do not leak ms digits into template IDs.
_ISO_TS = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?")
_NUM = re.compile(r"\b\d+(?:\.\d+)?\b")
_IP = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
# A letter prefix fused onto 3+ digits (e.g. "V133318") has no \b before its digits, so _NUM alone misses it.
_ALNUM_ID = re.compile(r"\b[A-Za-z]+\d{3,}\b")

def _mask_variables(message: str) -> str:
    """Mask volatile tokens (ISO timestamps, ids, numbers) so equal log shapes share one template ID."""
    s = _ISO_TS.sub("<TS>", message)
    s = _UUID.sub("<UUID>", s)
    s = _IP.sub("<IP>", s)
    s = _HEX.sub("<HEX>", s)
    s = _ALNUM_ID.sub("<ID>", s)
    s = _NUM.sub("<NUM>", s)
    return s


@dataclass
class ParseResult:
    template_id: str
    template: str
    message: str


class TemplateParser:
    """Regex parser whose template is the masked message."""

    def parse(self, message: str) -> ParseResult:
        template = _mask_variables(message.strip())
        tid = hashlib.md5(template.encode("utf-8")).hexdigest()[:10]
        return ParseResult(template_id=tid, template=template, message=message)


def build_parser() -> TemplateParser:
    return TemplateParser()


def assign_templates(messages: Iterable[str], parser) -> Tuple[List[str], List[str]]:
    """Parse messages; return (template_ids, templates)."""
    ids: List[str] = []
    templates: List[str] = []
    for msg in messages:
        r = parser.parse(msg)
        ids.append(r.template_id)
        templates.append(r.template)
    return ids, templates
