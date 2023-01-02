from github import Github
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import Repository, Issue, PullRequest
from django.contrib.auth.models import User
import pytz
from pytz import timezone

"""
This ingestion code will run and ingest github data into postgres database every hour when the computer system is switched ON using crontab 
in settings.py
"""
class Command(BaseCommand):
    help = "Ingest git data into database"
    WHITE_LISTED_REPO = ["xpertconnect", "xc_analytics", "rsa_crawling", "rsa_graphdb"]

    def update_pr(self, pr_info, repo, reviewer):
        """
        This function updates the pullRequest if it exists and if update date has changed.
        """

        pr = PullRequest.objects.filter(pr_number=pr_info.number, repo=repo)
        if PullRequest.objects.filter(pr_number=pr_info.number, repo=repo).exists():
            pr = PullRequest.objects.get(pr_number=pr_info.number, repo=repo)
        if pr.updated_on != pr_info.updated_at.replace(tzinfo=pytz.utc).astimezone(
            timezone("Asia/Kolkata")
        ):
            pr.reviewer = reviewer
            pr.title = pr_info.title
            pr.status = pr_info.state
            pr.updated_on = pr_info.updated_at.replace(tzinfo=pytz.utc).astimezone(
                timezone("Asia/Kolkata")
            )
            if pr_info.closed_at == None:
                pr.closed_on = pr_info.closed_at
            else:
                pr.closed_on = pr_info.closed_at.replace(tzinfo=pytz.utc).astimezone(
                    timezone("Asia/Kolkata")
                )
            pr.save()
            print(f"Updated pr_number: {pr_info.number} for repo: {repo}")

    def update_issue(self, issue_info, repo, reviewer):
        """
        This function updates the Issue if: 1. It exists and 2. If update date has changed.
        """

        issue = Issue.objects.filter(issue_number=issue_info.number, repo=repo)
        if Issue.objects.filter(issue_number=issue_info.number, repo=repo).exists():
            issue = Issue.objects.get(issue_number=issue_info.number, repo=repo)
        update_date = issue_info.updated_at
        if issue_info.updated_at != None:
            update_date = issue_info.updated_at.replace(tzinfo=pytz.utc).astimezone(
                timezone("Asia/Kolkata")
            )
        if issue.updated_on != update_date:
            issue.assignee = reviewer
            issue.title = issue_info.title
            issue.status = issue_info.state
            issue.updated_on = issue_info.updated_at.replace(
                tzinfo=pytz.utc
            ).astimezone(timezone("Asia/Kolkata"))
            if issue.closed_on == None:
                issue.closed_on = issue_info.closed_at
            else:
                issue.closed_on = issue_info.closed_at.replace(
                    tzinfo=pytz.utc
                ).astimezone(timezone("Asia/Kolkata"))
            issue.save()
            print(f"Updated issue_number: {issue_info.number} for repo: {repo}")

    def handle(self, *args, **options):
        client = Github(settings.GITHUB_ACCESS_TOKEN)
        for current_repo in client.get_user().get_repos():
            if current_repo.name in self.WHITE_LISTED_REPO:
                print(current_repo)
                all_pr_number = []
                repo = Repository.objects.get(name=current_repo.name)
                """
                For loop for PullRequest
                """
                for current_pr in current_repo.get_pulls(state="all"):
                    print(f"pr number: {current_pr.number}")
                    if current_pr.number not in all_pr_number:
                        all_pr_number.append(current_pr.number)
                    reviewer = User.objects.get(username="nobody")
                    if len(current_pr.assignees) > 0:
                        reviewer = User.objects.get(
                            username=current_pr.assignees[0].login
                        )
                    if PullRequest.objects.filter(
                        pr_number=current_pr.number, repo=repo
                    ).exists():
                        self.update_pr(current_pr, repo, reviewer)
                    else:
                        pr = PullRequest()
                        pr.repo = repo
                        pr.reviewer = reviewer
                        pr.title = current_pr.title
                        pr.pr_number = current_pr.number
                        pr.status = current_pr.state
                        pr.created_at = current_pr.created_at.replace(
                            tzinfo=pytz.utc
                        ).astimezone(timezone("Asia/Kolkata"))
                        pr.updated_on = current_pr.updated_at.replace(
                            tzinfo=pytz.utc
                        ).astimezone(timezone("Asia/Kolkata"))
                        if current_pr.closed_at == None:
                            pr.closed_on = current_pr.closed_at
                        else:
                            pr.closed_on = current_pr.closed_at.replace(
                                tzinfo=pytz.utc
                            ).astimezone(timezone("Asia/Kolkata"))
                        pr.save()
                        print(f"Created PR {pr.pr_number} for repo {pr.repo}")

                """
                For loop for Issue
                """
                for current_issue in current_repo.get_issues(state="all"):
                    print(current_issue.number, current_issue.assignees)
                    reviewer = User.objects.get(username="nobody")
                    if len(current_issue.assignees) > 0:
                        reviewer = User.objects.get(
                            username=current_issue.assignees[0].login
                        )
                    if current_issue.number not in all_pr_number:
                        print(f"issue number: {current_issue.number}")
                        if Issue.objects.filter(
                            issue_number=current_issue.number, repo=repo
                        ).exists():
                            self.update_issue(current_issue, repo, reviewer)
                        else:
                            issue = Issue()
                            issue.repo = repo
                            issue.assignee = reviewer
                            issue.title = current_issue.title
                            issue.issue_number = current_issue.number
                            issue.status = current_issue.state
                            issue.created_at = current_issue.created_at.replace(
                                tzinfo=pytz.utc
                            ).astimezone(timezone("Asia/Kolkata"))
                            issue.updated_on = current_issue.updated_at.replace(
                                tzinfo=pytz.utc
                            ).astimezone(timezone("Asia/Kolkata"))
                            if current_issue.closed_at == None:
                                issue.closed_on = current_issue.closed_at
                            else:
                                issue.closed_on = current_issue.closed_at.replace(
                                    tzinfo=pytz.utc
                                ).astimezone(timezone("Asia/Kolkata"))
                            issue.save()
                            print(
                                f"Created Issue {issue.issue_number} for repo {issue.repo}"
                            )
