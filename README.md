# informatiCup 2021 solution

## Build

```
docker build -t informaticup-solution .
```

If you rather like to use a pre-built docker image, you can also [pull it from GitHub](https://github.com/orgs/informatiCup/packages/container/package/icup2021_example):

```
docker pull ghcr.io/informaticup/icup2021_example
docker tag ghcr.io/informaticup/icup2021_example icup2021_example
```

## Run

```
docker run -e URL="wss://msoll.de/spe_ed" -e KEY="<Your API key>" -e TIME_URL "https://msoll.de/spe_ed_time" icup2021_example
```
