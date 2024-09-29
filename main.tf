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
      cluster_name = "liquor-store-etl-workflow-cluster"
      config {
        gce_cluster_config {
          zone = "us-central1-a"
        }
        master_config {
          num_instances = 1
          machine_type = "n1-standard-2"  
          disk_config {
            boot_disk_type   = "pd-ssd"
            boot_disk_size_gb = 30  
          }
        }
        worker_config {
          num_instances = 3
          machine_type = "n1-standard-2" 
          disk_config {
            boot_disk_size_gb = 30  
            num_local_ssds    = 2
          }
        }
        secondary_worker_config {
          num_instances = 2
        }
        software_config {
          image_version = "2.0.35-debian10"

          # Include the BigQuery connector using spark.jars
          properties = {
            "spark.jars" = "gs://spark-lib/bigquery/spark-bigquery-latest.jar"
          }
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
