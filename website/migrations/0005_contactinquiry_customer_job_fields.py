from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_alter_article_image_alter_event_image_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contactinquiry",
            old_name="message",
            new_name="job_details",
        ),
        migrations.AddField(
            model_name="contactinquiry",
            name="phone_number",
            field=models.CharField(default="", max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="contactinquiry",
            name="company_name",
            field=models.CharField(default="", max_length=160),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="contactinquiry",
            name="country",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="contactinquiry",
            name="job_title",
            field=models.CharField(default="", max_length=120),
            preserve_default=False,
        ),
    ]
