# Generated by Django 3.0 on 2020-09-16 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_profile_question_survey'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='content',
            new_name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='name',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='questions',
        ),
        migrations.AddField(
            model_name='question',
            name='part_of',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='api.Survey'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='description',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]