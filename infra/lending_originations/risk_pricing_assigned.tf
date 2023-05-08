resource "google_pubsub_schema" "risk_pricing_assigned" {
  name       = "risk_pricing_assigned"
  type       = "AVRO"
  definition = file("./lending_originations/schemas/risk_pricing_assigned.json")
}

resource "google_pubsub_topic" "risk_pricing_assigned" {
  name = "risk_pricing_assigned_topic"

  depends_on = [google_pubsub_schema.risk_pricing_assigned]
  schema_settings {
    schema   = "projects/${var.PROJECT_ID}/schemas/${google_pubsub_schema.risk_pricing_assigned.name}"
    encoding = "JSON"
  }
}


resource "google_pubsub_subscription" "risk_pricing_assigned" {
  name                 = "risk_pricing_assigned_subscription"
  topic                = google_pubsub_topic.risk_pricing_assigned.name
  ack_deadline_seconds = 15

  bigquery_config {
    write_metadata      = false
    use_topic_schema    = true
    drop_unknown_fields = true

    table = "${google_bigquery_table.risk_pricing_assigned.project}.${google_bigquery_table.risk_pricing_assigned.dataset_id}.${google_bigquery_table.risk_pricing_assigned.table_id}"
  }

  depends_on = [google_project_iam_member.viewer, google_project_iam_member.editor]
}


data "external" "risk_pricing_assigned_bq_schema" {
  program = ["python", "${path.module}/../functions/avro_to_bigquery.py"]

  query = {
    avro_schema = "./lending_originations/schemas/risk_pricing_assigned.json"
  }
}

resource "google_bigquery_table" "risk_pricing_assigned" {
  deletion_protection = false
  table_id            = "risk_pricing_assigned"
  dataset_id          = google_bigquery_dataset.lending_originations.dataset_id

  schema = data.external.risk_pricing_assigned_bq_schema.result.converted_schema
}
