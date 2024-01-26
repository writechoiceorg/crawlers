# crawlers

## Readme.io 

The crawler will access every sidebar link from Readme.io and check the translation.

It will save all phrases without translation in a JSON file, with the URL as the key to identify the page needing translation:

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

To ignore strings from pages, add it to the `ignore.json` file.