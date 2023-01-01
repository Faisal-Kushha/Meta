from django.contrib import admin
from .models import ReportEngine, EmbeddedReport

admin.site.register(ReportEngine, EmbeddedReport)