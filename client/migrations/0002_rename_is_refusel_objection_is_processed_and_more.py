# Generated by Django 5.0.4 on 2024-05-07 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='objection',
            old_name='is_refusel',
            new_name='is_processed',
        ),
        migrations.AddField(
            model_name='deferment',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='permanence',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='repractical',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='shoicesubject',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='RefuselObjection',
        ),
    ]
