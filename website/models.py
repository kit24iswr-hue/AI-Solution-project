from decimal import Decimal

from django.db import models


class PublishableModel(models.Model):
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["sort_order", "title"]


class SiteSetting(models.Model):
    brand_name = models.CharField(max_length=80, default="AI-Solution")
    brand_tagline = models.CharField(
        max_length=120, default="Digital workplace systems"
    )
    footer_summary = models.TextField(
        default="Premium AI-powered employee experience solutions for service teams, product leaders, and growing digital operations."
    )
    location = models.CharField(max_length=160, default="Sunderland, United Kingdom")
    contact_email = models.EmailField(default="hello@ai-solution.example")
    opening_hours = models.CharField(max_length=120, default="Mon to Fri, 9:00 to 17:00")

    home_eyebrow = models.CharField(
        max_length=120, default="AI workplace systems from Sunderland"
    )
    home_title = models.CharField(max_length=140, default="AI-Solution")
    home_summary = models.TextField(
        default="AI-powered employee experience tools for faster answers, smarter service discovery, and measurable customer engagement."
    )
    home_hero_image = models.ImageField(upload_to="site/", blank=True)
    home_feature_eyebrow = models.CharField(
        max_length=120, default="Digital workplace focus"
    )
    home_feature_title = models.CharField(
        max_length=180,
        default="Built around customer inquiry, service clarity, and admin insight.",
    )
    operating_eyebrow = models.CharField(max_length=120, default="Operating focus")
    operating_title = models.CharField(
        max_length=180,
        default="One connected experience for prospects, customers, and internal teams.",
    )
    operating_summary = models.TextField(
        default="Service information, customer inquiries, demo interest, events, portfolio evidence, and content insights are brought together through a clean web experience."
    )
    operating_image = models.ImageField(upload_to="site/", blank=True)
    cta_eyebrow = models.CharField(max_length=120, default="Ready for client review")
    cta_title = models.CharField(
        max_length=180, default="Book a demo or send an inquiry through the website flow."
    )
    cta_button_text = models.CharField(max_length=80, default="Contact AI-Solution")
    home_services_eyebrow = models.CharField(max_length=120, default="Services preview")
    home_services_title = models.CharField(
        max_length=180, default="Practical AI services for growing teams."
    )

    testimonial_eyebrow = models.CharField(max_length=120, default="Client confidence")
    testimonial_title = models.CharField(
        max_length=180,
        default="Trusted for clear prototypes, polished service journeys, and admin insight.",
    )
    testimonial_summary = models.TextField(
        default="AI-Solution focuses on practical outcomes: easier inquiry handling, stronger customer education, and dashboards that help teams understand demand."
    )

    class Meta:
        verbose_name = "site setting"
        verbose_name_plural = "site settings"

    def __str__(self):
        return self.brand_name


class PageContent(models.Model):
    PAGE_CHOICES = [
        ("about", "About"),
        ("services", "Services"),
        ("portfolio", "Portfolio"),
        ("events", "Events"),
        ("testimonials", "Testimonials"),
        ("articles", "Articles"),
        ("contact", "Contact"),
    ]

    page = models.CharField(max_length=40, choices=PAGE_CHOICES, unique=True)
    eyebrow = models.CharField(max_length=120)
    title = models.CharField(max_length=220)
    summary = models.TextField()
    image = models.ImageField(upload_to="pages/", blank=True)
    secondary_image = models.ImageField(upload_to="pages/", blank=True)
    body_eyebrow = models.CharField(max_length=120, blank=True)
    body_title = models.CharField(max_length=220, blank=True)
    body_summary = models.TextField(blank=True)
    secondary_eyebrow = models.CharField(max_length=120, blank=True)
    secondary_title = models.CharField(max_length=220, blank=True)

    class Meta:
        ordering = ["page"]
        verbose_name = "page content"
        verbose_name_plural = "page content"

    def __str__(self):
        return self.get_page_display()


