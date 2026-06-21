import csv
import io

from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .models import (
    Article,
    ArticleSection,
    ContactInquiry,
    Event,
    EventAgendaItem,
    FeatureCard,
    Metric,
    PageContent,
    PortfolioItem,
    PortfolioTechnology,
    Service,
    ServiceDeliverable,
    ServiceSection,
    SiteSetting,
    Testimonial,
)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand and contact", {"fields": ("brand_name", "brand_tagline", "footer_summary", "location", "contact_email", "opening_hours")}),
        ("Home hero", {"fields": ("home_eyebrow", "home_title", "home_summary", "home_hero_image")}),
        ("Home feature cards heading", {"fields": ("home_feature_eyebrow", "home_feature_title")}),
        ("Home operating section", {"fields": ("operating_eyebrow", "operating_title", "operating_summary", "operating_image")}),
        ("Home services heading", {"fields": ("home_services_eyebrow", "home_services_title")}),
        ("Call to action", {"fields": ("cta_eyebrow", "cta_title", "cta_button_text")}),
        ("Testimonials feature", {"fields": ("testimonial_eyebrow", "testimonial_title", "testimonial_summary")}),
    )

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ("page", "eyebrow", "title")
    search_fields = ("title", "summary")


@admin.register(FeatureCard)
class FeatureCardAdmin(admin.ModelAdmin):
    list_display = ("title", "area", "icon", "sort_order", "is_published")
    list_filter = ("area", "is_published")
    list_editable = ("sort_order", "is_published")
    search_fields = ("title", "summary")


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "area", "sort_order", "is_published")
    list_filter = ("area", "is_published")
    list_editable = ("sort_order", "is_published")
    search_fields = ("value", "label")


class ServiceDeliverableInline(admin.TabularInline):
    model = ServiceDeliverable
    extra = 1


class ServiceSectionInline(admin.StackedInline):
    model = ServiceSection
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "metric", "metric_label", "sort_order", "is_published")
    list_filter = ("is_published",)
    list_editable = ("sort_order", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "subtitle")
    inlines = [ServiceDeliverableInline, ServiceSectionInline]


class PortfolioTechnologyInline(admin.TabularInline):
    model = PortfolioTechnology
    extra = 1


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "sort_order", "is_published")
    list_filter = ("category", "is_published")
    list_editable = ("sort_order", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "challenge", "solution", "impact")
    inlines = [PortfolioTechnologyInline]


class EventAgendaItemInline(admin.TabularInline):
    model = EventAgendaItem
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "event_date", "location", "sort_order", "is_published")
    list_filter = ("status", "event_date", "is_published")
    list_editable = ("sort_order", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "location")
    inlines = [EventAgendaItemInline]


class ArticleSectionInline(admin.StackedInline):
    model = ArticleSection
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "read_time", "sort_order", "is_published")
    list_filter = ("category", "published_at", "is_published")
    list_editable = ("sort_order", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary")
    inlines = [ArticleSectionInline]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "score", "sort_order", "is_published")
    list_filter = ("score", "is_published")
    list_editable = ("sort_order", "is_published")
    search_fields = ("quote", "name", "company")


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone_number",
        "company_name",
        "country",
        "job_title",
        "inquiry_type",
        "status",
        "created_at",
    )
    list_filter = ("inquiry_type", "status", "country", "created_at")
    search_fields = (
        "full_name",
        "email",
        "phone_number",
        "company_name",
        "country",
        "job_title",
        "job_details",
    )
    fieldsets = (
        ("Customer details", {"fields": ("full_name", "email", "phone_number", "company_name", "country", "job_title")}),
        ("Inquiry", {"fields": ("inquiry_type", "job_details", "status")}),
    )
    ordering = ("-created_at",)
    actions = ["export_csv", "export_pdf"]

    @admin.action(description="Export selected inquiries to CSV")
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="contact_inquiries.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Full Name",
            "Email",
            "Phone Number",
            "Company Name",
            "Country",
            "Job Title",
            "Inquiry Type",
            "Status",
            "Job Details",
            "Created At",
        ])
        for obj in queryset:
            writer.writerow([
                obj.full_name,
                obj.email,
                obj.phone_number,
                obj.company_name,
                obj.country,
                obj.job_title,
                obj.inquiry_type,
                obj.get_status_display(),
                obj.job_details,
                obj.created_at.strftime("%Y-%m-%d %H:%M"),
            ])
        return response

    @admin.action(description="Export selected inquiries to PDF")
    def export_pdf(self, request, queryset):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            leftMargin=1.5*cm, rightMargin=1.5*cm,
            topMargin=1.5*cm, bottomMargin=1.5*cm,
        )
        styles = getSampleStyleSheet()

        cell_style = styles["Normal"].clone("cell")
        cell_style.fontSize = 8
        cell_style.leading = 11

        header_style = styles["Normal"].clone("hdr")
        header_style.fontSize = 9
        header_style.textColor = colors.white
        header_style.fontName = "Helvetica-Bold"

        def P(text, style=cell_style):
            return Paragraph(str(text), style)

        headers = ["#", "Full Name", "Email", "Phone", "Company", "Country", "Job Title", "Type", "Status", "Job Details", "Created At"]
        data = [[P(h, header_style) for h in headers]]

        for i, obj in enumerate(queryset, 1):
            data.append([
                P(i),
                P(obj.full_name),
                P(obj.email),
                P(obj.phone_number),
                P(obj.company_name),
                P(obj.country),
                P(obj.job_title),
                P(obj.inquiry_type),
                P(obj.get_status_display()),
                P(obj.job_details[:300]),
                P(obj.created_at.strftime("%Y-%m-%d\n%H:%M")),
            ])

        col_widths = [0.7*cm, 2.3*cm, 3.2*cm, 2.2*cm, 2.5*cm, 1.8*cm, 2*cm, 2.1*cm, 1.5*cm, 5.2*cm, 2*cm]
        table = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#006B63")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0fafa")]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#ccdddc")),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))

        elements = [
            Paragraph("Contact Inquiries", styles["Title"]),
            Spacer(1, 0.4*cm),
            table,
        ]
        doc.build(elements)
        buffer.seek(0)
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="contact_inquiries.pdf"'
        return response
