from go_fish.logging import load_logger
from go_fish.settings import settings

load_logger(log_file=settings.log_file)


def main() -> None:
    print("Hello from go-fish!")
