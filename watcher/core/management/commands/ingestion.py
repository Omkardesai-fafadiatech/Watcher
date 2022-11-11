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
                    project_name = "Xpertconnect"
                    
                    repo = Repository.objects.get(name=repository_name)
                    all_issues = repository.get_issues(state="all")
                    itr = 0
                    for issue in all_issues:
                        itr+=1
                        if len(issue.assignees) > 1 or len(issue.assignees) == 1:
                            for single_assignee in issue.assignees:
                                print(f"single assignee after handling1: {single_assignee.login}")
                                assignee = User.objects.get(username=single_assignee.login)
                                if Issue.objects.filter(title=issue.title).exists():
                                    continue

                                issue = Issue(
                                    assignee = assignee,
                                    title = issue.title,
                                    issue_number = issue.number,
                                    status = issue.state,
                                    repo = repo,
                                    created_at = issue.created_at,
                                    updated_on = issue.updated_at,
                                    closed_on = issue.closed_at
                                )
                                issue.save()

                                
                        elif len(issue.assignees) == 0:
                            assignee = User.objects.get(username="nobody")
                            if Issue.objects.filter(title=issue.title).exists():
                                continue
                            issue = Issue(
                                assignee = assignee,
                                title = issue.title,
                                issue_number = issue.number,
                                status = issue.state,
                                repo = repo,
                                created_at = issue.created_at,
                                updated_on = issue.updated_at,
                                closed_on = issue.closed_at
                            )
                            issue.save()
                        print(f"itr number outside loop: {itr}")

                        # if len(issue.assignees) > 1 or len(issue.assignees) == 1:
                        #     for single_assignee in issue.assignees:
                        #         print(f"single assignee after handling1: {single_assignee.login}")
                        #         assignee = User.objects.get(username=single_assignee.login)
                        #         if Issue.objects.filter(title=issue.title).exists():
                        #             prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=issue.title)]
                        #             prev_status = [i.status for i in Issue.objects.filter(title=issue.state)]
                        #             if prev_updated_on != issue.updated_at or prev_status != issue.state:
                        #                 for i in Issue.objects.filter(title=issue.state):
                        #                     issue = Issue(
                        #                         status = i.status,
                        #                         updated_on = i.updated_on,
                        #                     )
                        #                     issue.save()

                        #         elif not Issue.objects.filter(title=issue.title).exists():
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

                        #         else :
                        #             continue
                                
                        # elif len(issue.assignees) == 0:
                        #     assignee = User.objects.get(username="nobody")
                        #     if Issue.objects.filter(title=issue.title).exists():
                        #             prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=issue.title)]
                        #             prev_status = [i.status for i in Issue.objects.filter(title=issue.state)]
                        #             if prev_updated_on != issue.updated_at or prev_status != issue.state:
                        #                 for i in Issue.objects.filter(title=issue.state):
                        #                     issue = Issue(
                        #                         status = i.status,
                        #                         updated_on = i.updated_on,
                        #                     )
                        #                     issue.save()
                        #     elif not Issue.objects.filter(title=issue.title).exists():
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
                            
                            # else:
                            #     continue

                        # print(f"itr number outside loop: {itr}")


                    # print(f"Ingesting pull request info from repo {repository.name}")
                    # pulls = repository.get_pulls(state="all")
                    # for pr in pulls:
                    #     for info in pr.assignees:
                    #         if not User.objects.filter(username=info.login).exists():
                    #             User.objects.create(username=info.login)
                    #             User.save()
                    #             reviewer = User.objects.get(username=info.login)
                    #         elif User.objects.filter(username=info.login).exists():
                    #             reviewer = User.objects.get(username=info.login)

                    #         if not Repository.objects.filter(name=repository.name).exists():
                    #             Repository.objects.create(name=repository.name)
                    #             Repository.save()
                    #             repo = Repository.objects.get(name=repository.name),
                    #         elif Repository.objects.filter(name=repository.name).exists():
                    #             repo = Repository.objects.get(name=repository.name),
                    #         PullRequest.objects.create(
                    #             reviewer = reviewer,
                    #             title = pr.title,
                    #             pr_number = pr.number,
                    #             status = pr.state,
                    #             repo = repo,
                    #             created_at = pr.created_at,
                    #             closed_on = pr.closed_at
                    #         )
                    #         PullRequest.save()
                    # print(f"Ingested pull request")


                    
                    
                        