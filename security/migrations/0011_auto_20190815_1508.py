# Generated by Django 2.0 on 2019-08-15 13:08

from django.db import migrations, models
from django.db.models import F
import enumfields.fields
import security.models


def set_created_at_and_changed_at(apps, schema_editor):
    InputLoggedRequest = apps.get_model('security', 'InputLoggedRequest')
    OutputLoggedRequest = apps.get_model('security', 'OutputLoggedRequest')
    CommandLog = apps.get_model('security', 'CommandLog')

    InputLoggedRequest.objects.all().update(created_at=F('request_timestamp'), changed_at=F('request_timestamp'))
    OutputLoggedRequest.objects.all().update(created_at=F('request_timestamp'), changed_at=F('request_timestamp'))
    CommandLog.objects.all().update(created_at=F('start'), changed_at=F('start'))


class Migration(migrations.Migration):
    dependencies = [
        ('security', '0010_auto_20190710_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryTaskLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='changed at')),
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='start')),
                ('stop', models.DateTimeField(blank=True, null=True, verbose_name='stop')),
                ('name', models.CharField(max_length=250, verbose_name='task name')),
                ('state', enumfields.fields.NumEnumField(default=1, enum=security.models.CeleryTaskLogState,
                                                         verbose_name='state')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='error message')),
                ('queue_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='queue name')),
            ],
            options={
                'verbose_name': 'celery task',
                'verbose_name_plural': 'celery tasks',
                'ordering': ('-created_at',),
            },
        ),
        migrations.AlterModelOptions(
            name='commandlog',
            options={'ordering': ('-created_at',), 'verbose_name': 'command log',
                     'verbose_name_plural': 'command logs'},
        ),
        migrations.AlterModelOptions(
            name='inputloggedrequest',
            options={'ordering': ('-created_at',), 'verbose_name': 'input logged request',
                     'verbose_name_plural': 'input logged requests'},
        ),
        migrations.AlterModelOptions(
            name='outputloggedrequest',
            options={'ordering': ('-created_at',), 'verbose_name': 'output logged request',
                     'verbose_name_plural': 'output logged requests'},
        ),
        migrations.AddField(
            model_name='commandlog',
            name='changed_at',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True, blank=True,
                                       verbose_name='changed at'),
        ),
        migrations.AddField(
            model_name='commandlog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True, blank=True,
                                       verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inputloggedrequest',
            name='changed_at',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True, blank=True,
                                       verbose_name='changed at'),
        ),
        migrations.AddField(
            model_name='inputloggedrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True, blank=True,
                                       verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outputloggedrequest',
            name='changed_at',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True, blank=True,
                                       verbose_name='changed at'),
        ),
        migrations.AddField(
            model_name='outputloggedrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True, blank=True,
                                       verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inputloggedrequest',
            name='status',
            field=enumfields.fields.NumEnumField(default=0, enum=security.enums.LoggedRequestStatus,
                                                 verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='inputloggedrequest',
            name='type',
            field=enumfields.fields.NumEnumField(default=1, enum=security.enums.InputLoggedRequestType,
                                                 verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='outputloggedrequest',
            name='status',
            field=enumfields.fields.NumEnumField(default=0, enum=security.enums.LoggedRequestStatus,
                                                 verbose_name='status'),
        ),
        migrations.RunPython(set_created_at_and_changed_at),
    ]
