# Generated by Django 4.2.13 on 2024-05-30 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('location', models.CharField(max_length=100)),
                ('employeeamount', models.IntegerField()),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
