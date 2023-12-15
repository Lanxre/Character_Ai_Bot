import logging
import traceback

from typing import NoReturn

from colorama import Style, Fore

from .types import Colors, LogLevel


class ColoredFormatter(logging.Formatter):
	success: str = "Success"
	error: str = "Error"
	warning: str = "Warning"

	def format(self, record):
		log_message = super(ColoredFormatter, self).format(record)
		return Colors.get(name=record.levelname, default_value='INFO') + log_message + Style.RESET_ALL





class SingletonMeta(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


class FastApiAuthLogger:
	def __init__(self, logger_name: str, level: LogLevel = logging.INFO):
		self.logger = logging.getLogger(logger_name.upper())
		self.logger.setLevel(level or logging.INFO)

		formatter = ColoredFormatter(f'%(levelname)s{Style.RESET_ALL}:\t' +
		                             f'{Fore.LIGHTWHITE_EX}{Style.BRIGHT:6}%(asctime)s\t' +
		                             f'{Fore.RED + Fore.YELLOW}%(name)s\t' +
		                             f'{Fore.LIGHTWHITE_EX}%(message)s',
		                             datefmt='%Hh:%Mm:%Ss | %d/%m/%Y')

		handler = logging.StreamHandler()
		handler.setFormatter(formatter)

		self.logger.addHandler(handler)

	def info(self, message: str) -> NoReturn:
		self.logger.info(message)

	def debug(self, message: str) -> NoReturn:
		self.logger.debug(message)

	def warning(self, message: str) -> NoReturn:
		self.logger.warning(message)

	def error(self, message: str) -> NoReturn:
		self.logger.error(message)

	def critical(self, message: str) -> NoReturn:
		self.logger.critical(message)


class TelegramLogger(FastApiAuthLogger):
	def __init__(self, logger_name: str, level: LogLevel = logging.INFO):
		super().__init__(logger_name, level)

	def error(self, message: str, error: Exception = None) -> NoReturn:
		error_message = f"{message}\n"
		if error:
			traceback_str = traceback.format_exc()
			error_message += f"Error Details:\n{traceback_str}"

		self.logger.error(error_message)