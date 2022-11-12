'''
    This code is to ingest all the github data at once after deleting all rows from postgresql 
    table "core_issue".

    Run this sql query to delete all the rows from postgresql table "core_issue"
    1. sudo su postgres
    2. psql
    3. "delete from core_issue"
    4. Then run this command on terminal: "python manage.py ingestion_full_data.py"
        to ingest all data into postgres again.
'''

from github import Github
from django.core.management.base import BaseCommand
from core.models import Project, Repository, Issue, PullRequest
from core.serializers import ProjectSerializer, RepositorySerializer, IssueSerializer, PullRequestSerializer
from pathlib import Path
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Ingest git_data into Postgres database"

    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).parent.resolve()

        access_token = "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"

        login = Github(access_token)
        user = login.get_user()
        my_repos = user.get_repos()

        for repository in my_repos:
            private = repository.private

            if private:
                if repository.name == "xpertconnect":
                    repository_name = repository.name
                    
                    repo = Repository.objects.get(name=repository_name)
                    all_issues = repository.get_issues(state="all")
                    # itr = 0
                    # for issue in all_issues:
                    #     itr+=1
                    #     if len(issue.assignees) > 0:
                    #         for single_assignee in issue.assignees:
                    #             print(f"single assignee after handling1: {single_assignee.login}")
                    #             assignee = User.objects.get(username=single_assignee.login)
                    #             if Issue.objects.filter(title=issue.title).exists():
                    #                 continue
                                
                    #             print(f"title: {issue.title}")
                    #             issue = Issue(
                    #                 assignee = assignee,
                    #                 title = issue.title,
                    #                 issue_number = issue.number,
                    #                 status = issue.state,
                    #                 repo = repo,
                    #                 created_at = issue.created_at,
                    #                 updated_on = issue.updated_at,
                    #                 closed_on = issue.closed_at
                    #             )
                    #             issue.save()

                                
                    #     elif len(issue.assignees) == 0:
                    #         assignee = User.objects.get(username="nobody")
                    #         if Issue.objects.filter(title=issue.title).exists():
                    #             continue

                    #         print(f"title: {issue.title}")
                    #         issue = Issue(
                    #             assignee = assignee,
                    #             title = issue.title,
                    #             issue_number = issue.number,
                    #             status = issue.state,
                    #             repo = repo,
                    #             created_at = issue.created_at,
                    #             updated_on = issue.updated_at,
                    #             closed_on = issue.closed_at
                    #         )
                    #         issue.save()
                    #     print(f"itr number outside loop: {itr}")
                    # print(f"Ingested issues")
                    
                    print(f"Ingesting pull request info from repo {repository.name}")
                    
                    pulls = repository.get_pulls(state="all")
                    itr1 =  0
                    for pr in pulls:
                        itr1+=1
                        if len(pr.assignees) > 0:
                            for single_assignee in pr.assignees:
                                print(f"single assignee after handling1: {single_assignee.login}")
                                reviewer = User.objects.get(username=single_assignee.login)
                                if PullRequest.objects.filter(title=pr.title).exists():
                                    continue
                                
                                print(f"title: {pr.title}")
                                pullrequest = PullRequest(
                                    reviewer = reviewer,
                                    title = pr.title,
                                    pr_number = pr.number,
                                    status = pr.state,
                                    repo = repo,
                                    created_at = pr.created_at,
                                    updated_on = pr.updated_at,
                                    closed_on = pr.closed_at
                                )
                                pullrequest.save()
                        
                        elif len(pr.assignees) == 0:
                            reviewer = User.objects.get(username="nobody")
                            if PullRequest.objects.filter(title=pr.title).exists():
                                continue

                            print(f"title: {pr.title}")
                            pullrequest = PullRequest(
                                reviewer = reviewer,
                                title = pr.title,
                                pr_number = pr.number,
                                status = pr.state,
                                repo = repo,
                                created_at = pr.created_at,
                                updated_on = pr.updated_at,
                                closed_on = pr.closed_at
                            )
                            pullrequest.save()
                        print(f"itr1 number outside loop: {itr1}")
                    print(f"Ingested pull request")