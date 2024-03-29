# Generated by Django 4.2.7 on 2023-12-17 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ForGramGiftModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128)),
                ('count', models.IntegerField(default=100)),
                ('used', models.IntegerField(default=0)),
                ('volum', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Gitf',
                'verbose_name_plural': 'Gift',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ForGramModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128)),
                ('bot_token', models.CharField(max_length=128)),
                ('api_id', models.CharField(max_length=128)),
                ('api_hash', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Forgram Data',
                'verbose_name_plural': 'Forgram Data',
            },
        ),
        migrations.CreateModel(
            name='ForgramPlansModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=128, unique=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('day', models.IntegerField(default=0)),
                ('volum', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField()),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('discount', models.IntegerField(blank=True, default=0, null=True)),
                ('is_discount', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('forgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='forgram.forgrammodel')),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Plans',
            },
        ),
        migrations.CreateModel(
            name='SubForGramUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiry', models.DateTimeField(blank=True, null=True)),
                ('volum', models.IntegerField(blank=True, default=0, null=True)),
                ('volum_used', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('forgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forgram.forgrammodel')),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forgram.forgramplansmodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Subscription',
                'verbose_name_plural': 'User Subscription',
            },
        ),
        migrations.CreateModel(
            name='ForGramUsersModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True, null=True)),
                ('forgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forgram.forgrammodel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fg', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'User',
            },
        ),
        migrations.CreateModel(
            name='ForGramUserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_name', models.CharField(max_length=128)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User session',
                'verbose_name_plural': 'User session',
            },
        ),
        migrations.CreateModel(
            name='ForGramUserMessageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.JSONField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(blank=True, default='message', max_length=16, null=True)),
                ('message_id', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Message',
                'verbose_name_plural': 'User Message',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ForGramUserLinkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=1024, null=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now=True, null=True)),
                ('forgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link', to='forgram.forgrammodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User links',
                'verbose_name_plural': 'User links',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ForgramUserInvoiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('is_paid', models.CharField(blank=True, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid'), ('paying', 'Paying')], default='unpaid', max_length=10, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('notes', models.TextField(blank=True, null=True)),
                ('is_discount', models.BooleanField(default=False)),
                ('buyer_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('forgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forgram.forgrammodel')),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forgram.forgramplansmodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User invoice',
                'verbose_name_plural': 'User invoice',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ForGramUseGift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('gift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gift_used', to='forgram.forgramgiftmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gift', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Gitf Used',
                'verbose_name_plural': 'Gift Used',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ForGramSettingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('setting', models.JSONField()),
                ('forgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='forgram.forgrammodel')),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Setting',
            },
        ),
        migrations.CreateModel(
            name='ForGramRefUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('invited_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invited_user', to=settings.AUTH_USER_MODEL)),
                ('inviting_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inviting_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User invitation',
                'verbose_name_plural': 'User invitations',
            },
        ),
        migrations.CreateModel(
            name='ForGramPaymentHistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('is_paid', models.BooleanField(default=False)),
                ('cart_number', models.CharField(blank=True, max_length=128, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('request_date', models.DateTimeField(auto_now=True)),
                ('forgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_history', to='forgram.forgrammodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment history',
                'verbose_name_plural': 'Payment history',
                'ordering': ['-request_date'],
            },
        ),
        migrations.CreateModel(
            name='ForGramMessageSenderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('forgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forgram.forgrammodel')),
            ],
            options={
                'verbose_name': 'Send message',
                'verbose_name_plural': 'Send message',
            },
        ),
        migrations.AddField(
            model_name='forgramgiftmodel',
            name='forgram',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gift', to='forgram.forgrammodel'),
        ),
        migrations.CreateModel(
            name='ForGramForwarderAdvanceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_channel', models.CharField(blank=True, max_length=32, null=True)),
                ('destination_channel', models.CharField(blank=True, max_length=32, null=True)),
                ('text_filters', models.JSONField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('session_name', models.CharField(blank=True, max_length=128, null=True)),
                ('status', models.CharField(choices=[('Completed', 'completed'), ('In Progress', 'in_progress'), ('Not Completed', 'not_completed')], default='Not Completed', max_length=20)),
                ('created', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(blank=True, choices=[('allposts', 'allposts'), ('momentary', 'momentary')], max_length=20, null=True)),
                ('text', models.BooleanField(blank=True, default=True, null=True)),
                ('photo', models.BooleanField(blank=True, default=True, null=True)),
                ('audio', models.BooleanField(blank=True, default=True, null=True)),
                ('document', models.BooleanField(blank=True, default=True, null=True)),
                ('sticker', models.BooleanField(blank=True, default=True, null=True)),
                ('video', models.BooleanField(blank=True, default=True, null=True)),
                ('animation', models.BooleanField(blank=True, default=True, null=True)),
                ('voice', models.BooleanField(blank=True, default=True, null=True)),
                ('video_note', models.BooleanField(blank=True, default=True, null=True)),
                ('pid', models.IntegerField(blank=True, null=True)),
                ('forgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forwarder_advance', to='forgram.forgrammodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forwarder_advance', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]