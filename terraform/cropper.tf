resource "yandex_storage_bucket" "faces_bucket" {
  bucket = var.faces_bucket
}

resource "yandex_function" "cropper" {
  name               = var.face_cut_function
  entrypoint         = "cropper.entrypoint"
  memory             = "128"
  runtime            = "python312"
  user_hash          = data.archive_file.cropper_source.output_sha512
  service_account_id = yandex_iam_service_account.sa_cropper.id
  environment = {
    PHOTOS_MOUNT_POINT = yandex_storage_bucket.photos_bucket.bucket
    FACES_MOUNT_POINT  = yandex_storage_bucket.faces_bucket.bucket
    ACCESS_KEY_ID      = yandex_iam_service_account_static_access_key.sa_cropper_static_key.access_key
    SECRET_ACCESS_KEY  = yandex_iam_service_account_static_access_key.sa_cropper_static_key.secret_key
  }
  content {
    zip_filename = data.archive_file.cropper_source.output_path
  }
  mounts {
    name = yandex_storage_bucket.photos_bucket.bucket
    mode = "ro"
    object_storage {
      bucket = yandex_storage_bucket.photos_bucket.bucket
    }
  }
  mounts {
    name = yandex_storage_bucket.faces_bucket.bucket
    mode = "rw"
    object_storage {
      bucket = yandex_storage_bucket.faces_bucket.bucket
    }
  }
}
