from types import SimpleNamespace

from django.db import OperationalError, ProgrammingError
from django.db.models import Avg
from django.utils import timezone

from .models import (
    Article,
    ContactInquiry,
    Event,
    FeatureCard,
    Metric,
    PageContent,
    PortfolioItem,
    Service,
    SiteSetting,
    Testimonial,
)


DEFAULT_SITE_SETTINGS = SimpleNamespace(
    brand_name="AI-Solution",
    brand_tagline="Digital workplace systems",
    footer_summary="Premium AI-powered employee experience solutions for service teams, product leaders, and growing digital operations.",
    location="Sunderland, United Kingdom",
    contact_email="hello@ai-solution.example",
    opening_hours="Mon to Fri, 9:00 to 17:00",
    home_eyebrow="AI workplace systems from Sunderland",
    home_title="AI-Solution",
    home_summary="AI-powered employee experience tools for faster answers, smarter service discovery, and measurable customer engagement.",
    home_hero_image="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1800&q=80",
    home_feature_eyebrow="Digital workplace focus",
    home_feature_title="Built around customer inquiry, service clarity, and admin insight.",
    operating_eyebrow="Operating focus",
    operating_title="One connected experience for prospects, customers, and internal teams.",
    operating_summary="Service information, customer inquiries, demo interest, events, portfolio evidence, and content insights are brought together through a clean web experience.",
    operating_image="https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1100&q=80",
    cta_eyebrow="Ready for client review",
    cta_title="Book a demo or send an inquiry through the website flow.",
    cta_button_text="Contact AI-Solution",
    home_services_eyebrow="Services preview",
    home_services_title="Practical AI services for growing teams.",
    testimonial_eyebrow="Client confidence",
    testimonial_title="Trusted for clear prototypes, polished service journeys, and admin insight.",
    testimonial_summary="AI-Solution focuses on practical outcomes: easier inquiry handling, stronger customer education, and dashboards that help teams understand demand.",
)


def site_settings(request):
    try:
        settings = SiteSetting.objects.first() or DEFAULT_SITE_SETTINGS
    except (OperationalError, ProgrammingError):
        settings = DEFAULT_SITE_SETTINGS

    return {"site_settings": settings}


def admin_dashboard(request):
    if request.path.rstrip("/") != "/admin":
        return {}

    try:
        data = build_admin_dashboard()
    except (OperationalError, ProgrammingError):
        data = empty_admin_dashboard()

    return {"admin_dashboard": data}


