# Githuber stats
This projet is a little script to retrieve some stats about one or more GitHuber. 
It retrieves the following informations: 

- Global audience - The number of unique users that a user (or organization) can reach with its projects. It's based on the people that had stared a projet (the stargazers), the ones who forked a projet and the other that watched one of their repositoy.
- Fork audience
- Stargazers audience

## Install dependencies
At the projet's root please run:

```bash
pip install -r requirements.txt
```

## Usage of generate_stats.py
```bash
usage: python generate_stats.py [-h] [-a ACCOUNTS] [-o OUTPUT] [-v]

Get GitHub accounts' audience.

optional arguments:
  -h, --help            show this help message and exit
  -a ACCOUNTS, --accounts ACCOUNTS
                        The targeted github accounts separated by comma.
  -o OUTPUT, --output OUTPUT
                        The output file to write data, ex: -a
                        jplusplus,pbellon
  -v, --verbose         Show some information during process


```
