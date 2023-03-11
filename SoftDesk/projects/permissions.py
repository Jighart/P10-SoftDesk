from rest_framework import permissions

from projects.models import Project, Contributor


def check_contributor(user, project):
    for contributor in Contributor.objects.filter(project=project.id):
        if user == contributor.user:
            return True
    return False

class ProjectPermissions(permissions.BasePermission):

    message = 'You dont have permissions to do that.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, obj)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author


class ContributorPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user and request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, Project.objects.filter(id=view.kwargs['projects_pk']).first())

        elif view.action in ['update', 'partial_update', 'create', 'destroy']:
            return request.user == Project.objects.filter(id=view.kwargs['projects_pk']).first().author


class IssuePermissions(permissions.BasePermission):

    message = 'You dont have permission to do that.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list', 'create']:
            return check_contributor(request.user, obj.project)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author


class CommentPermissions(permissions.BasePermission):

    message = 'You dont have permission to do that.'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'list', 'create']:
            return check_contributor(request.user, obj.issue.project)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author