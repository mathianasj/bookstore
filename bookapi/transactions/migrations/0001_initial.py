# Generated by Django 4.0.3 on 2022-03-24 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0003_alter_book_isbn'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_datetime', models.DateTimeField()),
                ('transaction_type', models.CharField(choices=[('CO', 'CHECKOUT'), ('CI', 'CHECKIN'), ('RN', 'RENEW')], max_length=2)),
                ('due_date', models.DateField()),
                ('active', models.BooleanField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('book', 'active')},
            },
        ),
    ]