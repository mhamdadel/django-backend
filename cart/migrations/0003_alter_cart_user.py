# Generated by Django 4.2 on 2023-05-15 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0002_remove_cart_id_alter_cart_user_alter_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='cart', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
