
resource "google_pubsub_schema" "phase_outcomes" {
  name       = "phase_outcomes"
  type       = "AVRO"
  definition = file("./lending_originations/schemas/phase_outcomes.json")
}

resource "google_pubsub_topic" "phase_outcomes" {
  name = "phase_outcomes_topic"

  depends_on = [google_pubsub_schema.phase_outcomes]
  schema_settings {
    schema   = "projects/${var.PROJECT_ID}/schemas/${google_pubsub_schema.phase_outcomes.name}"
    encoding = "JSON"
  }
}


resource "google_pubsub_subscription" "phase_outcomes" {
  name                 = "phase_outcomes_subscription"
  topic                = google_pubsub_topic.phase_outcomes.name
  ack_deadline_seconds = 15

  bigquery_config {
    write_metadata      = false
    use_topic_schema    = true
    drop_unknown_fields = true

    table = "${google_bigquery_table.phase_outcomes.project}.${google_bigquery_table.phase_outcomes.dataset_id}.${google_bigquery_table.phase_outcomes.table_id}"
  }

  depends_on = [google_project_iam_member.viewer, google_project_iam_member.editor]
}


data "external" "phase_outcomes_bq_schema" {
  program = ["python", "${path.module}/../functions/avro_to_bigquery.py"]

  query = {
    avro_schema = "./lending_originations/schemas/phase_outcomes.json"
  }
}

resource "google_bigquery_table" "phase_outcomes" {
  deletion_protection = false
  table_id            = "phase_outcomes"
  dataset_id          = google_bigquery_dataset.lending_originations.dataset_id

  schema = data.external.phase_outcomes_bq_schema.result.converted_schema
}
