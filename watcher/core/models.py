from django.db import models
from django.contrib.auth.models import User

    
class Project(models.Model):
    __table__ = "project"
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Repository(models.Model):
    __table__ = "repository"
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    
    def __str__(self):
        return self.name

class Issue(models.Model):
    __tablename__ = "issues"
    repo = models.ForeignKey(Repository, blank=True, null=True, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    issue_number = models.IntegerField()
    status = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_on = models.DateTimeField(blank=True,null=True)
    closed_on = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.repo} > {self.issue_number}"

class PullRequest(models.Model):
    __tablename__ = "pull_requests"
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repository, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    pr_number = models.IntegerField()
    status = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_on = models.DateTimeField(blank=True,null=True)
    closed_on = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.repo} > {self.pr_number}"
