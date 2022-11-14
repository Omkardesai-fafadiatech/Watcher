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
                if repository.name != "xc_multimeter":
                    repository_name = repository.name
                    
                    repo = Repository.objects.get(name=repository_name)
                    all_issues = repository.get_issues(state="all")
                    itr = 0
                    for issue in all_issues:
                        itr+=1

                        if len(issue.assignees) > 0:
                            for single_assignee in issue.assignees:
                                print(f"single assignee after handling1: {single_assignee.login}")
                                assignee = User.objects.get(username=single_assignee.login)
                                if Issue.objects.filter(title=issue.title).exists():
                                    prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=issue.title)]
                                    prev_status = [i.status for i in Issue.objects.filter(title=issue.title)]
                                    prev_closed_on = [i.closed_on for i in Issue.objects.filter(title=issue.title)]
                                    print(f"prev_updated_on: {prev_updated_on} , prev_status: {prev_status}")
                                    try:
                                        if prev_updated_on != issue.updated_at:
                                            print(f"prev_updated_on: {prev_updated_on}, updated_at: {issue.updated_at}")
                                            Issue.objects.filter(title=issue.title).update(updated_on=issue.updated_at)
                                    except:
                                        continue
                                    if prev_status != issue.state:
                                        Issue.objects.filter(title=issue.title).update(status=issue.state)
                                    if prev_closed_on != issue.closed_at:
                                        Issue.objects.filter(title=issue.title).update(closed_on=issue.closed_at)

                                elif not Issue.objects.filter(title=issue.title).exists():
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
                            print(f"no_assignee after handling: {assignee}")
                            if Issue.objects.filter(title=issue.title).exists():
                                prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=issue.title)]
                                prev_status = [i.status for i in Issue.objects.filter(title=issue.title)]
                                prev_closed_on = [i.closed_on for i in Issue.objects.filter(title=issue.title)]
                                print(f"prev_updated_on: {prev_updated_on} , prev_status: {prev_status}")
                                if prev_updated_on != issue.updated_at:
                                    print(f"prev_updated_on: {prev_updated_on}, updated_at: {issue.updated_at}")
                                    Issue.objects.filter(title=issue.title).update(updated_on=issue.updated_at)
                                if prev_status != issue.state:
                                    Issue.objects.filter(title=issue.title).update(status=issue.state)
                                if prev_closed_on != issue.closed_at:
                                    Issue.objects.filter(title=issue.title).update(closed_on=issue.closed_at)

                            elif not Issue.objects.filter(title=issue.title).exists():
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


                    pulls = repository.get_pulls(state="all")
                    itr1 =  0
                    for pr in pulls:
                        itr1+=1
                        if len(pr.assignees) > 0:
                            for single_assignee in pr.assignees:
                                print(f"single assignee after handling1: {single_assignee.login}")
                                reviewer = User.objects.get(username=single_assignee.login)
                                if PullRequest.objects.filter(title=pr.title).exists():
                                    prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=pr.title)]
                                    prev_status = [i.status for i in Issue.objects.filter(title=pr.title)]
                                    prev_closed_on = [i.closed_on for i in Issue.objects.filter(title=pr.title)]
                                    if prev_updated_on != pr.updated_at:
                                        print(f"prev_updated_on: {prev_updated_on}, updated_at: {issue.updated_at}")
                                        Issue.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                                    if prev_status != pr.state:
                                        Issue.objects.filter(title=pr.title).update(status=pr.state)
                                    if prev_closed_on != pr.closed_at:
                                        Issue.objects.filter(title=pr.title).update(closed_on=pr.closed_at)
                                elif not PullRequest.objects.filter(title=pr.title).exists():
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
                                prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=pr.title)]
                                prev_status = [i.status for i in Issue.objects.filter(title=pr.title)]
                                prev_closed_on = [i.closed_on for i in Issue.objects.filter(title=pr.title)]
                                if prev_updated_on != pr.updated_at:
                                    print(f"prev_updated_on: {prev_updated_on}, updated_at: {issue.updated_at}")
                                    Issue.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                                if prev_status != pr.state:
                                    Issue.objects.filter(title=pr.title).update(status=pr.state)
                                if prev_closed_on != pr.closed_at:
                                    Issue.objects.filter(title=pr.title).update(closed_on=pr.closed_at)
                            elif not PullRequest.objects.filter(title=pr.title).exists():
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


                    
                    
                        