from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    CharField,
    IntegerField,
    EmailField,
    ReadOnlyField,
    StringRelatedField,
    PrimaryKeyRelatedField,
)
from rest_framework.response import Response
from core.models import Project, Repository, Issue, PullRequest


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["project_name"]


class RepositorySerializer(ModelSerializer):
    class Meta:
        model = Repository
        fields = ["project", "name", "created_at"]


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        field = [
            "repo",
            "assignee",
            "title",
            "issue_number",
            "status",
            "created_at",
            "updated_on",
            "closed_on",
        ]


class PullRequestSerializer(ModelSerializer):
    class Meta:
        model = PullRequest
        fields = [
            "reviewer",
            "repo",
            "title",
            "pr_number",
            "status",
            "created_at",
            "closed_on",
        ]