def build_admin_dashboard():
    today = timezone.localdate()
    months = [add_months(today.replace(day=1), offset) for offset in range(-5, 1)]
    month_keys = {(month.year, month.month): 0 for month in months}
    demo_keys = {(month.year, month.month): 0 for month in months}

    inquiries = list(ContactInquiry.objects.order_by("-created_at"))
    for inquiry in inquiries:
        local_date = timezone.localtime(inquiry.created_at).date()
        key = (local_date.year, local_date.month)
        if key in month_keys:
            month_keys[key] += 1
            if inquiry.inquiry_type == "Schedule demo":
                demo_keys[key] += 1

    trend_max = max([1, *month_keys.values()])
    inquiry_trend = []
    for month in months:
        key = (month.year, month.month)
        total = month_keys[key]
        demos = demo_keys[key]
        inquiry_trend.append(
            {
                "label": month.strftime("%b"),
                "total": total,
                "demos": demos,
                "total_percent": chart_percent(total, trend_max),
                "demo_percent": chart_percent(demos, trend_max),
            }
        )

    status_items = make_distribution(
        [
            ("New", ContactInquiry.objects.filter(status="new").count(), "#f4b740"),
            ("Open", ContactInquiry.objects.filter(status="open").count(), "#087f7a"),
            ("Done", ContactInquiry.objects.filter(status="done").count(), "#3f5e18"),
        ]
    )
    type_items = make_distribution(
        [
            (
                "General",
                ContactInquiry.objects.filter(inquiry_type="General inquiry").count(),
                "#087f7a",
            ),
            (
                "Demos",
                ContactInquiry.objects.filter(inquiry_type="Schedule demo").count(),
                "#e7634f",
            ),
            (
                "Events",
                ContactInquiry.objects.filter(inquiry_type="Join event").count(),
                "#f4b740",
            ),
            (
                "Partners",
                ContactInquiry.objects.filter(inquiry_type="Partnership").count(),
                "#2f80ed",
            ),
        ]
    )

    service_count = Service.objects.filter(is_published=True).count()
    portfolio_count = PortfolioItem.objects.filter(is_published=True).count()
    event_count = Event.objects.filter(is_published=True).count()
    article_count = Article.objects.filter(is_published=True).count()
    testimonial_count = Testimonial.objects.filter(is_published=True).count()
    page_count = PageContent.objects.count()
    feature_count = FeatureCard.objects.filter(is_published=True).count()
    metric_count = Metric.objects.filter(is_published=True).count()
    upcoming_count = Event.objects.filter(is_published=True, status="upcoming").count()
    past_count = Event.objects.filter(is_published=True, status="past").count()
    avg_score = (
        Testimonial.objects.filter(is_published=True).aggregate(score=Avg("score"))[
            "score"
        ]
        or 0
    )

    content_items = make_distribution(
        [
            ("Services", service_count, "#087f7a"),
            ("Portfolio", portfolio_count, "#e7634f"),
            ("Events", event_count, "#f4b740"),
            ("Articles", article_count, "#2f80ed"),
            ("Testimonials", testimonial_count, "#17211f"),
        ]
    )
    content_total = sum(item["count"] for item in content_items)
    content_gradient = conic_gradient(content_items)

    event_pipeline = make_distribution(
        [
            ("Upcoming", upcoming_count, "#087f7a"),
            ("Past", past_count, "#66736f"),
        ]
    )

    total_inquiries = len(inquiries)
    demo_requests = ContactInquiry.objects.filter(inquiry_type="Schedule demo").count()
    open_inquiries = ContactInquiry.objects.filter(status__in=["new", "open"]).count()
    content_assets = (
        service_count
        + portfolio_count
        + event_count
        + article_count
        + testimonial_count
        + page_count
    )
    readiness_score = calculate_readiness_score(
        avg_score=float(avg_score),
        content_assets=content_assets,
        upcoming_events=upcoming_count,
        total_inquiries=total_inquiries,
        demo_requests=demo_requests,
    )

    return {
        "generated_at": timezone.now(),
        "kpi_cards": [
            {
                "label": "Customer inquiries",
                "value": total_inquiries,
                "caption": f"{open_inquiries} need follow-up",
                "icon": "fa-inbox",
                "tone": "teal",
            },
            {
                "label": "Demo requests",
                "value": demo_requests,
                "caption": "Captured from contact forms",
                "icon": "fa-calendar-check",
                "tone": "coral",
            },
            {
                "label": "Upcoming events",
                "value": upcoming_count,
                "caption": f"{past_count} completed sessions",
                "icon": "fa-calendar-alt",
                "tone": "amber",
            },
            {
                "label": "Average rating",
                "value": f"{avg_score:.1f}",
                "caption": f"{testimonial_count} published testimonials",
                "icon": "fa-star",
                "tone": "ink",
            },
            {
                "label": "Content assets",
                "value": content_assets,
                "caption": f"{page_count} managed pages",
                "icon": "fa-layer-group",
                "tone": "blue",
            },
            {
                "label": "Readiness score",
                "value": f"{readiness_score}%",
                "caption": "Content, events, reviews, demand",
                "icon": "fa-tachometer-alt",
                "tone": "green",
            },
        ],
        "inquiry_trend": inquiry_trend,
        "status_items": status_items,
        "type_items": type_items,
        "content_items": content_items,
        "content_total": content_total,
        "content_gradient": content_gradient,
        "event_pipeline": event_pipeline,
        "recent_inquiries": inquiries[:6],
        "upcoming_events": Event.objects.filter(
            is_published=True, status="upcoming"
        ).order_by("event_date")[:5],
        "inventory": [
            {"label": "Pages", "count": page_count},
            {"label": "Services", "count": service_count},
            {"label": "Portfolio cases", "count": portfolio_count},
            {"label": "Articles", "count": article_count},
            {"label": "Events", "count": event_count},
            {"label": "Feature cards", "count": feature_count},
            {"label": "Metrics", "count": metric_count},
            {"label": "Testimonials", "count": testimonial_count},
        ],
    }


def empty_admin_dashboard():
    return {
        "generated_at": timezone.now(),
        "kpi_cards": [],
        "inquiry_trend": [],
        "status_items": [],
        "type_items": [],
        "content_items": [],
        "content_total": 0,
        "content_gradient": "conic-gradient(#d9e1de 0% 100%)",
        "event_pipeline": [],
        "recent_inquiries": [],
        "upcoming_events": [],
        "inventory": [],
    }


def add_months(value, offset):
    month = value.month - 1 + offset
    year = value.year + month // 12
    month = month % 12 + 1
    return value.replace(year=year, month=month)


def chart_percent(value, total):
    if value <= 0:
        return 0
    return max(10, round((value / total) * 100))


def make_distribution(items):
    total = sum(count for _, count, _ in items) or 1
    return [
        {
            "label": label,
            "count": count,
            "color": color,
            "percent": round((count / total) * 100),
        }
        for label, count, color in items
    ]


def conic_gradient(items):
    total = sum(item["count"] for item in items)
    if total == 0:
        return "conic-gradient(#d9e1de 0% 100%)"

    cursor = 0
    segments = []
    for item in items:
        end = cursor + (item["count"] / total) * 100
        segments.append(f"{item['color']} {cursor:.2f}% {end:.2f}%")
        cursor = end
    return f"conic-gradient({', '.join(segments)})"


def calculate_readiness_score(
    avg_score, content_assets, upcoming_events, total_inquiries, demo_requests
):
    rating_score = (avg_score / 5) * 100 if avg_score else 0
    content_score = min(100, content_assets * 4)
    event_score = min(100, upcoming_events * 25)
    demand_score = min(100, (total_inquiries * 4) + (demo_requests * 12))
    score = (
        rating_score * 0.35
        + content_score * 0.35
        + event_score * 0.2
        + demand_score * 0.1
    )
    return round(score)
