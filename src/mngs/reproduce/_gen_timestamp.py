#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-11-07 17:44:32 (ywatanabe)"
# File: ./mngs_repo/src/mngs/reproduce/_gen_timestamp.py

from datetime import datetime as _datetime


def gen_timestamp():
    return _datetime.now().strftime("%Y-%m%d-%H%M")

timestamp = gen_timestamp

# EOF
