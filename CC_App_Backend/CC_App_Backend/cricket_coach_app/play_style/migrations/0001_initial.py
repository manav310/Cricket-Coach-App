# Generated by Django 5.0.6 on 2024-07-28 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_name', models.CharField(default='Play Style', max_length=100)),
                ('analyzed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
