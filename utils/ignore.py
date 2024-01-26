def ignore_cases(text, ignore_misses, ignore_data):
    try:
        int(text)
        return True
    except ValueError:
        pass

    if (
        text in ignore_data
        or text in ignore_misses
        or text.startswith(("https://", "http://"))
        or text in "📘🚧❗️👍."
        or not text
    ):
        return True
    return False
