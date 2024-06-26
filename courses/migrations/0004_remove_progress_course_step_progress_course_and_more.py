# Generated by Django 5.0.4 on 2024-06-15 18:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_course_user_alter_coursestep_article_progress'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progress',
            name='course_step',
        ),
        migrations.AddField(
            model_name='progress',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='courses.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='progress',
            name='step',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='courses.coursestep'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='progress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to=settings.AUTH_USER_MODEL),
        ),
    ]
