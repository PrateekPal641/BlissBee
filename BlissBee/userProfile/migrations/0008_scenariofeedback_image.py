# Generated by Django 4.2.5 on 2023-09-28 18:10

from django.db import migrations, models
import userProfile.models


class Migration(migrations.Migration):

    dependencies = [
        ("userProfile", "0007_scenariofeedback_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="scenariofeedback",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=userProfile.models.generate_image_filename,
            ),
        ),
    ]