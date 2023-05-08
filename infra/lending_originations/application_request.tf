
resource "google_pubsub_schema" "application_request" {
  name       = "application_request"
  type       = "AVRO"
  definition = file("./lending_originations/schemas/application_request.json")
}

resource "google_pubsub_topic" "application_request" {
  name = "application_request_topic"

  depends_on = [google_pubsub_schema.application_request]
  schema_settings {
    schema   = "projects/${var.PROJECT_ID}/schemas/${google_pubsub_schema.application_request.name}"
    encoding = "JSON"
  }
}


resource "google_pubsub_subscription" "application_request" {
  name                 = "application_request_subscription"
  topic                = google_pubsub_topic.application_request.name
  ack_deadline_seconds = 15

  bigquery_config {
    write_metadata      = false
    use_topic_schema    = true
    drop_unknown_fields = true

    table = "${google_bigquery_table.application_request.project}.${google_bigquery_table.application_request.dataset_id}.${google_bigquery_table.application_request.table_id}"
  }

  depends_on = [google_project_iam_member.viewer, google_project_iam_member.editor]
}


data "external" "application_request_bq_schema" {
  program = ["python", "${path.module}/../functions/avro_to_bigquery.py"]

  query = {
    avro_schema = "./lending_originations/schemas/application_request.json"
  }
}

resource "google_bigquery_table" "application_request" {
  deletion_protection = false
  table_id            = "application_request"
  dataset_id          = google_bigquery_dataset.lending_originations.dataset_id

  schema = data.external.application_request_bq_schema.result.converted_schema
}
