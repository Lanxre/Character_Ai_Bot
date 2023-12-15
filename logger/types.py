from enum import IntEnum
from typing import Optional, Annotated

from colorama import Fore, Style


class Colors:
	DEBUG = Fore.BLUE
	INFO = Fore.GREEN
	WARNING = Fore.YELLOW
	ERROR = Fore.RED
	CRITICAL = Style.BRIGHT + Fore.RED

	@classmethod
	def get(cls, name: Optional[str], default_value: str) -> Annotated[Fore, str]:
		return cls.__dict__.get(name) if name is not None else default_value


class LogLevel(IntEnum):
	CRITICAL = 50
	FATAL = CRITICAL
	ERROR = 40
	WARNING = 30
	WARN = WARNING
	INFO = 20
	DEBUG = 10
	NOTSET = 0
