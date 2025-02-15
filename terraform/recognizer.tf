resource "yandex_storage_bucket" "photos_bucket" {
  bucket = var.photos_bucket
}

resource "yandex_function" "recognizer" {
  name               = var.face_detection_function
  entrypoint         = "recognizer.entrypoint"
  memory             = "256"
  runtime            = "python312"
  user_hash          = data.archive_file.recognizer_source.output_sha512
  service_account_id = yandex_iam_service_account.sa_recognizer.id
  environment = {
    MOUNT_POINT       = yandex_storage_bucket.photos_bucket.bucket
    QUEUE_URL         = yandex_message_queue.crop_tasks_queue.id
    ACCESS_KEY_ID     = yandex_iam_service_account_static_access_key.sa_recognizer_static_key.access_key
    SECRET_ACCESS_KEY = yandex_iam_service_account_static_access_key.sa_recognizer_static_key.secret_key
  }
  content {
    zip_filename = data.archive_file.recognizer_source.output_path
  }
  mounts {
    name = yandex_storage_bucket.photos_bucket.bucket
    mode = "ro"
    object_storage {
      bucket = yandex_storage_bucket.photos_bucket.bucket
    }
  }
}
