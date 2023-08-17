import os
import inflect


# Docker Action key format converter. Will convert key from, for example, 'key' to 'INPUT_KEY'


def set_output(key, val, file):
    print(f"{key}={val}", file=file)


def get_input(key):
    return os.environ["INPUT_" + key.upper()]


def run():
    p = inflect.engine()
    first_name = get_input("first-name")
    age = get_input("age")

    print(f"Hello {first_name}, you are {age} {p.plural('year', int(age))} old.")

    last_name = "Tolman"

    with open(os.environ["GITHUB_OUTPUT"], "a") as gh_output:
        set_output(key="last-name", val=last_name, file=gh_output)


if __name__ == "__main__":
    run()
