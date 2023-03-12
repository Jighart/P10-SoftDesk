from django.contrib import admin
from .models import Issue, Project, Contributor, Comment


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role')


@admin.register(Comment)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('issue',)