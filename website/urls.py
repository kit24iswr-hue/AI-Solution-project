from django.urls import path

from . import views
from .chatbot import chatbot_api

app_name = "website"

urlpatterns = [
    path("api/chatbot/", chatbot_api, name="chatbot_api"),
    path("", views.home, name="home"),
    path("index.html", views.home, name="home_legacy"),
    path("about/", views.about, name="about"),
    path("about.html", views.about, name="about_legacy"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("services.html", views.services, name="services_legacy"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/<slug:slug>/", views.portfolio_detail, name="portfolio_detail"),
    path("portfolio.html", views.portfolio, name="portfolio_legacy"),
    path("events/", views.events, name="events"),
    path("events/upcoming/", views.events_by_status, {"status": "upcoming"}, name="events_upcoming"),
    path("events/past/", views.events_by_status, {"status": "past"}, name="events_past"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
    path("events.html", views.events, name="events_legacy"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("testimonials.html", views.testimonials, name="testimonials_legacy"),
    path("articles/", views.articles, name="articles"),
    path("articles/<slug:slug>/", views.article_detail, name="article_detail"),
    path("articles.html", views.articles, name="articles_legacy"),
    path("contact/", views.contact, name="contact"),
    path("contact.html", views.contact, name="contact_legacy"),
    path("dashboard/", views.admin_panel, name="admin_panel"),
    path("admin.html", views.admin_panel, name="admin_panel_legacy"),
]
