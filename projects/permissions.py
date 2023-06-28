from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from projects.models import Project, Contributor


def check_contributor(user, project):
    for contributor in Contributor.objects.filter(project=project.id):
        if user == contributor.user:
            return True
    return False


class ProjectPermissions(permissions.BasePermission):

    message = 'You don\'t have permissions to do that.'

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return check_contributor(request.user, obj)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.author


class ContributorPermissions(permissions.BasePermission):

    message = 'You don\'t have permissions to do that.'

    def has_permission(self, request, view):
        try:
            if view.action in ['retrieve', 'list']:
                return check_contributor(request.user, Project.objects.get(id=view.kwargs['projects_pk']))
            elif view.action in ['update', 'partial_update', 'create', 'destroy']:
                return request.user == Project.objects.get(id=view.kwargs['projects_pk']).author
        except Exception:
            return False


class IssuePermissions(permissions.BasePermission):

    message = 'You don\'t have permissions to do that.'

    def has_permission(self, request, view):
        try:
            if view.action in ['retrieve', 'list', 'create']:
                return check_contributor(request.user, Project.objects.get(id=view.kwargs['projects_pk']))
            elif view.action in ['update', 'partial_update', 'destroy']:
                return request.user == Project.objects.get(id=view.kwargs['projects_pk']).author
        except Exception:
            return False


class CommentPermissions(permissions.BasePermission):

    message = 'You don\'t have permissions to do that.'

    def has_permission(self, request, view):
        try:
            if view.action in ['retrieve', 'list', 'create']:
                return check_contributor(request.user, Project.objects.get(id=view.kwargs['projects_pk']))
            elif view.action in ['update', 'partial_update', 'destroy']:
                return request.user == Project.objects.get(id=view.kwargs['projects_pk']).author
        except Exception:
            return False
