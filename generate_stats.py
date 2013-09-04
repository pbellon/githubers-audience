from lib.githuber_stats import GitHuberStats
import argparse

from StringIO import StringIO
import sys 
import os
import json 
import time
import getpass

# Eleapsed time 
start_time = time.time()

parser = argparse.ArgumentParser(description='Get GitHub accounts\' audience.')

parser.add_argument('-a','--accounts',
                     help='The targeted github accounts separated by comma.')

parser.add_argument('-o','--output', 
                     help='The output file to write data, ex: -a jplusplus,pbellon', 
                     default='githuber_stats.json')

parser.add_argument('-v','--verbose',
                     help='Show some information during process', 
                     action='store_true')

parsed  = parser.parse_args(sys.argv[1:])
verbose = parsed.verbose
names   = parsed.accounts.split(',')
login    = raw_input("Please enter your GitHub's login:")
password = getpass.getpass("Please enter your GitHub's password:")

"""
will generate an array like that:
[
    {
        user: <Github user> 
        repos_counts: <total number of repositories>
        stars_audience: <audience of unique stargazers> 
        watchers_audience: <audience of unique stargazers>
        forks_audience: <audience of unique fork owners>
        total_audience: <audience of unique users reached the >
        forks_count: <cumulated number of forks (will not be equal to forks_audience)
        size_cumulated: <the cumulated size of the user's repositories> 
    },
    ..
]
""" 
stats = []
for name in names:
    user_api = GitHuberStats(user_name=name, verbose=parsed.verbose, api_password=password, api_login=login)
    user_stats = user_api.getStats()
    stats.append(user_stats)
    if verbose:
        print user_stats

io = StringIO() 
json.dump(stats, io)
f = open(parsed.output, "w")
f.write(io.getvalue())

if verbose:
    ellapsed = time.time() - start_time
    print "Ellapsed time: %f" % (ellapsed)