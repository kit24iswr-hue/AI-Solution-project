"""Gemini-powered chatbot that answers questions about this website."""
import json

from django.conf import settings
from django.db import OperationalError, ProgrammingError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import (
    Article,
    Event,
    FeatureCard,
    Metric,
    PageContent,
    PortfolioItem,
    Service,
    SiteSetting,
    Testimonial,
)


def _build_site_context():
    """Collect all published content from the DB into one text block."""
    parts = []

    try:
        s = SiteSetting.objects.first()
        if s:
            parts.append(
                f"# About {s.brand_name}\n"
                f"Tagline: {s.brand_tagline}\n"
                f"Location: {s.location}\n"
                f"Contact email: {s.contact_email}\n"
                f"Opening hours: {s.opening_hours}\n"
                f"Description: {s.home_summary}\n"
                f"Footer: {s.footer_summary}\n"
            )
    except (OperationalError, ProgrammingError):
        pass

    try:
        services = Service.objects.filter(is_published=True).prefetch_related("deliverables", "sections")
        if services.exists():
            parts.append("# Services offered")
            for svc in services:
                deliverables = ", ".join(d.text for d in svc.deliverables.all())
                sections = " | ".join(f"{sec.heading}: {sec.body}" for sec in svc.sections.all())
                parts.append(
                    f"## {svc.title}\n"
                    f"{svc.subtitle}\n"
                    f"{svc.summary}\n"
                    + (f"Deliverables: {deliverables}\n" if deliverables else "")
                    + (f"Details: {sections}\n" if sections else "")
                )
    except (OperationalError, ProgrammingError):
        pass

    try:
        portfolio = PortfolioItem.objects.filter(is_published=True).prefetch_related("technologies")
        if portfolio.exists():
            parts.append("# Portfolio / Case Studies")
            for p in portfolio:
                techs = ", ".join(t.name for t in p.technologies.all())
                parts.append(
                    f"## {p.title} ({p.category})\n"
                    f"{p.summary}\n"
                    f"Challenge: {p.challenge}\n"
                    f"Solution: {p.solution}\n"
                    f"Impact: {p.impact}\n"
                    + (f"Technologies: {techs}\n" if techs else "")
                )
    except (OperationalError, ProgrammingError):
        pass

    try:
        events = Event.objects.filter(is_published=True)
        if events.exists():
            parts.append("# Events")
            for e in events:
                parts.append(
                    f"## {e.title} — {e.get_status_display()} on {e.event_date}\n"
                    f"Location: {e.location}\n"
                    f"{e.summary}\n"
                )
    except (OperationalError, ProgrammingError):
        pass

    try:
        articles = Article.objects.filter(is_published=True).prefetch_related("sections")
        if articles.exists():
            parts.append("# Articles / Blog")
            for a in articles:
                section_text = " | ".join(f"{sec.heading}: {sec.body}" for sec in a.sections.all())
                parts.append(
                    f"## {a.title} ({a.category}) — {a.published_at}\n"
                    f"{a.summary}\n"
                    + (f"{section_text}\n" if section_text else "")
                )
    except (OperationalError, ProgrammingError):
        pass

    try:
        testimonials = Testimonial.objects.filter(is_published=True)
        if testimonials.exists():
            parts.append("# Client Testimonials")
            for t in testimonials:
                parts.append(f'"{t.quote}" — {t.name}, {t.company} (rated {t.score}/5)')
    except (OperationalError, ProgrammingError):
        pass

    try:
        metrics = Metric.objects.filter(is_published=True)
        if metrics.exists():
            parts.append("# Key Metrics")
            for m in metrics:
                parts.append(f"{m.value} — {m.label}")
    except (OperationalError, ProgrammingError):
        pass

    try:
        pages = PageContent.objects.all()
        if pages.exists():
            parts.append("# Page descriptions")
            for pg in pages:
                parts.append(f"## {pg.get_page_display()} page\n{pg.title}\n{pg.summary}\n")
    except (OperationalError, ProgrammingError):
        pass

    return "\n\n".join(parts)


SYSTEM_PROMPT = """\
You are a helpful AI assistant embedded on this company website.
Answer questions about the company, its services, portfolio, events, articles, testimonials, and contact details.
Be concise, friendly, and professional.
If the visitor asks something you don't know from the website data, say so honestly and suggest they use the Contact page.
Never make up information that is not in the website data below.

WEBSITE DATA:
{site_context}
"""


@require_POST
@csrf_exempt
def chatbot_api(request):
    try:
        body = json.loads(request.body)
        user_message = body.get("message", "").strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "Invalid request."}, status=400)

    if not user_message:
        return JsonResponse({"error": "Empty message."}, status=400)

    if len(user_message) > 1000:
        return JsonResponse({"error": "Message too long (max 1000 characters)."}, status=400)

    try:
        from google import genai

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        site_context = _build_site_context()
        full_prompt = SYSTEM_PROMPT.format(site_context=site_context) + f"\n\nVisitor: {user_message}\nAssistant:"

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=full_prompt,
        )
        reply = response.text.strip()
    except Exception as exc:
        return JsonResponse({"error": f"AI error: {str(exc)}"}, status=500)

    return JsonResponse({"reply": reply})
