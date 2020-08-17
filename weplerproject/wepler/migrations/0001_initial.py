# Generated by Django 3.1 on 2020-08-17 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plus_id', models.EmailField(max_length=20, verbose_name='아이디')),
                ('plus_password', models.CharField(max_length=20, verbose_name='비밀번호')),
                ('plus_name', models.CharField(max_length=10, verbose_name='이름')),
                ('plus_class', models.CharField(choices=[('exercise', '운동'), ('music', '음악'), ('study', '공부')], max_length=8, verbose_name='분야')),
                ('plus_edu', models.BooleanField(verbose_name='교육 여부')),
                ('plus_start_date', models.DateTimeField(verbose_name='시작 날짜')),
                ('plus_end_date', models.DateTimeField(verbose_name='끝 날짜')),
                ('plus_address', models.CharField(max_length=30, verbose_name='주소')),
                ('plus_team', models.BooleanField(verbose_name='팀 여부')),
                ('plus_job', models.CharField(choices=[('student', '학생'), ('worker', '직장인')], max_length=7, verbose_name='직업')),
            ],
        ),
        migrations.CreateModel(
            name='plz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plz_id', models.EmailField(max_length=20, verbose_name='아이디')),
                ('plz_password', models.CharField(max_length=20, verbose_name='비밀번호')),
                ('plz_name', models.CharField(max_length=10, verbose_name='이름')),
                ('plz_class', models.CharField(choices=[('exercise', '운동'), ('music', '음악'), ('study', '공부')], max_length=8, verbose_name='분야')),
                ('plz_address', models.CharField(max_length=30, verbose_name='주소')),
                ('plz_group', models.BooleanField(verbose_name='개인 단체 여부')),
            ],
        ),
    ]