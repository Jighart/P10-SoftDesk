# Generated by Django 4.1.7 on 2023-03-12 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_issue_assignee_alter_issue_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project', to_field='title'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
