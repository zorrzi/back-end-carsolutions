# Generated by Django 5.1.2 on 2024-10-31 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agendamentos", "0009_feedback_feedbackenviado"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feedback",
            name="feedbackEnviado",
        ),
        migrations.AddField(
            model_name="agendamento",
            name="feedbackEnviado",
            field=models.BooleanField(default=False),
        ),
    ]