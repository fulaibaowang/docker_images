# docker_images

One folder / tool

One folder / version

For automated builds a tag needs to be added and pushed.

Tag format must be:

`<tool>-<version>`

eg. `kallisto-0.48.0`, adding tags and commiting eg.:
```
git fetch --tags
git describe --abbrev=0 --tags # get last tag
git tag -e -a kallisto-0.48.0 HEAD
git push
git push origin --tags
```