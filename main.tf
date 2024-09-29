provider "google" {
  project = "liqour-store-etl"
  region  = "us-central1"
}

# Create a GCS bucket
resource "google_storage_bucket" "data_bucket" {
  name     = "liquor-store-bucket"
  location = "us-central1"

  lifecycle {
    ignore_changes = [name]
  }
}

# Create a Dataproc workflow template
resource "google_dataproc_workflow_template" "template" {
  name     = "liquor-store-etl-workflow"
  location = "us-central1"

  placement {
    managed_cluster {
      cluster_name = "liquor-store-etl-workflow-jobs"
      config {
        gce_cluster_config {
          zone = "us-central1-a"
        }
        master_config {
          machine_type = "n1-standard-2"
          disk_config {
            boot_disk_type   = "pd-balanced"
            boot_disk_size_gb = 50
          }
        }
        worker_config {
          num_instances = 2
          machine_type  = "n1-standard-2"
          disk_config {
            boot_disk_type   = "pd-balanced"
            boot_disk_size_gb = 50
          }
        }
        software_config {
          # Default
        }
      }
    }
  }

  # PySpark Job in Dataproc Workflow
  jobs {
    step_id = "job-a722fda0"
    pyspark_job {
      main_python_file_uri = "gs://${google_storage_bucket.data_bucket.name}/main.py"
      jar_file_uris = ["gs://spark-lib/bigquery/spark-bigquery-latest.jar"]
    }
  }
}

