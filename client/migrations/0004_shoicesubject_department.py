# Generated by Django 5.0.4 on 2024-05-19 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_requestdegreegraduation_is_processed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoicesubject',
            name='department',
            field=models.CharField(blank=True, choices=[('برمجيات', 'برمجيات'), ('شبكات', 'شبكات')], default='برمجيات', max_length=20, null=True),
        ),
    ]
