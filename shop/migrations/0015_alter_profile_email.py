# Generated by Django 5.1.1 on 2024-10-11 17:09

from django.db import migrations, models


def set_unique_email(apps, schema_editor):
    Profile = apps.get_model('shop', 'Profile')
    for profile in Profile.objects.all():
        profile.email = f"{profile.user.username}@example.com"
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.RunPython(set_unique_email),
    ]
