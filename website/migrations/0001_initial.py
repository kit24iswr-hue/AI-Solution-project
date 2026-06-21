from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactInquiry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                (
                    "inquiry_type",
                    models.CharField(
                        choices=[
                            ("General inquiry", "General inquiry"),
                            ("Schedule demo", "Schedule demo"),
                            ("Join event", "Join event"),
                            ("Partnership", "Partnership"),
                        ],
                        max_length=40,
                    ),
                ),
                ("message", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "New"),
                            ("open", "Open"),
                            ("done", "Done"),
                        ],
                        default="new",
                        max_length=12,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "contact inquiries",
                "ordering": ["-created_at"],
            },
        ),
    ]
