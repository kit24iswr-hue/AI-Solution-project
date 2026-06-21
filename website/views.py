from django.conf import settings
from django.db import OperationalError, ProgrammingError
from django.db.models import Avg
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AdminLoginForm, ContactInquiryForm
from .models import (
    Article,
    ContactInquiry,
    Event,
    FeatureCard,
    Metric,
    PageContent,
    PortfolioItem,
    Service,
    Testimonial,
)


def home(request):
    context = {
        "active_page": "home",
        "home_features": published(FeatureCard).filter(area="home_feature"),
        "home_metrics": published(Metric).filter(area="home_operating"),
        "services": published(Service)[:3],
    }
    return render(request, "website/home.html", context)


def about(request):
    return render(
        request,
        "website/about.html",
        {
            "active_page": "about",
            "page": page_content("about"),
            "mission_points": published(FeatureCard).filter(area="about_mission_point"),
            "about_values": published(FeatureCard).filter(area="about_value"),
        },
    )


def services(request):
    return render(
        request,
        "website/services.html",
        {
            "active_page": "services",
            "page": page_content("services"),
            "services": published(Service).prefetch_related("deliverables"),
        },
    )


def service_detail(request, slug):
    service = get_object_or_404(
        published(Service).prefetch_related("deliverables", "sections"),
        slug=slug,
    )
    related_services = published(Service).exclude(pk=service.pk)[:2]
    return render(
        request,
        "website/service_detail.html",
        {
            "active_page": "services",
            "service": service,
            "related_services": related_services,
        },
    )


def portfolio(request):
    return render(
        request,
        "website/portfolio.html",
        {
            "active_page": "portfolio",
            "page": page_content("portfolio"),
            "portfolio_items": published(PortfolioItem),
        },
    )


def portfolio_detail(request, slug):
    item = get_object_or_404(
        published(PortfolioItem).prefetch_related("technologies"),
        slug=slug,
    )
    return render(
        request,
        "website/portfolio_detail.html",
        {"active_page": "portfolio", "item": item},
    )


def events(request):
    return events_by_status(request, "upcoming")


def events_by_status(request, status):
    if status not in {"upcoming", "past"}:
        raise Http404("Event status not found.")

    events_queryset = published(Event).filter(status=status).prefetch_related("agenda_items")
    if status == "past":
        events_queryset = events_queryset.order_by("-event_date", "sort_order", "title")

    return render(
        request,
        "website/events.html",
        {
            "active_page": "events",
            "page": page_content("events"),
            "events": events_queryset,
            "current_status": status,
            "upcoming_count": published(Event).filter(status="upcoming").count(),
            "past_count": published(Event).filter(status="past").count(),
        },
    )


def event_detail(request, slug):
    event = get_object_or_404(
        published(Event).prefetch_related("agenda_items"),
        slug=slug,
    )
    return render(
        request,
        "website/event_detail.html",
        {"active_page": "events", "event": event},
    )


def testimonials(request):
    return render(
        request,
        "website/testimonials.html",
        {
            "active_page": "testimonials",
            "page": page_content("testimonials"),
            "testimonial_metrics": published(Metric).filter(area="testimonial_showcase"),
            "testimonials": published(Testimonial),
        },
    )


def articles(request):
    return render(
        request,
        "website/articles.html",
        {
            "active_page": "articles",
            "page": page_content("articles"),
            "articles": published(Article),
        },
    )


def article_detail(request, slug):
    article = get_object_or_404(
        published(Article).prefetch_related("sections"),
        slug=slug,
    )
    related_articles = published(Article).exclude(pk=article.pk)[:2]
    return render(
        request,
        "website/article_detail.html",
        {
            "active_page": "articles",
            "article": article,
            "related_articles": related_articles,
        },
    )


def contact(request):
    success_message = ""
    save_error = ""

    if request.method == "POST":
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                success_message = "Inquiry received. The team will respond shortly."
                form = ContactInquiryForm()
            except (OperationalError, ProgrammingError):
                save_error = "The form is valid, but the database needs migrations first."
    else:
        form = ContactInquiryForm()

    return render(
        request,
        "website/contact.html",
        {
            "active_page": "contact",
            "page": page_content("contact"),
            "form": form,
            "success_message": success_message,
            "save_error": save_error,
        },
    )


def admin_panel(request):
    if request.method == "POST" and request.POST.get("action") == "logout":
        request.session.pop("ai_solution_admin", None)
        return redirect(reverse("website:admin_panel"))

    if not request.session.get("ai_solution_admin"):
        login_form = AdminLoginForm(request.POST or None)
        if request.method == "POST" and login_form.is_valid():
            email = login_form.cleaned_data["email"].strip().lower()
            password = login_form.cleaned_data["password"]
            if (
                email == settings.DEMO_ADMIN_EMAIL.lower()
                and password == settings.DEMO_ADMIN_PASSWORD
            ):
                request.session["ai_solution_admin"] = True
                return redirect(reverse("website:admin_panel"))
            login_form.add_error(None, "Invalid email or password.")

        return render(
            request,
            "website/admin_panel.html",
            {
                "active_page": "admin",
                "is_authenticated": False,
                "login_form": login_form,
            },
        )

    stats, recent_inquiries = get_dashboard_data()
    return render(
        request,
        "website/admin_panel.html",
        {
            "active_page": "admin",
            "is_authenticated": True,
            "stats": stats,
            "recent_inquiries": recent_inquiries,
            "upcoming_events": published(Event).filter(status="upcoming")[:3],
        },
    )


def get_dashboard_data():
    try:
        total_inquiries = ContactInquiry.objects.count()
        demo_requests = ContactInquiry.objects.filter(inquiry_type="Schedule demo").count()
        event_signups = ContactInquiry.objects.filter(inquiry_type="Join event").count()
        recent_inquiries = list(ContactInquiry.objects.all()[:5])
        average_score = Testimonial.objects.filter(is_published=True).aggregate(
            score=Avg("score")
        )["score"]
    except (OperationalError, ProgrammingError):
        total_inquiries = 0
        demo_requests = 0
        event_signups = 0
        recent_inquiries = []
        average_score = None

    stats = {
        "total_inquiries": total_inquiries,
        "demo_requests": demo_requests,
        "event_signups": event_signups,
        "satisfaction": f"{average_score:.1f}" if average_score else "0.0",
    }
    return stats, recent_inquiries


def page_content(page):
    try:
        return PageContent.objects.filter(page=page).first()
    except (OperationalError, ProgrammingError):
        return None


def published(model):
    try:
        return model.objects.filter(is_published=True)
    except (OperationalError, ProgrammingError):
        return model.objects.none()
