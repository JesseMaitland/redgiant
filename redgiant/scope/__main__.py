from rsterm import run_entry_point
from pathlib import Path


def main():
    try:
        run_entry_point(Path(__file__).absolute().parent / "redscope.yml")
    except FileNotFoundError:
        run_entry_point()


if __name__ == '__main__':
    main()
