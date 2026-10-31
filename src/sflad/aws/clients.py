"""boto3 clients for the evaluation runs."""

from __future__ import annotations

import os
from typing import Optional

import boto3


def region_name(default: str = "eu-west-1") -> str:
    return (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or default
    )


def make_client(service: str, region: Optional[str] = None, config=None):
    return boto3.client(service, region_name=region or region_name(), config=config)
