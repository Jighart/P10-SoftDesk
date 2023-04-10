from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction

from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorListSerializer, ContributorDetailSerializer, IssueListSerializer, IssueDetailSerializer, CommentSerializer
from projects.mixins import GetDetailSerializerClassMixin
from projects.permissions import ProjectPermissions, ContributorPermissions, IssuePermissions, CommentPermissions
 

@permission_classes([IsAuthenticated, ProjectPermissions])
class ProjectViewset(GetDetailSerializerClassMixin, ModelViewSet):
 
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
 
    def get_queryset(self):
        return Project.objects.all()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.id
        request.POST._mutable = False
        project = super(ProjectViewset, self).create(request, *args, **kwargs)

        contributor = Contributor.objects.create(
            user=request.user,
            project=Project.objects.get(id=project.data['id']),
            role='AUTHOR'
        )
        contributor.save()

        return Response(project.data, status=status.HTTP_201_CREATED)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.id
        request.POST._mutable = False
        return super(ProjectViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(ProjectViewset, self).destroy(request, *args, **kwargs)
    

@permission_classes([ContributorPermissions])
class ContributorsViewset(GetDetailSerializerClassMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs['projects_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['role'] = 'CONTRIBUTOR'
        request.data['project'] = self.kwargs['projects_pk']
        request.POST._mutable = False
        return super(ContributorsViewset, self).create(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        try:
            user_to_delete = Contributor.objects.get(id=self.kwargs['pk'])
            if user_to_delete.user == request.user:
                return Response(data={'error': 'You cannot delete yourself!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Contributor.DoesNotExist:
            return Response(data={'error': 'Contributor does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        
        contributor = Contributor.objects.filter(id=self.kwargs['pk'], project=self.kwargs['projects_pk']).first()
        if contributor:
            contributor.delete()
            return Response('Contributor successfully deleted.', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={'error': 'Contributor not assigned to project!'}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated, IssuePermissions])
class IssueViewset(GetDetailSerializerClassMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['projects_pk'])
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.pk
        if 'assignee' not in request.POST:
            request.data['assignee'] = request.user.pk
        request.data['project'] = self.kwargs['projects_pk']
        request.POST._mutable = False
        return super(IssueViewset, self).create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.pk
        if 'assignee' not in request.POST:
            request.data['assignee'] = request.user.pk
        request.data['project'] = self.kwargs['projects_pk']
        request.POST._mutable = False
        return super(IssueViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(IssueViewset, self).destroy(request, *args, **kwargs)
    

@permission_classes([CommentPermissions])
class CommentViewset(GetDetailSerializerClassMixin, ModelViewSet):

    serializer_class = CommentSerializer
    detail_serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issues_pk'])
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.id
        request.data['issue'] = self.kwargs['issues_pk']
        request.POST._mutable = False
        return super(CommentViewset, self).create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.id
        request.data['issue'] = self.kwargs['issues_pk']
        request.POST._mutable = False
        return super(CommentViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(CommentViewset, self).destroy(request, *args, **kwargs)