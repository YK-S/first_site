# Generated by Django 3.1 on 2020-09-30 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_name', models.CharField(max_length=32)),
                ('vote_type', models.IntegerField(choices=[(0, '单选不公开'), (1, '单选公开'), (2, '多选不公开'), (3, '多选公开')])),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField()),
                ('builder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote.user')),
                ('vote_items', models.ManyToManyField(to='vote.Item')),
            ],
            options={
                'db_table': 'vote',
            },
        ),
    ]
