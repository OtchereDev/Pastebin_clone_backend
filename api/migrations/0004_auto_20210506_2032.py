# Generated by Django 3.1.5 on 2021-05-06 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210423_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codepaste',
            name='expiration',
            field=models.CharField(choices=[('Never', 'Never'), ('10 min', '10 min'), ('1 hr', '1 hr'), ('1 week', '1 week'), ('2 week', '2 week'), ('1 month', '1 month'), ('6 month', '6 month'), ('1 year', '1 year')], default='0', max_length=30),
        ),
        migrations.AlterField(
            model_name='codepaste',
            name='language',
            field=models.CharField(choices=[('PLAIN', 'PLAIN'), ('PYTHON', 'PYTHON'), ('JAVASCRIPT', 'JAVASCRIPT'), ('GOLANG', 'GOLANG'), ('RUBY', 'RUBY'), ('HTML', 'HTML'), ('JAVA', 'JAVA'), ('JSON', 'JSON'), ('CSS', 'CSS'), ('C#', 'C#'), ('C++', 'C++')], default='0', max_length=30),
        ),
    ]
