def check_if_translated(text, data):
    return bool(data) and text in data


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
