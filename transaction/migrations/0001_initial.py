# Generated by Django 3.2.7 on 2021-09-24 14:53

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('merchantId', models.CharField(max_length=30)),
                ('amount', models.CharField(max_length=20)),
                ('createdAt', models.DateField()),
            ],
        ),
    ]
