## Bot Releases

#### Stage changes

```sh
git add .
```

#### Commit changes

```sh
git commit -m "Prepare release v1.0.0"
```

#### Push changes to GitHub

```sh
git push origin main
```

#### Create and push a new tag

```sh
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

#### Create a release with details

```sh
gh release create v1.0.0 --title "Initial Release" --notes "This is the initial release of my project."
```
