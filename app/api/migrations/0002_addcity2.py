# Generated by Django 4.0.4 on 2022-05-15 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddCity2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('temperatuer', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('alertAbove', models.IntegerField(blank=True, null=True)),
                ('alertBelow', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AddCityField2', to='api.profile')),
            ],
        ),
    ]