# Generated by Django 3.2.9 on 2021-11-25 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MarvelQuiz', '0004_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quiz_Name', models.CharField(max_length=20, unique=True)),
            ],
        ),
    ]
