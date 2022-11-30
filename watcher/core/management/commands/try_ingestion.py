from github import Github
from django.core.management.base import BaseCommand
from core.models import Project, Repository, Issue, PullRequest
from core.serializers import (
    ProjectSerializer,
    RepositorySerializer,
    IssueSerializer,
    PullRequestSerializer,
)
from pathlib import Path
from django.contrib.auth.models import User
from collections import defaultdict
import pytz
from pytz import timezone

from core.utils import (
    title_context_cleaner,
    title_label_cleaner,
    title_spliter,
    get_pr_model_unique_title,
    get_issue_model_unique_title,
)


class Command(BaseCommand):
    help = "Ingest git_data into Postgres database"

    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).parent.resolve()
        """
        This Github token is from Keith Github account.
        Since My(Omkar Github access tokens get deleted everyday)
        """
        # itr2 = 0
        # for pr_title in PullRequest.objects.all():
        #     # print(type(str(pr_title.repo)))
        #     if str(pr_title.repo) == "xpertconnect":
        #         print(pr_title.repo)
        #         itr2+=1
        # print(itr2)

        # model_dict = get_pr_model_unique_title()
        # print(model_dict)

        access_token = "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"

        login = Github(access_token)
        itr1 = 0
        itr = 0
        for repository in login.get_user().get_repos():
            private = repository.private

            if private:
                if repository.name in [
                    "xpertconnect"
                ]:  # , "xc_analytics", "rsa_crawling", "rsa_graphdb"]:
                    repository_name = repository.name
                    all_pr_number = []
                    repo = Repository.objects.get(name=repository_name)
                    for pr in repository.get_pulls(state="all"):
                        print(pr.title)
                        print(
                            pr.created_at.replace(tzinfo=pytz.utc).astimezone(
                                timezone("Asia/Kolkata")
                            )
                        )
                        # prev_updated_on = PullRequest.objects.filter(title=pr.title).values()[0]['updated_on']
                        # print(f"prev_updated_on: {prev_updated_on}")
                        # prev_status = PullRequest.objects.filter(title=pr.title).values()[0]['status']
                        # print(f"prev_status: {prev_status}")
                        # prev_closed_on = PullRequest.objects.filter(title=pr.title).values()[0]['closed_on']
                        # print(f"prev_closed_on: {prev_closed_on}")
                        # prev_created_at = PullRequest.objects.filter(title=pr.title).values()[0]['created_at'].replace(tzinfo=None)
                        # print(f"prev_created_at: {prev_created_at}")
                        # prev_pr_number = PullRequest.objects.filter(title=pr.title).values()[0]['pr_number']
                        # print(f"prev_pr_number: {prev_pr_number}")
                        if pr.number not in all_pr_number:
                            all_pr_number.append(pr.number)
                        git_pr_label, get_pr_title_context = title_spliter(pr)

                        model_dict = ""
                        model_dict = get_pr_model_unique_title()
                        #     # print(len(model_dict))
                        #     # for k, v in model_dict:
                        #     #     if v>1:
                        #     #         print(f"{k}: {v}")
                        #     # print(all_pr_number)
                        if len(pr.assignees) > 0:
                            reviewer = User.objects.get(username=pr.assignees[0].login)
                        elif len(pr.assignees) == 0:
                            reviewer = User.objects.get(username="nobody")

                        if model_dict.get(get_pr_title_context) != None:
                            print(
                                f"pr.created_at: {pr.created_at} and model_date; {model_dict[get_pr_title_context].replace(tzinfo=None)}"
                            )
                            # print(model_dict.get(get_pr_title_context))

                            # if len(pr.assignees) > 0:
                            #     reviewer = User.objects.get(username=pr.assignees[0].login)

                            itr1 += 1
                            print(f"pullrequest count: {itr1}")

                            if pr.created_at > model_dict[get_pr_title_context].replace(
                                tzinfo=None
                            ):
                                print("this pr is not merged")
                                PullRequest.objects.filter(title=pr.title).update(
                                    updated_on=pr.updated_at.replace(
                                        tzinfo=pytz.utc
                                    ).astimezone(timezone("Asia/Kolkata"))
                                )
                                print(f"updated_at: {pr.updated_at}")
                                PullRequest.objects.filter(title=pr.title).update(
                                    status=pr.state
                                )
                                print(f" updated_status: {pr.state}")
                                PullRequest.objects.filter(title=pr.title).update(
                                    closed_on=pr.closed_at.replace(
                                        tzinfo=pytz.utc
                                    ).astimezone(timezone("Asia/Kolkata"))
                                )
                                print(f"updated_closed_at: {pr.closed_at}")
                                PullRequest.objects.filter(title=pr.title).update(
                                    reviewer=reviewer
                                )
                                PullRequest.objects.filter(title=pr.title).update(
                                    pr_number=pr.number
                                )
                                PullRequest.objects.filter(title=pr.title).update(
                                    created_at=pr.created_at.replace(
                                        tzinfo=pytz.utc
                                    ).astimezone(timezone("Asia/Kolkata"))
                                )
                                PullRequest.objects.filter(title=pr.title).update(
                                    title=pr.title
                                )
                                PullRequest.objects.filter(title=pr.title).update(
                                    repo=repo
                                )

                            elif pr.created_at == model_dict[
                                get_pr_title_context
                            ].replace(tzinfo=None):

                                prev_updated_on1 = (
                                    PullRequest.objects.filter(title=pr.title)
                                    .values()[0]["updated_on"]
                                    .replace(tzinfo=None)
                                )
                                print(f"prev_updated_on1: {prev_updated_on1}")
                                # prev_status1 = PullRequest.objects.filter(title=pr.title).values()[0]['status']
                                # print(f"prev_status1: {prev_status1}")
                                # prev_closed_on1 = PullRequest.objects.filter(title=pr.title).values()[0]['closed_on'].replace(tzinfo=None)
                                # print(f"prev_closed_on1: {prev_closed_on1}")
                                # prev_created_at1 = PullRequest.objects.filter(title=pr.title).values()[0]['created_at'].replace(tzinfo=None)
                                # print(f"prev_created_at1: {prev_created_at1}")
                                # prev_pr_number1 = PullRequest.objects.filter(title=pr.title).values()[0]['pr_number']
                                # print(f"prev_pr_number1: {prev_pr_number1}")
                                prev_updated_on = [
                                    i.updated_on
                                    for i in PullRequest.objects.filter(title=pr.title)
                                ]
                                print(f"prev_updated_on: {prev_updated_on}")
                                prev_status = [
                                    i.status
                                    for i in PullRequest.objects.filter(title=pr.title)
                                ]
                                print(f"prev_status: {prev_status}")
                                prev_closed_on = [
                                    i.closed_on
                                    for i in PullRequest.objects.filter(title=pr.title)
                                ]
                                print(f"prev_closed_on: {prev_closed_on}")
                                prev_created_at_0 = PullRequest.objects.filter(
                                    title=pr.title
                                ).values()
                                prev_created_at = prev_created_at_0[0][
                                    "created_at"
                                ].replace(tzinfo=None)
                                print(f"prev_created_at: {prev_created_at}")
                                prev_pr_number = [
                                    i.pr_number
                                    for i in PullRequest.objects.filter(title=pr.title)
                                ]
                                print(f"prev_pr_number: {prev_pr_number}")
                                if len(prev_updated_on) != 0:
                                    if pr.updated_at != prev_updated_on[0].replace(
                                        tzinfo=None
                                    ):
                                        print(
                                            f"prev_updated_on: {prev_updated_on[0].replace(tzinfo=None)}, updated_at: {pr.updated_at}"
                                        )
                                        PullRequest.objects.filter(
                                            title=pr.title
                                        ).update(updated_on=pr.updated_at)
                                elif len(prev_updated_on) == 0:
                                    if pr.updated_at != "":
                                        PullRequest.objects.filter(
                                            title=pr.title
                                        ).update(updated_on=pr.updated_at)
                                if len(prev_closed_on) != 0:
                                    if pr.closed_at != prev_closed_on[0].replace(
                                        tzinfo=None
                                    ):
                                        print(
                                            f"prev_closed_on: {prev_closed_on[0].replace(tzinfo=None)}, updated_closed_at: {pr.closed_at}"
                                        )
                                        PullRequest.objects.filter(
                                            title=pr.title
                                        ).update(closed_on=pr.closed_at)
                                elif len(prev_closed_on) == 0:
                                    if pr.closed_at != "":
                                        PullRequest.objects.filter(
                                            title=pr.title
                                        ).update(closed_on=pr.closed_at)
                                if len(prev_status) != 0:
                                    if prev_status[0] != pr.state:
                                        print(
                                            f"prev_status: {prev_status[0]}, updated_status: {pr.state}"
                                        )
                                        PullRequest.objects.filter(
                                            title=pr.title
                                        ).update(status=pr.state)
                                elif len(prev_status) == 0:
                                    if pr.state != "":
                                        print(
                                            f"prev_status: {prev_status}, updated_status: {pr.state}"
                                        )
                                        PullRequest.objects.filter(
                                            title=pr.title
                                        ).update(status=pr.state)
                                PullRequest.objects.filter(title=pr.title).update(
                                    reviewer=reviewer
                                )
                                PullRequest.objects.filter(title=pr.title).update(
                                    pr_number=pr.number
                                )
                                PullRequest.objects.filter(title=pr.title).update(
                                    created_at=pr.created_at
                                )
                                PullRequest.objects.filter(title=pr.title).update(
                                    title=pr.title
                                )
                                PullRequest.objects.filter(title=pr.title).update(
                                    repo=repo
                                )
                            else:
                                continue

                        # elif model_dict.get(get_pr_title_context) == None:
                        #     print(f"new pr: {pr.title}")
                        #     itr1+=1
                        #     print(f"pullrequest count: {itr1}")
                        #     pullrequest = PullRequest(
                        #         reviewer = reviewer,
                        #         title = pr.title,
                        #         pr_number = pr.number,
                        #         status = pr.state,
                        #         repo = repo,
                        #         created_at = pr.created_at,
                        #         updated_on = pr.updated_at,
                        #         closed_on = pr.closed_at
                        #     )
                        #     pullrequest.save()
                        # else:
                        #     continue
                        # print(f"itr1 number outside loop: {itr1}")
                        # break
                    print(f"Ingested pull request")
                    # print(all_pr_number)
                    print(len(all_pr_number))

                    # for issue in repository.get_issues(state="all"):
                    #     # if not PullRequest.objects.filter(pr_number = issue.number):
                    #     # #can't use this because in models we have updated or merged unique pr only.
                    #     if issue.number not in all_pr_number:
                    #         print(issue.title)
                    #         git_issue_label, git_issue_title_context = title_spliter(issue)

                    #         issue_model_dict = ""
                    #         issue_model_dict = get_issue_model_unique_title()

                    #         if len(issue.assignees) > 0:
                    #             assignee = User.objects.get(username=issue.assignees[0].login)
                    #         elif len(issue.assignees) == 0:
                    #             assignee = User.objects.get(username="nobody")

                    #         if issue_model_dict.get(git_issue_title_context) != None:
                    #             print(issue_model_dict.get(git_issue_title_context))

                    #             # if len(issue.assignees) > 0:
                    #             #     assignee = User.objects.get(username=issue.assignees[0].login)

                    #             itr+=1
                    #             print(f"issue count: {itr}")
                    #             if issue.created_at > issue_model_dict[git_issue_title_context].replace(tzinfo=None):
                    #                 prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_status = [i.status for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_closed_on = [i.closed_on for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_created_at = [i.created_at for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_issue_number = [i.issue_number for i in Issue.objects.filter(title=issue.title)]
                    #                 print("this issue is not latest")
                    #                 Issue.objects.filter(title=issue.title).update(updated_on=issue.updated_at)
                    #                 print(f"prev_updated_on: {prev_updated_on}, updated_at: {issue.updated_at}")
                    #                 Issue.objects.filter(title=issue.title).update(status=issue.state)
                    #                 print(f"prev_status: {prev_status}, updated_status: {issue.state}")
                    #                 Issue.objects.filter(title=issue.title).update(closed_on=issue.closed_at)
                    #                 print(f"prev_closed_on: {prev_closed_on}, updated_closed_at: {issue.closed_at}")
                    #                 Issue.objects.filter(title=issue.title).update(assignee=assignee)
                    #                 Issue.objects.filter(title=issue.title).update(issue_number=issue.number)
                    #                 Issue.objects.filter(title=issue.title).update(created_at=issue.created_at)
                    #                 Issue.objects.filter(title=issue.title).update(title=issue.title)
                    #                 Issue.objects.filter(title=issue.title).update(repo=repo)

                    #             elif issue.created_at == issue_model_dict[git_issue_title_context].replace(tzinfo=None):
                    #                 print("this issue is not updated")
                    #                 prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_status = [i.status for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_closed_on = [i.closed_on for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_created_at_0 = Issue.objects.filter(title=issue.title).values()
                    #                 prev_created_at = prev_created_at_0[0]['created_at'].replace(tzinfo=None)
                    #                 prev_issue_number = [i.issue_number for i in Issue.objects.filter(title=issue.title)]
                    #                 if len(prev_updated_on) != 0:
                    #                     if issue.updated_at != prev_updated_on[0].replace(tzinfo=None):
                    #                         try:
                    #                             print(f"prev_updated_on: {prev_updated_on[0].replace(tzinfo=None)}, updated_at: {issue.updated_at}")
                    #                             Issue.objects.filter(title=issue.title).update(updated_on=issue.updated_at)
                    #                         except:
                    #                             continue
                    #                 elif len(prev_updated_on) == 0:
                    #                     if issue.updated_at != "":
                    #                         Issue.objects.filter(title=issue.title).update(updated_on=issue.updated_at)
                    #                 if len(prev_closed_on) != 0:
                    #                     if issue.closed_at != prev_closed_on[0].replace(tzinfo=None):
                    #                         print(f"prev_closed_on: {prev_closed_on[0].replace(tzinfo=None)}, updated_closed_at: {issue.closed_at}")
                    #                         Issue.objects.filter(title=issue.title).update(closed_on=issue.closed_at)
                    #                 elif len(prev_closed_on) == 0:
                    #                     if issue.closed_at != "":
                    #                         Issue.objects.filter(title=issue.title).update(closed_on=issue.closed_at)
                    #                 if len(prev_status) != 0:
                    #                     if prev_status[0] != issue.state:
                    #                         print(f"prev_status: {prev_status[0]}, updated_status: {issue.state}")
                    #                         Issue.objects.filter(title=issue.title).update(status=issue.state)
                    #                 elif len(prev_status) == 0:
                    #                     if issue.state != "":
                    #                         print(f"prev_status: {prev_status}, updated_status: {issue.state}")
                    #                         Issue.objects.filter(title=issue.title).update(status=issue.state)
                    #                 if len(prev_issue_number) != 0:
                    #                     if prev_issue_number[0] != issue.number:
                    #                         Issue.objects.filter(title=issue.title).update(assignee=assignee)
                    #                         Issue.objects.filter(title=issue.title).update(issue_number=issue.number)
                    #                         Issue.objects.filter(title=issue.title).update(created_at=issue.created_at)
                    #                         Issue.objects.filter(title=issue.title).update(title=issue.title)
                    #                         Issue.objects.filter(title=issue.title).update(repo=repo)
                    #             else:
                    #                 continue

                    #         elif issue_model_dict.get(git_issue_title_context) == None:
                    #             print(f"new issue: {issue.title}")
                    #             itr+=1
                    #             print(f"issue count: {itr}")
                    #             issue = Issue(
                    #                     assignee = assignee,
                    #                     title = issue.title,
                    #                     issue_number = issue.number,
                    #                     status = issue.state,
                    #                     repo = repo,
                    #                     created_at = issue.created_at,
                    #                     updated_on = issue.updated_at,
                    #                     closed_on = issue.closed_at
                    #                 )
                    #             issue.save()
                    #         else:
                    #             continue
                    #         # print(f"itr number outside loop: {itr}")
                    #         # break
                    # print(f"Ingested issue")

                    # if pr.is_merged() == True:
                    #     print("this pr is merged")
                    #     prev_updated_on = [i.updated_on for i in PullRequest.objects.filter(title=pr.title)]
                    #     prev_status = [i.status for i in PullRequest.objects.filter(title=pr.title)]
                    #     prev_closed_on = [i.closed_on for i in PullRequest.objects.filter(title=pr.title)]
                    #     prev_created_at = [i.created_at for i in PullRequest.objects.filter(title=pr.title)]
                    #     prev_pr_number = [i.pr_number for i in PullRequest.objects.filter(title=pr.title)]
                    #     if len(prev_updated_on) != 0:
                    #         if pr.updated_at != prev_updated_on[0].replace(tzinfo=None):
                    #             try:
                    #                 print(f"prev_updated_on: {prev_updated_on[0].replace(tzinfo=None)}, updated_at: {pr.updated_at}")
                    #                 PullRequest.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                    #             except:
                    #                 continue
                    #     elif len(prev_updated_on) == 0:
                    #         if pr.updated_at != "":
                    #             PullRequest.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                    #     if len(prev_closed_on) != 0:
                    #         if pr.closed_at != prev_closed_on[0].replace(tzinfo=None):
                    #             print(f"prev_closed_on: {prev_closed_on[0].replace(tzinfo=None)}, updated_closed_at: {pr.closed_at}")
                    #             PullRequest.objects.filter(title=pr.title).update(closed_on=pr.closed_at)
                    #     elif len(prev_closed_on) == 0:
                    #         if pr.closed_at != "":
                    #             PullRequest.objects.filter(title=pr.title).update(closed_on=pr.closed_at)
                    #     if len(prev_status) != 0:
                    #         if prev_status[0] != pr.state:
                    #             print(f"prev_status: {prev_status[0]}, updated_status: {pr.state}")
                    #             PullRequest.objects.filter(title=pr.title).update(status=pr.state)
                    #     elif len(prev_status) == 0:
                    #         if pr.state != "":
                    #             print(f"prev_status: {prev_status}, updated_status: {pr.state}")
                    #             PullRequest.objects.filter(title=pr.title).update(status=pr.state)
                    #     if len(prev_pr_number) != 0:
                    #         if prev_pr_number[0] != pr.number:
                    #             PullRequest.objects.filter(title=pr.title).update(reviewer=reviewer)
                    #             PullRequest.objects.filter(title=pr.title).update(pr_number=pr.number)
                    #             PullRequest.objects.filter(title=pr.title).update(created_at=pr.created_at)
                    #             PullRequest.objects.filter(title=pr.title).update(title=pr.title)
                    #             PullRequest.objects.filter(title=pr.title).update(repo=repo)

                    # '''
                    # condition for assignee with len 0
                    # '''
                    # elif len(pr.assignees) == 0:
                    #     reviewer = User.objects.get(username="nobody")

                    #     itr1+=1
                    #     print(f"pullrequest count: {itr1}")
                    #     if pr.is_merged() == True:
                    #         print("this pr is merged")
                    #         prev_updated_on = [i.updated_on for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_status = [i.status for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_closed_on = [i.closed_on for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_created_at = [i.created_at for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_pr_number = [i.pr_number for i in PullRequest.objects.filter(title=pr.title)]
                    #         if len(prev_updated_on) != 0:
                    #             if pr.updated_at != prev_updated_on[0].replace(tzinfo=None):
                    #                 try:
                    #                     print(f"prev_updated_on: {prev_updated_on[0].replace(tzinfo=None)}, updated_at: {pr.updated_at}")
                    #                     PullRequest.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                    #                 except:
                    #                     continue
                    #         elif len(prev_updated_on) == 0:
                    #             if pr.updated_at != "":
                    #                 PullRequest.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                    #         if len(prev_closed_on) != 0:
                    #             if pr.closed_at != prev_closed_on[0].replace(tzinfo=None):
                    #                 print(f"prev_closed_on: {prev_closed_on[0].replace(tzinfo=None)}, updated_closed_at: {pr.closed_at}")
                    #                 PullRequest.objects.filter(title=pr.title).update(closed_on=pr.closed_at)
                    #         elif len(prev_closed_on) == 0:
                    #             if pr.closed_at != "":
                    #                 PullRequest.objects.filter(title=pr.title).update(closed_on=pr.closed_at)
                    #         if len(prev_status) != 0:
                    #             if prev_status[0] != pr.state:
                    #                 print(f"prev_status: {prev_status[0]}, updated_status: {pr.state}")
                    #                 PullRequest.objects.filter(title=pr.title).update(status=pr.state)
                    #         elif len(prev_status) == 0:
                    #             if pr.state != "":
                    #                 print(f"prev_status: {prev_status}, updated_status: {pr.state}")
                    #                 PullRequest.objects.filter(title=pr.title).update(status=pr.state)
                    #         if len(prev_pr_number) != 0:
                    #             if prev_pr_number[0] != pr.number:
                    #                 PullRequest.objects.filter(title=pr.title).update(reviewer=reviewer)
                    #                 PullRequest.objects.filter(title=pr.title).update(pr_number=pr.number)
                    #                 PullRequest.objects.filter(title=pr.title).update(created_at=pr.created_at)
                    #                 PullRequest.objects.filter(title=pr.title).update(title=pr.title)
                    #                 PullRequest.objects.filter(title=pr.title).update(repo=repo)

                    #     elif pr.created_at > model_dict[get_pr_title_context].replace(tzinfo=None):
                    #         prev_updated_on = [i.updated_on for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_status = [i.status for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_closed_on = [i.closed_on for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_created_at = [i.created_at for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_pr_number = [i.pr_number for i in PullRequest.objects.filter(title=pr.title)]
                    #         print("this pr is not merged")
                    #         PullRequest.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                    #         print(f"prev_updated_on: {prev_updated_on}, updated_at: {pr.updated_at}")
                    #         PullRequest.objects.filter(title=pr.title).update(status=pr.state)
                    #         print(f"prev_status: {prev_status}, updated_status: {pr.state}")
                    #         PullRequest.objects.filter(title=pr.title).update(closed_on=pr.closed_at)
                    #         print(f"prev_closed_on: {prev_closed_on}, updated_closed_at: {pr.closed_at}")
                    #         PullRequest.objects.filter(title=pr.title).update(reviewer=reviewer)
                    #         PullRequest.objects.filter(title=pr.title).update(pr_number=pr.number)
                    #         PullRequest.objects.filter(title=pr.title).update(created_at=pr.created_at)
                    #         PullRequest.objects.filter(title=pr.title).update(title=pr.title)
                    #         PullRequest.objects.filter(title=pr.title).update(repo=repo)

                    #     elif pr.created_at == model_dict[get_pr_title_context].replace(tzinfo=None):
                    #         print("this pr is not merged")
                    #         prev_updated_on = [i.updated_on for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_status = [i.status for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_closed_on = [i.closed_on for i in PullRequest.objects.filter(title=pr.title)]
                    #         prev_created_at_0 = PullRequest.objects.filter(title=pr.title).values()
                    #         prev_created_at = prev_created_at_0[0]['created_at'].replace(tzinfo=None)
                    #         prev_pr_number = [i.pr_number for i in PullRequest.objects.filter(title=pr.title)]
                    #         if len(prev_updated_on) != 0:
                    #             if pr.updated_at != prev_updated_on[0].replace(tzinfo=None):
                    #                 try:
                    #                     print(f"prev_updated_on: {prev_updated_on[0].replace(tzinfo=None)}, updated_at: {pr.updated_at}")
                    #                     PullRequest.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                    #                 except:
                    #                     continue
                    #         elif len(prev_updated_on) == 0:
                    #             if pr.updated_at != "":
                    #                 PullRequest.objects.filter(title=pr.title).update(updated_on=pr.updated_at)
                    #         if len(prev_closed_on) != 0:
                    #             if pr.closed_at != prev_closed_on[0].replace(tzinfo=None):
                    #                 print(f"prev_closed_on: {prev_closed_on[0].replace(tzinfo=None)}, updated_closed_at: {pr.closed_at}")
                    #                 PullRequest.objects.filter(title=pr.title).update(closed_on=pr.closed_at)
                    #         elif len(prev_closed_on) == 0:
                    #             if pr.closed_at != "":
                    #                 PullRequest.objects.filter(title=pr.title).update(closed_on=pr.closed_at)
                    #         if len(prev_status) != 0:
                    #             if prev_status[0] != pr.state:
                    #                 print(f"prev_status: {prev_status[0]}, updated_status: {pr.state}")
                    #                 PullRequest.objects.filter(title=pr.title).update(status=pr.state)
                    #         elif len(prev_status) == 0:
                    #             if pr.state != "":
                    #                 print(f"prev_status: {prev_status}, updated_status: {pr.state}")
                    #                 PullRequest.objects.filter(title=pr.title).update(status=pr.state)
                    #         if len(prev_pr_number) != 0:
                    #             if prev_pr_number[0] != pr.number:
                    #                 PullRequest.objects.filter(title=pr.title).update(reviewer=reviewer)
                    #                 PullRequest.objects.filter(title=pr.title).update(pr_number=pr.number)
                    #                 PullRequest.objects.filter(title=pr.title).update(created_at=pr.created_at)
                    #                 PullRequest.objects.filter(title=pr.title).update(title=pr.title)
                    #                 PullRequest.objects.filter(title=pr.title).update(repo=repo)
                    #     else:
                    #         continue

                    # '''
                    # old code for issues
                    # '''
                    #     if not PullRequest.objects.filter(pr_number=issue.number).exists():
                    #         if len(issue.assignees) > 0:
                    #             print(f"issue assignee name: {issue.assignees[0].login}")
                    #             assignee = User.objects.get(username=issue.assignees[0].login)
                    #             if Issue.objects.filter(title=issue.title).exists():
                    #                 prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_status = [i.status for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_closed_on = [i.closed_on for i in Issue.objects.filter(title=issue.title)]
                    #                 print(f"prev_updated_on: {prev_updated_on} , prev_status: {prev_status}")
                    #                 try:
                    #                     if prev_updated_on != issue.updated_at:
                    #                         print(f"prev_updated_on: {prev_updated_on}, updated_at: {issue.updated_at}")
                    #                         Issue.objects.filter(title=issue.title).update(updated_on=issue.updated_at)
                    #                 except:
                    #                     continue
                    #                 if prev_status != issue.state or prev_closed_on != issue.closed_at:
                    #                     Issue.objects.filter(title=issue.title).update(status=issue.state)
                    #                     Issue.objects.filter(title=issue.title).update(closed_on=issue.closed_at)

                    #             elif not Issue.objects.filter(title=issue.title).exists():
                    #                 issue = Issue(
                    #                     assignee = assignee,
                    #                     title = issue.title,
                    #                     issue_number = issue.number,
                    #                     status = issue.state,
                    #                     repo = repo,
                    #                     created_at = issue.created_at,
                    #                     updated_on = issue.updated_at,
                    #                     closed_on = issue.closed_at
                    #                 )
                    #                 issue.save()

                    #         elif len(issue.assignees) == 0:
                    #             assignee = User.objects.get(username="nobody")
                    #             print(f"no_assignee after handling: {assignee}")
                    #             if Issue.objects.filter(title=issue.title).exists():
                    #                 prev_updated_on = [i.updated_on for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_status = [i.status for i in Issue.objects.filter(title=issue.title)]
                    #                 prev_closed_on = [i.closed_on for i in Issue.objects.filter(title=issue.title)]
                    #                 if prev_updated_on != issue.updated_at:
                    #                     print(f"prev_updated_on: {prev_updated_on}, updated_at: {issue.updated_at}")
                    #                     Issue.objects.filter(title=issue.title).update(updated_on=issue.updated_at)
                    #                 if prev_status != issue.state or prev_closed_on != issue.closed_at:
                    #                     Issue.objects.filter(title=issue.title).update(status=issue.state)
                    #                     Issue.objects.filter(title=issue.title).update(closed_on=issue.closed_at)

                    #             elif not Issue.objects.filter(title=issue.title).exists():
                    #                 issue = Issue(
                    #                     assignee = assignee,
                    #                     title = issue.title,
                    #                     issue_number = issue.number,
                    #                     status = issue.state,
                    #                     repo = repo,
                    #                     created_at = issue.created_at,
                    #                     updated_on = issue.updated_at,
                    #                     closed_on = issue.closed_at
                    #                 )
                    #                 issue.save()
                    #     else:
                    #         continue
                    #     print(f"itr number outside loop: {itr}")
