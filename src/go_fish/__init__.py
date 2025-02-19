from go_fish.logging import load_logger
from go_fish.settings import get_settings

settings = get_settings()
load_logger(log_file=settings.log_file)


def main() -> None:
    print("Hello from go-fish!")
