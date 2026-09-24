from django.db import migrations, models

import account.models


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0005_alter_user_email_active_code_alter_user_national_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_active_code',
            field=models.CharField(default=account.models.generate_email_activation_code, max_length=64),
        ),
    ]
