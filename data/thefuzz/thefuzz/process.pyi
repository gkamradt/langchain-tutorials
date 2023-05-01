from collections.abc import Mapping
import typing
from typing import Any, Callable, Union, Tuple, Generator, TypeVar, Sequence


ChoicesT = Union[Mapping[str, str], Sequence[str]]
T = TypeVar('T')
ProcessorT = Union[Callable[[str, bool], str], Callable[[Any], Any]]
ScorerT = Callable[[str, str, bool, bool], int]


@typing.overload
def extractWithoutOrder(query: str, choices: Mapping[str, str], processor: ProcessorT, scorer: ScorerT, score_cutoff: int = ...) -> Generator[Tuple[str, int, str], None, None]: ...


@typing.overload
def extractWithoutOrder(query: str, choices: Sequence[str], processor: ProcessorT, scorer: ScorerT, score_cutoff: int = ...) -> Generator[Tuple[str, int], None, None]: ...
