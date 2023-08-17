import os
import inflect


# Docker Action key format converter. Will convert key from, for example, 'key' to 'INPUT_KEY'
def kc(key):
    return "INPUT_" + key.upper()


def set_output(key, val, file):
    print(f"{key}={val}", file=file)


def run():
    p = inflect.engine()
    first_name = os.environ[kc("first-name")]
    age = os.environ[kc("age")]

    print(f"Hello {first_name}, you are {age} {p.plural('year', int(age))} old.")

    last_name = "Tolman"

    with open(os.environ["GITHUB_OUTPUT"], "a") as gh_output:
        set_output(key="last-name", val=last_name, file=gh_output)


if __name__ == "__main__":
    run()
