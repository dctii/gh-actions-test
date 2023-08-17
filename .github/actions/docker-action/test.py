import os


def pluralize(quant, singular):
    if int(quant) != 1:
        return singular + "s"
    elif int(quant) == 1:
        return singular


def run():
    first_name = os.environ["first-name"]
    age = os.environ["age"]

    print(f"Hello {first_name}, you are {age} {pluralize(age, 'year')} old.")

    last_name = "Tolman"

    with open(os.environ["GITHUB_OUTPUT"], "a") as gh_output:
        print(f"last-name={last_name}", file=gh_output)


if __name__ == "__main__":
    run()