class FeatureCard(PublishableModel):
    AREA_CHOICES = [
        ("home_feature", "Home feature"),
        ("about_mission_point", "About mission point"),
        ("about_value", "About value"),
    ]

    area = models.CharField(max_length=40, choices=AREA_CHOICES)
    icon = models.CharField(max_length=80, default="sparkles")
    title = models.CharField(max_length=140)
    summary = models.TextField()

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "feature card"
        verbose_name_plural = "feature cards"

    def __str__(self):
        return self.title


class Metric(PublishableModel):
    AREA_CHOICES = [
        ("home_operating", "Home operating metrics"),
        ("testimonial_showcase", "Testimonial showcase metrics"),
    ]

    area = models.CharField(max_length=40, choices=AREA_CHOICES)
    value = models.CharField(max_length=40)
    label = models.CharField(max_length=120)
    title = models.CharField(max_length=140, default="Metric")

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "metric"
        verbose_name_plural = "metrics"

    def __str__(self):
        return f"{self.value} {self.label}"


class Service(PublishableModel):
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=80, default="bot")
    title = models.CharField(max_length=140)
    subtitle = models.CharField(max_length=220)
    summary = models.TextField()
    image = models.ImageField(upload_to="services/", blank=True)
    metric = models.CharField(max_length=40, blank=True)
    metric_label = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class ServiceDeliverable(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="deliverables"
    )
    text = models.CharField(max_length=220)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.text


class ServiceSection(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="sections")
    heading = models.CharField(max_length=180)
    body = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.heading


class PortfolioItem(PublishableModel):
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=120)
    title = models.CharField(max_length=160)
    summary = models.TextField()
    image = models.ImageField(upload_to="portfolio/", blank=True)
    challenge = models.TextField()
    solution = models.TextField()
    impact = models.TextField()

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "portfolio item"
        verbose_name_plural = "portfolio items"

    def __str__(self):
        return self.title


class PortfolioTechnology(models.Model):
    portfolio_item = models.ForeignKey(
        PortfolioItem, on_delete=models.CASCADE, related_name="technologies"
    )
    name = models.CharField(max_length=80)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "portfolio technology"
        verbose_name_plural = "portfolio technologies"

    def __str__(self):
        return self.name


class Event(PublishableModel):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("past", "Past"),
    ]

    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")
    event_date = models.DateField()
    title = models.CharField(max_length=160)
    summary = models.TextField()
    image = models.ImageField(upload_to="events/", blank=True)
    location = models.CharField(max_length=180)

    class Meta:
        ordering = ["event_date", "sort_order", "title"]

    def __str__(self):
        return self.title


class EventAgendaItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="agenda_items")
    text = models.CharField(max_length=180)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.text


class Article(PublishableModel):
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=120)
    title = models.CharField(max_length=180)
    published_at = models.DateField()
    read_time = models.CharField(max_length=40, default="5 min read")
    summary = models.TextField()
    image = models.ImageField(upload_to="articles/", blank=True)

    class Meta:
        ordering = ["-published_at", "sort_order", "title"]

    def __str__(self):
        return self.title


class ArticleSection(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="sections")
    heading = models.CharField(max_length=180)
    body = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.heading


class Testimonial(PublishableModel):
    quote = models.TextField()
    name = models.CharField(max_length=120)
    company = models.CharField(max_length=140)
    score = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal("5.0"))
    title = models.CharField(max_length=140, default="Client testimonial")

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return f"{self.name} - {self.company}"


class ContactInquiry(models.Model):
    INQUIRY_TYPES = [
        ("General inquiry", "General inquiry"),
        ("Schedule demo", "Schedule demo"),
        ("Join event", "Join event"),
        ("Partnership", "Partnership"),
    ]
    STATUS_CHOICES = [
        ("new", "New"),
        ("open", "Open"),
        ("done", "Done"),
    ]

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    company_name = models.CharField(max_length=160)
    country = models.CharField(max_length=100)
    job_title = models.CharField(max_length=120)
    inquiry_type = models.CharField(max_length=40, choices=INQUIRY_TYPES)
    job_details = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "contact inquiries"

    def __str__(self):
        return f"{self.full_name} - {self.inquiry_type}"
