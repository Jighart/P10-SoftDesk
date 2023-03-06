from django.contrib.auth.models import User
from rest_framework import serializers
from projects.models import Project, Contributor, Issue, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'author']


class ProjectDetailSerializer(serializers.ModelSerializer):

    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields =  '__all__'

    def get_issues(self, instance):
        queryset = Issue.objects.filter(project=instance.id)
        return IssueListSerializer(queryset, many=True).data


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = '__all__'
        read_only__fields = ('project', 'role', 'id')


class IssueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'priority', 'status', 'tag', 'created_time']


class IssueDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only__fields = ('author', 'issue', 'created_time', 'id')