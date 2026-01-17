from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
                    .appName("CPT Codes Ingestion") \
                    .getOrCreate()

# ------------------------
# Google Cloud Storage (GCS) Configuration
# GCS_BUCKET = "test-project-1857-de"
# HOSPITAL_NAME = "hospital-a"
# LANDING_PATH = f"gs://{GCS_BUCKET}/landing/{HOSPITAL_NAME}/"
# ARCHIVE_PATH = f"gs://{GCS_BUCKET}/landing/{HOSPITAL_NAME}/archive/"
# CONFIG_FILE_PATH = f"gs://{GCS_BUCKET}/configs/load_config.csv"

# # BigQuery Configuration
# BQ_PROJECT = "test-project-1857"
# BQ_AUDIT_TABLE = f"{BQ_PROJECT}.temp_dataset.audit_log"
# BQ_LOG_TABLE = f"{BQ_PROJECT}.temp_dataset.pipeline_logs"
# BQ_TEMP_PATH = f"{GCS_BUCKET}/temp/"  

# -------------------------------------
# configure variables
BUCKET_NAME = "test-project-1857-de"
CPT_BUCKET_PATH = f"gs://{BUCKET_NAME}/landing/cptcodes/*.csv"
BQ_TABLE = "test-project-1857.bronze_dataset.cpt_codes"
TEMP_GCS_BUCKET = f"{BUCKET_NAME}/temp/"

# read from cpt
cptcodes_df = spark.read.csv(CPT_BUCKET_PATH, header=True)

# replace spaces with underscore
for col in cptcodes_df.columns:
    new_col = col.replace(" ", "_").lower()
    cptcodes_df = cptcodes_df.withColumnRenamed(col, new_col)

# write to bigquery
(cptcodes_df.write
            .format("bigquery")
            .option("table", BQ_TABLE)
            .option("temporaryGcsBucket", TEMP_GCS_BUCKET)
            .mode("overwrite")
            .save())