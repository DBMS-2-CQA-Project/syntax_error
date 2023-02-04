# Generated by Django 4.1.6 on 2023-02-04 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tags',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('excerpt_post_id', models.IntegerField(verbose_name='excerpt_post_id')),
                ('tag_name', models.CharField(max_length=255, verbose_name='tag_name')),
                ('wiki_post_id', models.IntegerField(default=0)),
            ],
        ),
    ]
