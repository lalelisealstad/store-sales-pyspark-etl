provider "google" {
  project = "liqour-store-etl"
  region  = "us-central1"
}

# Create a GCS bucket
resource "google_storage_bucket" "data_bucket" {
  name     = "liquor-store-data-bucket"
  location = "us-central1"  # Changed to be consistent with the region
}

# Create a Dataproc workflow template
resource "google_dataproc_workflow_template" "template" {
  name     = "liquor-etl-workflow"
  location = "us-central1"

  placement {
    managed_cluster {
      cluster_name = "liquor-etl-workflow-cluster"
      config {
        gce_cluster_config {
          zone = "us-central1-a"
        }
        master_config {
          num_instances = 1
          machine_type = "n1-standard-1"
          disk_config {
            boot_disk_type   = "pd-ssd"
            boot_disk_size_gb = 20
          }
        }
        worker_config {
          num_instances = 3
          machine_type = "n1-standard-2"
          disk_config {
            boot_disk_size_gb = 15
            num_local_ssds    = 2
          }
        }
        secondary_worker_config {
          num_instances = 2
        }
        software_config {
          image_version = "2.0.35-debian10"
        }
      }
    }
  }

  # PySpark Job in Dataproc Workflow
  jobs {
    step_id = "pyspark-job"
    pyspark_job {
      main_python_file_uri = "gs://${google_storage_bucket.data_bucket.name}/main.py"
    }
  }
}