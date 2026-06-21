import decimal

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteSetting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("brand_name", models.CharField(default="AI-Solution", max_length=80)),
                ("brand_tagline", models.CharField(default="Digital workplace systems", max_length=120)),
                ("footer_summary", models.TextField(default="Premium AI-powered employee experience solutions for service teams, product leaders, and growing digital operations.")),
                ("location", models.CharField(default="Sunderland, United Kingdom", max_length=160)),
                ("contact_email", models.EmailField(default="hello@ai-solution.example", max_length=254)),
                ("opening_hours", models.CharField(default="Mon to Fri, 9:00 to 17:00", max_length=120)),
                ("home_eyebrow", models.CharField(default="AI workplace systems from Sunderland", max_length=120)),
                ("home_title", models.CharField(default="AI-Solution", max_length=140)),
                ("home_summary", models.TextField(default="AI-powered employee experience tools for faster answers, smarter service discovery, and measurable customer engagement.")),
                ("home_hero_image", models.URLField(default="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1800&q=80")),
                ("home_feature_eyebrow", models.CharField(default="Digital workplace focus", max_length=120)),
                ("home_feature_title", models.CharField(default="Built around customer inquiry, service clarity, and admin insight.", max_length=180)),
                ("operating_eyebrow", models.CharField(default="Operating focus", max_length=120)),
                ("operating_title", models.CharField(default="One connected experience for prospects, customers, and internal teams.", max_length=180)),
                ("operating_summary", models.TextField(default="Service information, customer inquiries, demo interest, events, portfolio evidence, and content insights are brought together through a clean web experience.")),
                ("operating_image", models.URLField(default="https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1100&q=80")),
                ("cta_eyebrow", models.CharField(default="Ready for client review", max_length=120)),
                ("cta_title", models.CharField(default="Book a demo or send an inquiry through the website flow.", max_length=180)),
                ("cta_button_text", models.CharField(default="Contact AI-Solution", max_length=80)),
                ("home_services_eyebrow", models.CharField(default="Services preview", max_length=120)),
                ("home_services_title", models.CharField(default="Practical AI services for growing teams.", max_length=180)),
                ("testimonial_eyebrow", models.CharField(default="Client confidence", max_length=120)),
                ("testimonial_title", models.CharField(default="Trusted for clear prototypes, polished service journeys, and admin insight.", max_length=180)),
                ("testimonial_summary", models.TextField(default="AI-Solution focuses on practical outcomes: easier inquiry handling, stronger customer education, and dashboards that help teams understand demand.")),
            ],
            options={
                "verbose_name": "site setting",
                "verbose_name_plural": "site settings",
            },
        ),
        migrations.CreateModel(
            name="PageContent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("page", models.CharField(choices=[("about", "About"), ("services", "Services"), ("portfolio", "Portfolio"), ("events", "Events"), ("testimonials", "Testimonials"), ("articles", "Articles"), ("contact", "Contact")], max_length=40, unique=True)),
                ("eyebrow", models.CharField(max_length=120)),
                ("title", models.CharField(max_length=220)),
                ("summary", models.TextField()),
                ("image", models.URLField(blank=True)),
                ("secondary_image", models.URLField(blank=True)),
                ("body_eyebrow", models.CharField(blank=True, max_length=120)),
                ("body_title", models.CharField(blank=True, max_length=220)),
                ("body_summary", models.TextField(blank=True)),
                ("secondary_eyebrow", models.CharField(blank=True, max_length=120)),
                ("secondary_title", models.CharField(blank=True, max_length=220)),
            ],
            options={
                "verbose_name": "page content",
                "verbose_name_plural": "page content",
                "ordering": ["page"],
            },
        ),
        migrations.CreateModel(
            name="FeatureCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_published", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("area", models.CharField(choices=[("home_feature", "Home feature"), ("about_mission_point", "About mission point"), ("about_value", "About value")], max_length=40)),
                ("icon", models.CharField(default="sparkles", max_length=80)),
                ("title", models.CharField(max_length=140)),
                ("summary", models.TextField()),
            ],
            options={
                "verbose_name": "feature card",
                "verbose_name_plural": "feature cards",
                "ordering": ["sort_order", "title"],
            },
        ),
        migrations.CreateModel(
            name="Metric",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_published", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("area", models.CharField(choices=[("home_operating", "Home operating metrics"), ("testimonial_showcase", "Testimonial showcase metrics")], max_length=40)),
                ("value", models.CharField(max_length=40)),
                ("label", models.CharField(max_length=120)),
                ("title", models.CharField(default="Metric", max_length=140)),
            ],
            options={
                "verbose_name": "metric",
                "verbose_name_plural": "metrics",
                "ordering": ["sort_order", "title"],
            },
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_published", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("slug", models.SlugField(unique=True)),
                ("icon", models.CharField(default="bot", max_length=80)),
                ("title", models.CharField(max_length=140)),
                ("subtitle", models.CharField(max_length=220)),
                ("summary", models.TextField()),
                ("image", models.URLField()),
                ("metric", models.CharField(blank=True, max_length=40)),
                ("metric_label", models.CharField(blank=True, max_length=120)),
            ],
            options={
                "ordering": ["sort_order", "title"],
            },
        ),
        migrations.CreateModel(
            name="PortfolioItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_published", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("slug", models.SlugField(unique=True)),
                ("category", models.CharField(max_length=120)),
                ("title", models.CharField(max_length=160)),
                ("summary", models.TextField()),
                ("image", models.URLField()),
                ("challenge", models.TextField()),
                ("solution", models.TextField()),
                ("impact", models.TextField()),
            ],
            options={
                "verbose_name": "portfolio item",
                "verbose_name_plural": "portfolio items",
                "ordering": ["sort_order", "title"],
            },
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_published", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("slug", models.SlugField(unique=True)),
                ("status", models.CharField(choices=[("upcoming", "Upcoming"), ("past", "Past")], default="upcoming", max_length=20)),
                ("event_date", models.DateField()),
                ("title", models.CharField(max_length=160)),
                ("summary", models.TextField()),
                ("image", models.URLField()),
                ("location", models.CharField(max_length=180)),
            ],
            options={
                "ordering": ["event_date", "sort_order", "title"],
            },
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_published", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("slug", models.SlugField(unique=True)),
                ("category", models.CharField(max_length=120)),
                ("title", models.CharField(max_length=180)),
                ("published_at", models.DateField()),
                ("read_time", models.CharField(default="5 min read", max_length=40)),
                ("summary", models.TextField()),
                ("image", models.URLField()),
            ],
            options={
                "ordering": ["-published_at", "sort_order", "title"],
            },
        ),
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_published", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("quote", models.TextField()),
                ("name", models.CharField(max_length=120)),
                ("company", models.CharField(max_length=140)),
                ("score", models.DecimalField(decimal_places=1, default=decimal.Decimal("5.0"), max_digits=2)),
                ("title", models.CharField(default="Client testimonial", max_length=140)),
            ],
            options={
                "ordering": ["sort_order", "title"],
            },
        ),
        migrations.CreateModel(
            name="ServiceDeliverable",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=220)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("service", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="deliverables", to="website.service")),
            ],
            options={
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="ServiceSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("heading", models.CharField(max_length=180)),
                ("body", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("service", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sections", to="website.service")),
            ],
            options={
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="PortfolioTechnology",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("portfolio_item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="technologies", to="website.portfolioitem")),
            ],
            options={
                "verbose_name": "portfolio technology",
                "verbose_name_plural": "portfolio technologies",
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="EventAgendaItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=180)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("event", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="agenda_items", to="website.event")),
            ],
            options={
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="ArticleSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("heading", models.CharField(max_length=180)),
                ("body", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("article", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sections", to="website.article")),
            ],
            options={
                "ordering": ["sort_order", "id"],
            },
        ),
    ]
