# Generated by Django 2.2.16 on 2021-09-16 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20210916_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='ЧПУ'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(help_text='Группа1, к которой будет относиться пост', max_length=200, verbose_name='Заголовок'),
        ),
    ]