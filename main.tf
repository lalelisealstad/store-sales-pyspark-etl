provider "google" {
  project = "liqour-store-etl"
  region  = "europe-west1"
}

# Create a GCS bucket
resource "google_storage_bucket" "data_bucket" {
  name     = "liquor-store-data-bucket"
  location = "EU"
}

# Create a Dataproc cluster
resource "google_dataproc_cluster" "dataproc_cluster" {
  name       = "liquor-store-dataproc-cluster"
  region     = "europe-west1"
  num_workers = 2

  cluster_config {
    master_config {
      num_instances = 1
      machine_type  = "n1-standard-1"
    }
    worker_config {
      num_instances = 2
      machine_type  = "n1-standard-1"
    }

    # Initialization actions to install BigQuery connector
    initialization_actions {
      executable_file = "gs://dataproc-initialization-actions/bigquery/connectors.sh"
    }
  }
}




# Create a BigQuery dataset
resource "google_bigquery_dataset" "bq_dataset" {
  dataset_id = "liquor_store_dataset"
  location   = "EU"
}

# GCS bucket for storing the PySpark job code 
resource "google_storage_bucket_object" "pyspark_job" {
  name   = "main.py"
  bucket = google_storage_bucket.data_bucket.name
}



resource "google_dataproc_job" "pyspark_job" {
  region      = google_dataproc_cluster.dataproc_cluster.region
  cluster     = google_dataproc_cluster.dataproc_cluster.name
  pyspark_job {
    main_python_file_uri = "gs://${google_storage_bucket.data_bucket.name}/main.py"
  }
}
