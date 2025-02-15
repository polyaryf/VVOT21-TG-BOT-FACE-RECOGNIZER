resource "yandex_function" "bot" {
  name               = var.bot_function
  entrypoint         = "bot.entrypoint"
  memory             = "128"
  runtime            = "python312"
  user_hash          = data.archive_file.bot_source.output_sha512
  service_account_id = yandex_iam_service_account.sa_bot.id
  environment = {
    TELEGRAM_BOT_TOKEN = var.tg_bot_key
    PHOTOS_MOUNT_POINT = yandex_storage_bucket.photos_bucket.bucket
    FACES_MOUNT_POINT  = yandex_storage_bucket.faces_bucket.bucket
    API_GATEWAY_URL    = "https://${yandex_api_gateway.api_gw.domain}"
  }
  content {
    zip_filename = data.archive_file.bot_source.output_path
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
