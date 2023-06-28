from django.contrib.auth.models import User
from rest_framework import serializers
from projects.models import Project, Contributor, Issue, Comment


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'author']


class ProjectDetailSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'issues']

    @staticmethod
    def get_issues(instance):
        queryset = Issue.objects.filter(project=instance.id)
        return IssueListSerializer(queryset, many=True).data


class ContributorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'role', 'project', 'user']


class ContributorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'priority', 'author', 'status', 'tag', 'created_time']


class IssueDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'created_time', 'title', 'description', 'priority', 'tag', 'status', 'author', 'assignee', 'project', 'comments']

    @staticmethod
    def get_comments(instance):
        queryset = Comment.objects.filter(issue=instance.id)
        return CommentSerializer(queryset, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only__fields = ['author', 'issue', 'created_time', 'id']
