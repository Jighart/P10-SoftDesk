from rest_framework.viewsets import ModelViewSet
 
from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
 
class ProjectViewset(ModelViewSet):
 
    serializer_class = ProjectSerializer
 
    def get_queryset(self):
        return Project.objects.all()