# Generated by Django 4.2.6 on 2023-10-25 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0008_alter_leave_duration_of_leave"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leave", name="end_date", field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="leave", name="start_date", field=models.DateField(null=True),
        ),
    ]