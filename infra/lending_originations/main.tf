


resource "google_bigquery_dataset" "lending_originations" {
  dataset_id = "lending_originations"
  location   = "EU"
}



data "google_project" "project" {
}
