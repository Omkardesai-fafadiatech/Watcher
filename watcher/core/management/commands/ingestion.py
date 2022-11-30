from github import Github
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import Repository, Issue, PullRequest
from django.contrib.auth.models import User

from core.utils import (
    title_spliter,
    get_pr_model_unique_title,
    get_issue_model_unique_title,
)


class Command(BaseCommand):
    help = "Ingest git data into database"
    WHITE_LISTED_REPO = [
        "xpertconnect",
        "xc_analytics",
        "rsa_crawling",
        "rsa_graphdb",
    ]

    def update_pr(self, pr_info, repo, reviewer):
        # TODO: for love of GOD please cleanup DB and change me to
        # pr = PullRequest.objects.get(pr_number=pr_info.number)
        pr = PullRequest.objects.filter(pr_number=pr_info.number).first()
        if pr.updated_on != pr_info.updated_at:
            pr.reviewer = reviewer
            pr.title = pr_info.title
            pr.status = pr_info.state
            pr.updated_on = pr_info.updated_at
            pr.closed_on = pr_info.closed_at
            pr.save()
            print(f"Updated {pr_info.number} for {repo}")

    def update_issue(self, issue_info):
        pass

    def handle(self, *args, **options):
        client = Github(settings.GITHUB_ACCESS_TOKEN)
        for current_repo in client.get_user().get_repos():
            if current_repo.name in self.WHITE_LISTED_REPO:
                print(current_repo)
                for current_pr in current_repo.get_pulls(state="all"):
                    repo = Repository.objects.get(name=current_repo.name)
                    reviewer = User.objects.get(username="nobody")
                    if len(current_pr.assignees) > 0:
                        reviewer = User.objects.get(
                            username=current_pr.assignees[0].login
                        )
                    if PullRequest.objects.filter(pr_number=current_pr.number).exists():
                        self.update_pr(current_pr, repo, reviewer)
                    else:
                        pr = PullRequest()
                        pr.repo = repo
                        pr.reviewer = reviewer
                        pr.title = current_pr.title
                        pr.pr_number = current_pr.number
                        pr.status = current_pr.state
                        pr.created_at = current_pr.created_at
                        pr.updated_on = current_pr.updated_at
                        pr.closed_on = current_pr.closed_at
                        pr.save()
                        print(f"Created PR {pr.pr_number} for {pr.repo}")
