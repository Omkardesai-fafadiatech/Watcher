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

        access_token = "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"

        login = Github(access_token)
        print(dir(login))
        user = login.get_user()
            
        my_repos = user.get_repos()

        for repository in my_repos:
            # print(repository)
            private = repository.private