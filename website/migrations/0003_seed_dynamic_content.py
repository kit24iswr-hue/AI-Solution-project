from datetime import date

from django.db import migrations


def seed_site_content(apps, schema_editor):
    SiteSetting = apps.get_model("website", "SiteSetting")
    PageContent = apps.get_model("website", "PageContent")
    FeatureCard = apps.get_model("website", "FeatureCard")
    Metric = apps.get_model("website", "Metric")
    Service = apps.get_model("website", "Service")
    ServiceDeliverable = apps.get_model("website", "ServiceDeliverable")
    ServiceSection = apps.get_model("website", "ServiceSection")
    PortfolioItem = apps.get_model("website", "PortfolioItem")
    PortfolioTechnology = apps.get_model("website", "PortfolioTechnology")
    Event = apps.get_model("website", "Event")
    EventAgendaItem = apps.get_model("website", "EventAgendaItem")
    Article = apps.get_model("website", "Article")
    ArticleSection = apps.get_model("website", "ArticleSection")
    Testimonial = apps.get_model("website", "Testimonial")

    SiteSetting.objects.update_or_create(
        pk=1,
        defaults={
            "brand_name": "AI-Solution",
            "brand_tagline": "Digital workplace systems",
            "footer_summary": "Premium AI-powered employee experience solutions for service teams, product leaders, and growing digital operations.",
            "location": "Sunderland, United Kingdom",
            "contact_email": "hello@ai-solution.example",
            "opening_hours": "Mon to Fri, 9:00 to 17:00",
            "home_eyebrow": "AI workplace systems from Sunderland",
            "home_title": "AI-Solution",
            "home_summary": "AI-powered employee experience tools for faster answers, smarter service discovery, and measurable customer engagement.",
            "home_hero_image": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1800&q=80",
            "home_feature_eyebrow": "Digital workplace focus",
            "home_feature_title": "Built around customer inquiry, service clarity, and admin insight.",
            "operating_eyebrow": "Operating focus",
            "operating_title": "One connected experience for prospects, customers, and internal teams.",
            "operating_summary": "Service information, customer inquiries, demo interest, events, portfolio evidence, and content insights are brought together through a clean web experience.",
            "operating_image": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1100&q=80",
            "cta_eyebrow": "Ready for client review",
            "cta_title": "Book a demo or send an inquiry through the website flow.",
            "cta_button_text": "Contact AI-Solution",
            "home_services_eyebrow": "Services preview",
            "home_services_title": "Practical AI services for growing teams.",
            "testimonial_eyebrow": "Client confidence",
            "testimonial_title": "Trusted for clear prototypes, polished service journeys, and admin insight.",
            "testimonial_summary": "AI-Solution focuses on practical outcomes: easier inquiry handling, stronger customer education, and dashboards that help teams understand demand.",
        },
    )

    pages = [
        {
            "page": "about",
            "eyebrow": "About the company",
            "title": "Human-focused AI for the digital workplace.",
            "summary": "AI-Solution is a Sunderland-based start-up helping organisations improve employee support, customer engagement, and product prototyping through practical AI systems.",
            "image": "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=900&q=80",
            "secondary_image": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1000&q=80",
            "body_eyebrow": "Mission",
            "body_title": "Make workplace support faster, clearer, and more measurable.",
            "body_summary": "The company combines AI assistants, structured web systems, and analytics to help teams answer questions, track engagement, and understand what customers need next.",
            "secondary_eyebrow": "Values",
            "secondary_title": "What shapes the product experience.",
        },
        {
            "page": "services",
            "eyebrow": "Services",
            "title": "AI services made practical, premium, and measurable.",
            "summary": "Each service connects the public website journey with structured inquiry capture, management insight, and better customer experience.",
        },
        {
            "page": "portfolio",
            "eyebrow": "Portfolio",
            "title": "Premium prototype examples for client review.",
            "summary": "Each portfolio item shows how AI-Solution can transform business ideas into usable, measurable digital systems.",
        },
        {
            "page": "events",
            "eyebrow": "Events",
            "title": "Workshops, launches, and AI product sessions.",
            "summary": "Explore upcoming client sessions and past digital workplace events from AI-Solution.",
        },
        {
            "page": "testimonials",
            "eyebrow": "Testimonials",
            "title": "Professional feedback from teams improving digital service quality.",
            "summary": "Client stories give the website credibility while connecting with the project objective of customer satisfaction and measurable engagement.",
        },
        {
            "page": "articles",
            "eyebrow": "Articles",
            "title": "Insights for AI adoption and digital workplace improvement.",
            "summary": "Premium guidance for smarter support, service automation, customer engagement, and early product decisions.",
        },
        {
            "page": "contact",
            "eyebrow": "Contact us",
            "title": "Send an inquiry or schedule a product demo.",
            "summary": "Tell the team what you need and AI-Solution will help you choose the right next step.",
        },
    ]
    for page in pages:
        page_defaults = page.copy()
        page_key = page_defaults.pop("page")
        PageContent.objects.update_or_create(page=page_key, defaults=page_defaults)

    features = [
        ("home_feature", "message-square-text", "Inquiry handling", "Structured customer messages, demo requests, and follow-up records."),
        ("home_feature", "bot", "AI assistance", "Guided support that helps visitors find answers and choose the right service path."),
        ("home_feature", "bar-chart-3", "Engagement analytics", "Admin dashboard concepts for traffic, leads, events, and satisfaction."),
        ("about_mission_point", "check", "Affordable AI prototyping", "Affordable AI prototyping for early product ideas."),
        ("about_mission_point", "check", "Simple interfaces", "Simple interfaces designed for non-technical users."),
        ("about_mission_point", "check", "Useful admin insight", "Admin tools that turn customer activity into useful insight."),
        ("about_value", "shield-check", "Secure by design", "Protected admin access and responsible data handling are treated as baseline practice."),
        ("about_value", "mouse-pointer-click", "Usable first", "Navigation, page structure, and forms are designed for clarity and confidence."),
        ("about_value", "line-chart", "Measurable progress", "Engagement data supports better decisions after launch."),
    ]
    for index, (area, icon, title, summary) in enumerate(features):
        FeatureCard.objects.update_or_create(
            area=area,
            title=title,
            defaults={"icon": icon, "summary": summary, "sort_order": index, "is_published": True},
        )

    metrics = [
        ("home_operating", "8", "Public pages"),
        ("home_operating", "3", "Admin tools"),
        ("home_operating", "4", "Wishlist ideas"),
        ("testimonial_showcase", "92%", "Satisfaction"),
        ("testimonial_showcase", "63", "Demo requests"),
        ("testimonial_showcase", "4.9", "Average score"),
    ]
    for index, (area, value, label) in enumerate(metrics):
        Metric.objects.update_or_create(
            area=area,
            label=label,
            defaults={"title": label, "value": value, "sort_order": index, "is_published": True},
        )

    services = [
        {
            "slug": "ai-virtual-assistant",
            "icon": "bot",
            "title": "AI Virtual Assistant",
            "subtitle": "A guided support experience for customers and employees.",
            "summary": "Answer common questions, qualify inquiries, and guide visitors to the right service or next action.",
            "image": "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?auto=format&fit=crop&w=1200&q=80",
            "metric": "42%",
            "metric_label": "faster inquiry routing",
            "deliverables": ["Website support flow and scripted response map", "Inquiry capture connected to the admin dashboard", "Escalation paths for demos, events, and partnerships"],
            "sections": [
                ("Designed for instant clarity", "The assistant structure helps visitors understand services, choose a relevant path, and submit the right information without searching across many pages."),
                ("Ready for future AI integration", "The current Django version creates the service flow and data capture foundation, with room to connect a richer AI chat model later."),
            ],
        },
        {
            "slug": "prototype-development",
            "icon": "layout-template",
            "title": "Prototype Development",
            "subtitle": "Premium web prototypes for testing product ideas early.",
            "summary": "Turn product ideas into structured pages, workflows, and dashboards before committing to full development.",
            "image": "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1200&q=80",
            "metric": "3x",
            "metric_label": "clearer stakeholder reviews",
            "deliverables": ["Clickable website or dashboard prototype", "Feature map and user journey structure", "Review-ready presentation of core screens"],
            "sections": [
                ("Built for decision making", "Prototype screens show how the product behaves, what content is needed, and where users will take action."),
                ("Practical scope control", "Each prototype focuses on the workflows that matter most, keeping early-stage development affordable and realistic."),
            ],
        },
        {
            "slug": "analytics-reporting",
            "icon": "chart-no-axes-combined",
            "title": "Analytics and Reporting",
            "subtitle": "Admin insight for inquiries, events, content, and satisfaction.",
            "summary": "Collect activity signals in one clean dashboard so teams can understand what customers need next.",
            "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
            "metric": "87%",
            "metric_label": "success prediction score",
            "deliverables": ["Contact inquiry reporting", "Event and demo interest summaries", "Management-ready engagement indicators"],
            "sections": [
                ("Insight without complexity", "The dashboard turns captured activity into simple metrics that support planning, follow-up, and product improvement."),
                ("Connected to the website journey", "Contact forms, service pages, articles, and event interest all become part of the same customer engagement picture."),
            ],
        },
    ]
    for service_index, data in enumerate(services):
        service, _ = Service.objects.update_or_create(
            slug=data["slug"],
            defaults={
                "icon": data["icon"],
                "title": data["title"],
                "subtitle": data["subtitle"],
                "summary": data["summary"],
                "image": data["image"],
                "metric": data["metric"],
                "metric_label": data["metric_label"],
                "sort_order": service_index,
                "is_published": True,
            },
        )
        service.deliverables.all().delete()
        for item_index, text in enumerate(data["deliverables"]):
            ServiceDeliverable.objects.create(service=service, text=text, sort_order=item_index)
        service.sections.all().delete()
        for item_index, (heading, body) in enumerate(data["sections"]):
            ServiceSection.objects.create(service=service, heading=heading, body=body, sort_order=item_index)

    portfolio = [
        ("service-desk-assistant", "Support automation", "Service Desk Assistant", "An AI-enabled inquiry flow for internal employee requests.", "https://images.unsplash.com/photo-1551650975-87deedd944c3?auto=format&fit=crop&w=1200&q=80", "Employees needed a faster way to find help without waiting for manual triage.", "AI-Solution designed a guided service desk journey with categories, escalation points, and dashboard visibility.", "Reduced repeated questions and made priority requests easier to identify.", ["Django", "Structured forms", "Admin reporting"]),
        ("engagement-insights", "Analytics", "Engagement Insights", "A reporting concept for contact forms, events, demos, and article activity.", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80", "The team had customer signals, but they were spread across separate channels.", "A single dashboard concept combined inquiries, demo requests, event interest, and satisfaction indicators.", "Leadership could see demand patterns and plan follow-up with more confidence.", ["SQLite", "Django admin", "Dashboard UI"]),
        ("knowledge-hub", "Content management", "Knowledge Hub", "A structured article and service information system for customer education.", "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80", "Customers needed clearer self-service content before contacting the team.", "A premium content hub grouped service education, adoption advice, and prototype evidence.", "Improved trust and helped prospects choose the right inquiry type.", ["Content strategy", "Responsive templates", "SEO-ready pages"]),
    ]
    for index, (slug, category, title, summary, image, challenge, solution, impact, techs) in enumerate(portfolio):
        item, _ = PortfolioItem.objects.update_or_create(
            slug=slug,
            defaults={"category": category, "title": title, "summary": summary, "image": image, "challenge": challenge, "solution": solution, "impact": impact, "sort_order": index, "is_published": True},
        )
        item.technologies.all().delete()
        for tech_index, name in enumerate(techs):
            PortfolioTechnology.objects.create(portfolio_item=item, name=name, sort_order=tech_index)

    events = [
        ("ai-workflow-discovery", "upcoming", date(2026, 6, 18), "AI Workflow Discovery", "Client workshop for identifying automation opportunities across support and service journeys.", "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=1200&q=80", "Sunderland Innovation Space", ["Workflow mapping", "AI opportunity scoring", "Prototype planning"]),
        ("prototype-review-day", "upcoming", date(2026, 7, 23), "Prototype Review Day", "Demonstration of web prototypes, contact flows, and admin analytics concepts.", "https://images.unsplash.com/photo-1515169067865-5387ec356754?auto=format&fit=crop&w=1200&q=80", "Online and Sunderland", ["Prototype demos", "Client feedback", "Next-sprint planning"]),
        ("digital-experience-launch", "upcoming", date(2026, 8, 14), "Digital Experience Launch", "Showcase for service pages, inquiry forms, event updates, and management reporting.", "https://images.unsplash.com/photo-1556761175-4b46a572b786?auto=format&fit=crop&w=1200&q=80", "Sunderland, United Kingdom", ["Launch walkthrough", "Admin dashboard review", "Success measures"]),
        ("customer-ai-readiness-briefing", "past", date(2026, 4, 10), "Customer AI Readiness Briefing", "A practical session on preparing teams, data, and support journeys for AI adoption.", "https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=1200&q=80", "Virtual briefing", ["Readiness checklist", "Risk review", "Pilot planning"]),
        ("service-design-sprint", "past", date(2026, 3, 6), "Service Design Sprint", "Hands-on sprint for improving service discovery, inquiry capture, and follow-up journeys.", "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&q=80", "Sunderland, United Kingdom", ["Journey mapping", "Content structure", "Prototype review"]),
    ]
    for index, (slug, status, event_date, title, summary, image, location, agenda) in enumerate(events):
        event, _ = Event.objects.update_or_create(
            slug=slug,
            defaults={"status": status, "event_date": event_date, "title": title, "summary": summary, "image": image, "location": location, "sort_order": index, "is_published": True},
        )
        event.agenda_items.all().delete()
        for agenda_index, text in enumerate(agenda):
            EventAgendaItem.objects.create(event=event, text=text, sort_order=agenda_index)

    articles = [
        ("preparing-teams-for-ai-support", "AI Strategy", "Preparing teams for AI-powered support", date(2026, 5, 18), "5 min read", "How organisations can introduce virtual assistance without disrupting existing workflows.", "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80", [("Start with repeated questions", "The best first use cases are high-volume, low-risk questions where the answer is already known and repeatable."), ("Keep escalation visible", "AI support works better when users can quickly move from automated guidance to a human follow-up path."), ("Measure what improves", "Track the number of resolved inquiries, demo requests, and satisfaction signals before expanding the assistant.")]),
        ("customer-engagement-data", "Analytics", "What customer engagement data can reveal", date(2026, 5, 9), "4 min read", "Using contact forms, demo requests, and event activity to shape better services.", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80", [("Look for demand patterns", "Inquiry type, event interest, and article activity can reveal which services customers understand and which need clearer communication."), ("Connect content to action", "A useful website does more than publish information; it shows whether information leads to inquiries, demos, or signups."), ("Use dashboards for decisions", "Simple dashboards help teams prioritise follow-up and decide which product ideas deserve more investment.")]),
        ("early-prototypes-reduce-risk", "Prototyping", "Why early prototypes reduce project risk", date(2026, 4, 26), "6 min read", "Turning business needs into visible designs before full development begins.", "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1200&q=80", [("Make assumptions visible", "Prototype screens expose unclear requirements early, while changes are still inexpensive and easy to explain."), ("Review workflows, not documents", "Stakeholders can respond more accurately when they see the journey instead of only reading written specifications."), ("Build confidence before scale", "A focused prototype gives teams evidence for scope, budget, and the next version of the product.")]),
    ]
    for index, (slug, category, title, published_at, read_time, summary, image, sections) in enumerate(articles):
        article, _ = Article.objects.update_or_create(
            slug=slug,
            defaults={"category": category, "title": title, "published_at": published_at, "read_time": read_time, "summary": summary, "image": image, "sort_order": index, "is_published": True},
        )
        article.sections.all().delete()
        for section_index, (heading, body) in enumerate(sections):
            ArticleSection.objects.create(article=article, heading=heading, body=body, sort_order=section_index)

    testimonials = [
        ("AI-Solution helped us turn a vague support idea into a clear web prototype with a strong admin view.", "Operations Manager", "North East Tech Firm", "5.0"),
        ("The service information became easier to navigate, and our demo requests were much simpler to track.", "Product Lead", "Digital Services Team", "4.9"),
        ("The analytics concept gave us a practical way to understand what customers were asking for.", "Client Success Head", "Workplace Platform", "5.0"),
    ]
    for index, (quote, name, company, score) in enumerate(testimonials):
        Testimonial.objects.update_or_create(
            name=name,
            company=company,
            defaults={"quote": quote, "score": score, "title": f"{name} testimonial", "sort_order": index, "is_published": True},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_dynamic_content_models"),
    ]

    operations = [
        migrations.RunPython(seed_site_content, migrations.RunPython.noop),
    ]
