from .models import ReportEngine, EmbeddedReport
class EmbeddedReportResource(PaginatorMixin, APIResource):
    preparer = EMBEDDED_REPORT_LIST_PREPARER
    paginate = True
    page_size = 40

    @property
    def base_query(self):
        return (
            EmbeddedReport.objects.filter(active=True)
            .select_related("engine")
            .order_by("name")
        )

    def prepare(self, data):
        result = super().prepare(data)
        if self.endpoint == "detail":
            result["url"] = data.get_report_url_for_business(self.business)
        return result

    @permissions(needs=("embedded-report-list",))
    def list(self):
        return self.base_query

    @permissions(needs=("embedded-report-list",))
    def detail(self, pk):
        return self.get_or_error(self.base_query, EMBEDDED_REPORT_NOT_FOUND, pk=pk)