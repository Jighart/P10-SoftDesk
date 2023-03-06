from rest_framework.viewsets import ModelViewSet
 
from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from projects.mixins import GetDetailSerializerClassMixin
 
class ProjectViewset(GetDetailSerializerClassMixin, ModelViewSet):
 
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
 
    def get_queryset(self):
        return Project.objects.all()
    
    