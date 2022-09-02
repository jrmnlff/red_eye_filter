#!/usr/bin/env python3

from utils.eye_pattern import InnerEyeType

class Eye:
    def __init__(self, point: int, type: InnerEyeType):
        self.point = point
        self.type = type
         