# Generated by Django 4.2.9 on 2025-07-01 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_masterkaryawan_nokk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nama', models.CharField(blank=True, max_length=250, null=True)),
                ('Lokasi', models.CharField(blank=True, max_length=250, null=True)),
                ('Deskripsi', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='kontrak',
            name='Durasi',
        ),
        migrations.RemoveField(
            model_name='kontrak',
            name='Status',
        ),
        migrations.RemoveField(
            model_name='kontrak',
            name='TipeKontrak',
        ),
        migrations.AddField(
            model_name='kontrak',
            name='JenisKontrak',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='kontrak',
            name='StatusAktif',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='kontrak',
            name='Proyek',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.proyek'),
        ),
    ]
