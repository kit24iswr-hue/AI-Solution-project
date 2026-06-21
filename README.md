# AI-Solution Django Website

This is the Django/Python version of the AI-Solution website. The original static HTML files are still in the project root, and the Django app lives in `ai_solutions/` and `website/`.

## Run Locally

Install Python, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Pages

- Home: `/`
- About: `/about/`
- Services: `/services/`
- Portfolio: `/portfolio/`
- Events: `/events/`
- Testimonials: `/testimonials/`
- Articles: `/articles/`
- Contact: `/contact/`
- Jazzmin Django admin: `/admin/`
- Demo dashboard: `/dashboard/`

The demo admin dashboard uses:

```text
Email: admin@ai-solution.example
Password: admin123
```

Contact form submissions are saved to SQLite after `py manage.py migrate`.

## Dynamic Admin Content

The public website is controlled from the Jazzmin Django admin at `/admin/`.

Editable models include:

- Site settings: brand, footer, contact details, home hero, home CTA, testimonial feature
- Page content: page headings, summaries, and page images
- Feature cards and metrics
- Services with deliverables and detail sections
- Portfolio items with technologies
- Events with upcoming/past status and agenda items
- Articles with detail sections
- Testimonials
- Contact inquiries

Services, portfolio items, events, and articles also have detail pages. Examples:

- `/services/ai-virtual-assistant/`
- `/portfolio/service-desk-assistant/`
- `/events/upcoming/`
- `/events/past/`
- `/articles/preparing-teams-for-ai-support/`
