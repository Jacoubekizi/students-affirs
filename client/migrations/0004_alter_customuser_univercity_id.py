# Generated by Django 5.0.4 on 2024-05-07 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_customuser_is_employee_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='univercity_id',
            field=models.IntegerField(blank=True, default=12, null=True),
        ),
    ]
