from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction
 
from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import UserSerializer, ProjectListSerializer, ProjectDetailSerializer, ContributorSerializer, IssueListSerializer, IssueDetailSerializer, CommentSerializer
from projects.mixins import GetDetailSerializerClassMixin
 

class ProjectViewset(GetDetailSerializerClassMixin, ModelViewSet):
 
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
 
    def get_queryset(self):
        return Project.objects.all()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        project = super(ProjectViewset, self).create(request, *args, **kwargs)
        contributor = Contributor.objects.create(
            user=request.user,
            project=Project.objects.filter(id=project.data['id']).first()
        )
        contributor.save()
        return Response(project.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.id
        request.POST._mutable = False
        return super(ProjectViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(ProjectViewset, self).destroy(request, *args, **kwargs)
    

class IssueViewset(GetDetailSerializerClassMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['projects_pk'])
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.id
        if not request.data['assignee']:
            request.data['assignee'] = request.user.id
        request.data['project'] = self.kwargs['projects_pk']
        request.POST._mutable = False
        return super(IssueViewset, self).create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.id
        if not request.data['assignee']:
            request.data['assignee'] = request.user.id
        request.data['project'] = self.kwargs['projects_pk']
        request.POST._mutable = False
        return super(IssueViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(IssueViewset, self).destroy(request, *args, **kwargs)
    

class ContributorsViewset(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        contributor_users = [contributor.user.id for contributor in Contributor.objects.filter(project=self.kwargs['projects_pk'])]
        return User.objects.filter(id__in=contributor_users)
    

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