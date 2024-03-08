from src.regex.regex import Regex


def run():
    regex = Regex("ab|c+")
    print(regex.search("kkkab"))


if __name__ == "__main__":
    run()
