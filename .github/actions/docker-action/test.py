import os


def pluralize(quant, singular):
    if int(quant) != 1:
        return singular + "s"
    elif int(quant) == 1:
        return singular


# Docker Action key format converter. Will convert key from, for example, 'key' to 'INPUT_KEY'
def kc(key):
    return "INPUT_" + key.upper()


def run():
    first_name = os.environ[kc("first-name")]
    age = os.environ[kc("age")]

    print(f"Hello {first_name}, you are {age} {pluralize(age, 'year')} old.")

    last_name = "Tolman"

    with open(os.environ["GITHUB_OUTPUT"], "a") as gh_output:
        print(f"last-name={last_name}", file=gh_output)


if __name__ == "__main__":
    run()
