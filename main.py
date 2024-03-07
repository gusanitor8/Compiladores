from src.regex.regex import Regex


def run():
    regex = Regex("ab|c+")
    print(regex.match_finder("ab"))


if __name__ == "__main__":
    run()
