# Generated by Django 4.1.3 on 2022-11-10 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="closed_on",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="issue",
            name="updated_on",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="pullrequest",
            name="closed_on",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
