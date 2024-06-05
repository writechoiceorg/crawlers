def check_if_translated(text, data):
    return True if text in data else False


def ignore_cases(text, ignore_data):
    try:
        int(text)
        return True
    except ValueError:
        pass

    if (
        text in ignore_data
        or text.startswith(
            (
                "https://",
                "http://",
                "Exemplo:",
                "Ejemplo:",
                "Example:",
                "* ",
                "//",
            )
        )
        or text in "📘🚧❗️👍."
        or not text
    ):
        return True
    return False
