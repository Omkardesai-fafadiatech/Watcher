from django.contrib import admin
from .models import Project, Repository, Issue, PullRequest


admin.site.register(Project)
admin.site.register(Repository)
admin.site.register(Issue)
admin.site.register(PullRequest)