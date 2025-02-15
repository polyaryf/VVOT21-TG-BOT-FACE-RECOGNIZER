# Приватное

variable "cloud_id" {
  type        = string
  description = "id облака"
}

variable "folder_id" {
  type        = string
  description = "id каталога"
}

variable "tg_bot_key" {
  type        = string
  description = "токен для доступа к тг боту"
}

# Сервисные аккаунты

variable "sa_key_file_path" {
  type        = string
  description = "путь для провайдера чтобы искать авторизованный ключ"
  default     = "~/.yc-keys/key.json"
}
