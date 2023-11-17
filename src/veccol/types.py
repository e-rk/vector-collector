#
# Copyright (c) 2023 Rafał Kuźnia <rafal.kuznia@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
from typing import Any

@dataclass
class PreConfig:
    commands: list[str]

@dataclass
class Value:
    name: str
    expr: str
    format: str

@dataclass
class Point:
    locspec: str
    values: list[Value]

@dataclass
class Collect:
    name: str
    points: list[Point]

@dataclass
class Config:
    collect: list[Collect]

@dataclass
class Spec(YAMLWizard):
    pre_config: PreConfig
    config: Config
    post_config: PreConfig
