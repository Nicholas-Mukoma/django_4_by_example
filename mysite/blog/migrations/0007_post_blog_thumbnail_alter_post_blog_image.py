# Generated by Django 4.2.5 on 2023-10-11 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_blog_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='blog_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images/thumbs'),
        ),
        migrations.AlterField(
            model_name='post',
            name='blog_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images/images'),
        ),
    ]
