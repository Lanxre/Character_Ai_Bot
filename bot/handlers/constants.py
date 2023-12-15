from pathlib import Path
from typing import Union, Dict


def get_images_in_directory(directory_path: Union[str, Path]) -> Dict[str, str]:
	images = {}

	directory_path = Path(directory_path)
	if not directory_path.is_dir():
		return images

	for filepath in directory_path.iterdir():
		if filepath.is_file() and filepath.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif'}:
			images[filepath.name.split('.')[0]] = str(filepath)

	return images


IMAGE_DIR = Path(__file__).parent.parent.parent / 'assets'
IMAGE_COMMANDS_DIR = IMAGE_DIR / 'commands'

IMAGE_COMMANDS = get_images_in_directory(directory_path=IMAGE_COMMANDS_DIR)