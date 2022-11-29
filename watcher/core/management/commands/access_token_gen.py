from github import Github
from django.core.management.base import BaseCommand
from core.models import Project, Repository, Issue, PullRequest
from core.serializers import ProjectSerializer, RepositorySerializer, IssueSerializer, PullRequestSerializer
from pathlib import Path
from django.contrib.auth.models import User
import requests
import json

class Command(BaseCommand):
    help = "Ingest git_data into Postgres database"

    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).parent.resolve()

        # access_token = "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"

        # login = Github(access_token)
        # print(dir(login))
        # user = login.get_user()
            
        # my_repos = user.get_repos()

        # for repository in my_repos:
        #     # print(repository)
        #     private = repository.private

        password = "Omkardesai*123698741#"

        
        login = Github("Omkardesai-fafadiatech", "Omkardesai*123698741#", per_page=100)  # Maximum per page seems to be 100

        repos = login.get_repos()

        list_of_repos = []

        # Repos object is a paginated list, it will automatically issue another request to GitHub when the end of the list
        # is reached. We have to pay attention to not exceed the rate limit. We use pickle to serialize the list (to a binary
        # file format)
        for repo in repos:
            if repo.private == True:
                print(repo.name)
                print(f"rate limit: {login.rate_limiting}")
                # rate_limit_remaining = login.rate_limiting[0]
                # print(rate_limit_remaining)
                # repo_dict = {
                #     'url': repo.url,
                #     'id': repo.id,
                #     'subscribers': repo.subscribers_count,
                #     'forks': repo.forks_count
                # }
                # list_of_repos.append(repo_dict)