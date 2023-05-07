resource "google_pubsub_schema" "policy_rule_results" {
  name       = "policy_rule_results"
  type       = "AVRO"
  definition = file("./lending_originations/schemas/policy_rule_results.json")
}

resource "google_pubsub_topic" "policy_rule_results" {
  name = "policy_rule_results_topic"

  depends_on = [google_pubsub_schema.policy_rule_results]
  schema_settings {
    schema   = "projects/${var.PROJECT_ID}/schemas/${google_pubsub_schema.policy_rule_results.name}"
    encoding = "JSON"
  }
}


resource "google_pubsub_subscription" "policy_rule_results" {
  name                 = "policy_rule_results_subscription"
  topic                = google_pubsub_topic.policy_rule_results.name
  ack_deadline_seconds = 15

  bigquery_config {
    write_metadata      = false
    use_topic_schema    = true
    drop_unknown_fields = true

    table = "${google_bigquery_table.policy_rule_results.project}.${google_bigquery_table.policy_rule_results.dataset_id}.${google_bigquery_table.policy_rule_results.table_id}"
  }

  depends_on = [google_project_iam_member.viewer, google_project_iam_member.editor]
}


data "external" "policy_rule_results_bq_schema" {
  program = ["python", "${path.module}/../functions/avro_to_bigquery.py"]

  query = {
    avro_schema = "./lending_originations/schemas/policy_rule_results.json"
  }
}

resource "google_bigquery_table" "policy_rule_results" {
  deletion_protection = false
  table_id            = "policy_rule_results"
  dataset_id          = google_bigquery_dataset.lending_originations.dataset_id

  schema = data.external.policy_rule_results_bq_schema.result.converted_schema
}
