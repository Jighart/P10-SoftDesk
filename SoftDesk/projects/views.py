from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
 
from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorListSerializer, ContributorDetailSerializer, IssueListSerializer, IssueDetailSerializer, CommentSerializer
from projects.mixins import GetDetailSerializerClassMixin
from projects.permissions import ProjectPermissions, ContributorPermissions, IssuePermissions, CommentPermissions
 

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
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['author'] = request.user.id
        request.POST._mutable = False
        return super(ProjectViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(ProjectViewset, self).destroy(request, *args, **kwargs)
    

class ContributorsViewset(GetDetailSerializerClassMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs['projects_pk'])

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = ContributorListSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                user_to_add = User.objects.filter(id=request.data['user']).first()
                print(user_to_add)
                if user_to_add:
                    contributor = Contributor.objects.create(
                        user=user_to_add,
                        project=Project.objects.filter(id=self.kwargs['projects_pk']).first()
                    )
                    contributor.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(data={'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError:
                return Response(data={'error': 'User already added!'}, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        user_to_delete = Contributor.objects.filter(id=self.kwargs['pk']).first()
        print(user_to_delete)
        if user_to_delete == request.user:
            return Response(data={'error': 'You cannot delete yourself!'}, status=status.HTTP_400_BAD_REQUEST)
        if user_to_delete:
            contributor = Contributor.objects.filter(id=self.kwargs['pk'], project=self.kwargs['projects_pk']).first()
            if contributor.role == 'AUTHOR':
                return Response('Project author cannot be deleted!', status=status.HTTP_400_BAD_REQUEST)
            if contributor:
                contributor.delete()
                return Response('Contributor successfully deleted.', status=status.HTTP_204_NO_CONTENT)
            return Response(data={'error': 'Contributor not assigned to project!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
    

class IssueViewset(GetDetailSerializerClassMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['projects_pk'])
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        if not request.data['author']:
            request.data['author'] = request.user.id
        if not request.data['assignee']:
            request.data['assignee'] = request.user.id
        request.data['project'] = self.kwargs['projects_pk']
        request.POST._mutable = False
        return super(IssueViewset, self).create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        if not request.data['author']:
            request.data['author'] = request.user.id
        if not request.data['assignee']:
            request.data['assignee'] = request.user.id
        request.data['project'] = self.kwargs['projects_pk']
        request.POST._mutable = False
        return super(IssueViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(IssueViewset, self).destroy(request, *args, **kwargs)
    

class CommentViewset(GetDetailSerializerClassMixin, ModelViewSet):

    serializer_class = CommentSerializer
    detail_serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issues_pk'])
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        if not request.data['author']:
            request.data['author'] = request.user.id
        request.data['issue'] = self.kwargs['issues_pk']
        request.POST._mutable = False
        return super(CommentViewset, self).create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        if not request.data['author']:
            request.data['author'] = request.user.id
        request.data['issue'] = self.kwargs['issues_pk']
        request.POST._mutable = False
        return super(CommentViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(CommentViewset, self).destroy(request, *args, **kwargs)