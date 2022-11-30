import re
from collections import defaultdict
from datetime import datetime
from core.models import PullRequest, Issue


def title_context_cleaner(title):
    return (
        title.lower()
        .replace(",", "")
        .replace("'", "")
        .replace("[", "")
        .replace("]", "")
        .replace('"', "")
        .strip()
    )


def title_label_cleaner(label):
    return label.lower().replace("[", "")


def title_spliter(full_title):
    if full_title.title.find("]") != -1:
        full_text = re.split("\]\s\:|\]\:|\]", full_title.title)
        pre_label, pre_title_context = title_label_cleaner(
            full_text[0]
        ), title_context_cleaner(f"{full_text[1:]}")
        if pre_title_context.find("]") != -1:
            full_text1 = re.split("\]", pre_title_context)
            label1, title_context1 = title_label_cleaner(
                full_text1[0]
            ), title_context_cleaner(f"{full_text1[1:]}")
            label, title_context = f"{pre_label} {label1}", title_context1
        elif pre_title_context.find("]") == -1:
            label, title_context = pre_label, pre_title_context
    elif full_title.title.find("]") == -1 and full_title.title.find(":") != -1:
        full_text = re.split("\:", full_title.title)
        label, title_context = title_label_cleaner(full_text[0]), title_context_cleaner(
            f"{full_text[1:]}"
        )
        if title_context.strip() == "":
            label, title_context = "", label
    else:
        label, title_context = "", title_context_cleaner(full_title.title)
    return label, title_context


def get_pr_model_unique_title():
    model_defaultdict = ""
    model_defaultdict = defaultdict(datetime)
    for pr in PullRequest.objects.all():
        label_model, title_context_model = title_spliter(pr)
        model_defaultdict[title_context_model] = pr.created_at
    return model_defaultdict


def get_issue_model_unique_title():
    model_defaultdict = ""
    model_defaultdict = defaultdict(datetime)
    for issue in Issue.objects.all():
        label_model, title_context_model = title_spliter(issue)
        model_defaultdict[title_context_model] = issue.created_at
    return model_defaultdict
