#!/usr/bin/env python3

from typing import Tuple
from enum import Enum

#EyePattern = Tuple[str, str, str, str, str]
EyeLinePattern = Tuple[int, int, int, int, int]
EyePattern = Tuple[EyeLinePattern, EyeLinePattern, EyeLinePattern, EyeLinePattern, EyeLinePattern]

InnerEyeLine = Tuple[int, int, int]
InnerEye = Tuple[InnerEyeLine,InnerEyeLine,InnerEyeLine]

class InnerEyeType(Enum):
    TypeHorizontal = 0
    TypeVertical = 1
    TypePlus = 2
    TypeDiagonal = 3

EYE_PATTERN_BASE: EyePattern = [
                [1,1,1,1,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,1,1,1,1]]

EYE_INNER_PATTERN_1: InnerEye = [
                [0,0,0],
                [1,1,1],
                [0,0,0]]

EYE_INNER_PATTERN_2: InnerEye = [
                [0,1,0],
                [0,1,0],
                [0,1,0]]

EYE_INNER_PATTERN_3: InnerEye = [
                [0,1,0],
                [1,1,1],
                [0,1,0]]

EYE_INNER_PATTERN_4: InnerEye = [
                [1,0,1],
                [0,1,0],
                [1,0,1]]

EYE_PATTERN_1: EyePattern = (
  "/---\\",
  "|   |",
  "|-o-|",
  "|   |",
  "\\---/"
)

EYE_PATTERN_2: EyePattern = (
  "/---\\",
  "| | |",
  "| 0 |",
  "| | |",
  "\\---/"
)

EYE_PATTERN_3: EyePattern = (
  "/---\\",
  "| | |",
  "|-q-|",
  "| | |",
  "\\---/"
)

EYE_PATTERN_4: EyePattern = (
  "/---\\",
  "|\\ /|",
  "| w |",
  "|/ \\|",
  "\\---/"
)