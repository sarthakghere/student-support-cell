# Generated by Django 5.1.5 on 2025-02-09 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_rename_caste_student_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='cet_rank',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='family_income',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='previous_academic_stream',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='special_quota',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
