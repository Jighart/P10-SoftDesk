from rest_framework.viewsets import ModelViewSet
 
from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorSerializer, IssueListSerializer, IssueDetailSerializer, CommentSerializer
from projects.mixins import GetDetailSerializerClassMixin
 
class ProjectViewset(GetDetailSerializerClassMixin, ModelViewSet):
 
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
 
    def get_queryset(self):
        return Project.objects.all()
    

class IssueViewset(GetDetailSerializerClassMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.all()