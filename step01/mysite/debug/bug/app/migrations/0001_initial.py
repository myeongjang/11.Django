# Generated by Django 2.0.2 on 2018-03-03 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alpha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dummy', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Bravo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dummy', models.CharField(default='', max_length=10)),
                ('alpha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Alpha')),
            ],
        ),
    ]