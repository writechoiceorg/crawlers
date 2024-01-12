# PagBank documentation translation validator

The crawler will access every API Reference page from PagBank and check if all the english translation.

It will save all phrases without translation in a JSON named `missing_translation.json`, with the URL as key to identify the page needing translation:

```json
{
  "https://dev.pagbank.uol.com.br/reference/introducao": [
    "Lorem Ipsum",
    "dolor sit amet",
    "consectetur adipiscing elit,",
    "sed do eiusmod tempor incididunt ut labore et dolore magna",
    "."
  ],
  "https://dev.pagbank.uol.com.br/reference/funcionalidades-disponiveis": [
    ...
  ],
}
```

### Ignoring strings

To ignore strings from pages, the `ignore.json` file will follow the format from the created JSON above. The code will ignore any strings related to each URL.