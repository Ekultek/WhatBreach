def info(string):
    print(
        "[\033[32m i \033[0m] {}".format(string)
    )


def warn(string):
    print(
        "[\033[33m w \033[0m] {}".format(string)
    )


def error(string):
    print(
        "[\033[31m ! \033[0m] {}".format(string)
    )


def prompt(string, lowercase=True):
    question = input(
        "[ ? ] {}: ".format(
            string
        )
    )
    if lowercase:
        return question.lower()
    return question
