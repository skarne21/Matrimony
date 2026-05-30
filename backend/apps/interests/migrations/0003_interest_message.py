from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='message',
            field=models.TextField(blank=True, default=''),
        ),
    ]
