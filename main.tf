provider "google" {
  project = "liqour-store-etl"
  region  = "europe-west1"
}

# Create a GCS bucket
resource "google_storage_bucket" "data_bucket" {
  name     = "liquor-store-data-bucket"
  location = "EU"
}

# # Create a Dataproc cluster
# resource "google_dataproc_cluster" "dataproc_cluster" {
#   name       = "liquor-store-dataproc-cluster"
#   region     = "europe-west1"
#   num_workers = 2
# 
#   cluster_config {
#     master_config {
#       num_instances = 1
#       machine_type  = "n1-standard-1"
#     }
#     worker_config {
#       num_instances = 2
#       machine_type  = "n1-standard-1"
#     }
#   }
# }
# 
# # Create a BigQuery dataset
# resource "google_bigquery_dataset" "bq_dataset" {
#   dataset_id = "liquor_store_dataset"
#   location   = "EU"
# }
