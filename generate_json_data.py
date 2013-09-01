from lib.githuber_stats import GitHuberStats
import argparse

import sys 
import os
import json 
import time

# Eleapsed time 
start_time = time.time()


def generate_stats(links, password, login, verbose):
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
    for link in links:
        user_api = GitHuberStats(user_link=link, verbose=verbose, api_password=password, api_login=login)
        user_stats = user_api.getStats()
        stats.append(user_stats)
        if verbose:
            print user_stats
    return stats

def write_as_json(data, filename):
    from StringIO import StringIO
    io = StringIO() 
    json.dump(data, io)
    f = open(filename, "w")
    f.write(io.getvalue())



parser = argparse.ArgumentParser(description='Get GitHub accounts\' audience.')

parser.add_argument('-a','--accounts',
                     help='The targeted github accounts separated by comma.')

parser.add_argument('-l','--login', 
                     help='Your GitHub login', 
                     type=str)

parser.add_argument('-p','--password', 
                     help='Your GitHub password', 
                     type=str)

parser.add_argument('-o','--output', 
                     help='The output file to write data', 
                     default='githuber_stats.json')

parser.add_argument('-v','--verbose',
                     help='Show some information during process', 
                     action='store_true')

parsed  = parser.parse_args(sys.argv[1:])

verbose = parsed.verbose
links   = parsed.accounts.split(',')
stats   = generate_stats(
            links=links, 
            password=parsed.password, 
            login=parsed.login,
            verbose=parsed.verbose
            )
write_as_json(stats, parsed.output)

if verbose:
    ellapsed = time.time() - start_time
    print "Ellapsed time: %f" % (ellapsed)