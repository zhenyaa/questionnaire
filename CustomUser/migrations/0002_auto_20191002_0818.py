# Generated by Django 2.2.5 on 2019-10-02 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomUser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='media/images/boy.png', upload_to='images/'),
        ),
    ]
