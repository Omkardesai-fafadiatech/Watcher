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
        """
        This Github token is from Keith Github account.
        Since My(Omkar Github access tokens get deleted everyday)
        """
        access_token = "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"

        login = Github(access_token)

        for repository in login.get_user().get_repos():
            private = repository.private

            if private:
                if repository.name in ["xpertconnect", "xc_analytics", "rsa_crawling", "rsa_graphdb"]:
                    repository_name = repository.name
                    
                    repo = Repository.objects.get(name=repository_name)
                    itr1 =  0
                    for pr in repository.get_pulls(state="all"):
                        itr1+=1
                        if len(pr.assignees) > 0:
                            print(f"pr assignee name: {pr.assignees[0].login}")
                            reviewer = User.objects.get(username=pr.assignees[0].login)
                            if PullRequest.objects.filter(title=pr.title).exists():
                                prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=pr.title)]
                                prev_status = [i.status for i in Issue.objects.filter(title=pr.title)]
                                prev_closed_on = [i.closed_on for i in Issue.objects.filter(title=pr.title)]
                                if prev_updated_on != pr.updated_at:
                                    try:
                                        print(f"prev_updated_on: {prev_updated_on}, updated_at: {pr.updated_at}")
                                        # Issue.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                                    except:
                                        continue
                                if prev_status != pr.state or prev_closed_on != pr.closed_at:
                                    print(f"prev_status: {prev_status}, updated_status: {pr.state}")
                                    Issue.objects.filter(title=pr.title).update(status=pr.state)
                                    print(f"prev_closed_on: {prev_closed_on}, updated_closed_at: {pr.closed_at}")
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
                                    try:
                                        print(f"prev_updated_on: {prev_updated_on}, updated_at: {pr.updated_at}")
                                        # Issue.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                                    except:
                                        continue
                                if prev_status != pr.state or prev_closed_on != pr.closed_at:
                                    print(f"prev_status: {prev_status}, updated_status: {pr.state}")
                                    Issue.objects.filter(title=pr.title).update(status=pr.state)
                                    print(f"prev_closed_on: {prev_closed_on}, updated_closed_at: {pr.closed_at}")
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

                    itr = 0
                    for issue in repository.get_issues(state="all"):
                        itr+=1
                        if not PullRequest.objects.filter(pr_number=issue.number).exists():
                            if len(issue.assignees) > 0:
                                print(f"pr assignee name: {issue.assignees[0].login}")
                                assignee = User.objects.get(username=issue.assignees[0].login)
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
                                    if prev_status != issue.state or prev_closed_on != issue.closed_at:
                                        Issue.objects.filter(title=issue.title).update(status=issue.state)
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
                                    if prev_updated_on != issue.updated_at:
                                        print(f"prev_updated_on: {prev_updated_on}, updated_at: {issue.updated_at}")
                                        Issue.objects.filter(title=issue.title).update(updated_on=issue.updated_at)
                                    if prev_status != issue.state or prev_closed_on != issue.closed_at:
                                        Issue.objects.filter(title=issue.title).update(status=issue.state)
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
                        else:
                            continue
                        print(f"itr number outside loop: {itr}")