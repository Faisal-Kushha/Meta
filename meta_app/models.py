from django.db import models
import jwt
import time
from hashid_field import HashidAutoField

class ReportEngine(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    type = models.CharField(
        choices=(("metabase", "Metabase"),), default="metabase", max_length=50
    )
    base_url = models.URLField()
    integration_api_key = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class EmbeddedReport(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    engine = models.ForeignKey(ReportEngine, on_delete=models.PROTECT)
    reference_id = models.CharField(
        help_text="Report ID on the engine, like question id, dashboard id on Metabase",
        max_length=50,
    )
    reference_type = models.CharField(
        choices=(
            ("single_report", "Question/Single Report"),
            ("dashboard", "Dashboard"),
        ),
        max_length=50,
    )
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_report_url_for_business(self, business):
      map_resource = {
          "dashboard": {
              "params": {"dashboard": int(self.reference_id)},
              "url_path": "dashboard",
          },
          "single_report": {
              "params": {"question": int(self.reference_id)},
              "url_path": "question",
          },
      }

      resource = map_resource[self.reference_type]

      payload = {
          "resource": resource["params"],
          "params": {"organization_id": business.organization_id},
          "exp": round(time.time()) + (60 * 10),  # 10 minute expiration
      }

      token = jwt.encode(
          payload, self.engine.integration_api_key, algorithm="HS256"
      ).decode("utf8")

      return "{}/embed/{}/{}#bordered=false&titled=false".format(
          self.engine.base_url, resource["url_path"], token
      )
