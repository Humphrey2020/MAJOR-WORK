# Generated by Django 4.2.15 on 2024-08-29 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("elda", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CandidateProfile",
            new_name="Candidate",
        ),
        migrations.RenameModel(
            old_name="StaffProfile",
            new_name="Staff",
        ),
    ]
