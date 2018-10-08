import requests
import datetime
import json

class GitNavi():
    """
    This is a class for getting and processing repository and commits data from github API.

    Attributes:
          no_repos (int): The number of repositories to be rendered.
          headers (dict): The header to be passed to github API.
    """
    def __init__(self, no_repos):
        """
        The constructor for GitNavi class.

        Parameters:
            no_repos (int): The number of repositories to be rendered.
        """
        self.no_repos = no_repos
        self.headers = {}
        self.headers['User-Agent'] = 'GitHub navigator'

    def get_repos_req(self, search_term, order_by):
        """
        The function to query repositories via github API with the input search_term and return the ordered response.

        Parameters:
            search_term (string): The search_term to query github API.
            order_by    (string): The param with which response from github API needs to be sorted.

        Returns:
            repos_dict    (list): List of sorted json objects returned from github API in dict format.
        """
        repos_url = 'https://api.github.com/search/repositories'
        repos_res = requests.get(repos_url, headers= self.headers, params= {'q':search_term})
        repos_list = sorted(repos_res.json()['items'], key=lambda x: x[order_by], reverse=True)
        return repos_list

    def get_commit_req(self, commits_url):
        """
        The function to query commits for a repository via github API with the input commits_url.

        Parameters:
            commits_url (string): The url to query commits on a repository.

        Returns:
            commit_res    (list): List of json objects in returned from github API dict format.
        """
        commits_url = commits_url[:commits_url.find('{')]
        commit_res = requests.get(commits_url, headers= self.headers)
        return commit_res.json()

    def search_git_repos(self, search_term):
        """
        The function to call get_repos_req and get_commit_req to get 'no_repos' number of newest repositories and some
        information about the latest commits on those repositories.

        Parameters:
            search_term (string): The search_term to query github API.

        Returns:
            render_list   (list): The list with latest repositories fetched from the API with some information.
        """
        repos_list = self.get_repos_req(search_term, 'created_at')
        render_list = []

        for index in range(self.no_repos):
            render_dict = {}
            render_dict['index'] = index+1
            render_dict['repository_name'] = repos_list[index]['name']
            render_dict['created_at'] = datetime.datetime.strptime(repos_list[index]['created_at'],'%Y-%m-%dT%H:%M:%SZ')
            render_dict['owner_login'] =  repos_list[index]['owner']['login']
            render_dict['avatar_url'] = repos_list[index]['owner']['avatar_url']
            commit_dict = self.get_commit_req(repos_list[index]['commits_url'])
            render_dict['sha'] = commit_dict[0]['sha']
            render_dict['commit_message'] = commit_dict[0]['commit']['message']
            render_dict['commit_author_name'] = commit_dict[0]['commit']['author']['name']
            render_list.append(render_dict)
        return  render_list
