from   sets import Set 
import re
import requests

class GitHuberStats:
    def __init__(self,user_name=None, verbose=False,api_login=None, api_password=None):

        if api_password == None or api_login == None:
            raise Exception('Please set your GitHub\'s login & password')
        
        self.api_login = api_login
        self.api_password = api_password
        self.user_name = user_name
        self.GITHUB_API_NS = 'api.github.com/users/'
        self.watchers_count   = 0
        self.stars_count      = 0
        self.forks_count      = 0
        self.size_cumulated   = 0
        # Global audience, like every audience we want to get unique user so we
        # need a Set to avoid doublons. 
        self.audience         = Set()
        # Stargazers audience
        self.all_stargazers   = Set()
        # Watchers audience 
        self.all_watchers     = Set()
        # Forks audience 
        self.all_forks_owners = Set()
        self.verbose = verbose

    def getJSON(self,url):
        """
        Will request the API endpoint (parameter `url`) and return the JSON 
        result
        """
        if self.verbose:
            print "Going to request %s ressource" % url

        result = requests.get(url,  headers=self.getJSONHeaders(), auth=self.auth())
        if self.verbose:
            print "Result: %s" % result

        return result.json()

    def getAPIUrl(self):
        return 'https://' + self.GITHUB_API_NS + self.user_name

    def getJSONHeaders(self):
        return { "Accept": "application/json", "Accept-Charset": "utf-8" }

    def auth(self):
        return (self.api_login, self.api_password)

    def getIDS(self, url, id_selector=lambda user: user['id'], ids=None, page=0):
        """
        Navigate trough a paginated REST ressource and return IDs 
        """
        if ids == None:
            ids = Set()
        # Build the paginated url (e.g <ressource URI>?page=10)
        paged_url = "%s?page=%i" % (url, page)
        r = self.getJSON(paged_url)
        if len(r) == 0 or r == None:
            return ids
        else:
            for user in r:
                user_id = id_selector(user)
                ids.add(user_id)
            return self.getIDS(url, id_selector, ids, page+1)

    def get_repo_watchers(self,repo):
        """
        Returns all repository watchers' IDS
        """
        watchers_url = "%s/subscribers" % repo['url']
        return self.getIDS(watchers_url)

    def get_repo_stargazers(self,repo):
        stargazers_url = "%s/stargazers" % repo['url']
        return self.getIDS(stargazers_url)

    def get_repo_forks_owners(self,repo):
        forks_url = "%s/forks" % repo['url']
        selector  = lambda fork: fork['owner']['id']
        return self.getIDS(forks_url, selector)

    def getStats(self):
        """
        Return all user stats, will launch navigation in GitHub's API
        """
        user_url   = self.getAPIUrl()
        repos_url  = "%s/repos" % user_url
        user_json  = self.getJSON(user_url)
        repos_json = self.getJSON(repos_url)
        
        # we navigate through every user's repositories to retrieve their stats
        for repo in repos_json:
            repo_stargazers   = self.get_repo_stargazers(repo)
            repo_watchers     = self.get_repo_watchers(repo)
            repo_forks_owners = self.get_repo_forks_owners(repo)
            if self.verbose:
                infos = (
                    repo['name'], 
                    len(repo_stargazers), 
                    len(repo_watchers), 
                    len(repo_forks_owners)
                ) 
                print "\n\n\t%s repository has\n\t- %d stargazers,\n\t- %d watchers,\n\t- and %d forks\n\n" % infos

            self.all_stargazers   |= Set(repo_stargazers)
            self.all_watchers     |= Set(repo_watchers)
            self.all_forks_owners |= Set(repo_forks_owners)

            self.size_cumulated += repo['size']
            self.forks_count    += repo['forks']

        self.audience |= self.all_stargazers | self.all_watchers | self.all_forks_owners

        stats = {
            "user": user_json['name'],
            "repos_count": user_json['public_repos'],
            "stars_audience":    len(self.all_stargazers),
            "watchers_audience": len(self.all_watchers),
            "forks_audience":    len(self.all_forks_owners),
            "total_audience":    len(self.audience),
            "forks_count":      self.forks_count,
            "size_cumulated":   self.size_cumulated,
        }
        return stats