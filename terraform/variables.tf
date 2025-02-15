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


# Функции

variable "face_detection_function" {
  type        = string
  description = "функция обнаружения лиц"
  default     = "vvot21-face-detection"
}

variable "face_cut_function" {
  type        = string
  description = "Название обрезания лиц"
  default     = "vvot21-face-cut"
}


variable "bot_function" {
  type        = string
  description = "функции тг бота"
  default     = "vvot21-boot"
}

# Бакеты

variable "photos_bucket" {
  type        = string
  description = "бакет для оригинальных фотографий"
  default     = "vvot21-photo"
}

variable "faces_bucket" {
  type        = string
  description = "бакет для вырезанных фотографий лиц"
  default     = "vvot21-faces"
}
# Сервисные аккаунты

variable "sa_key_file_path" {
  type        = string
  description = "путь для провайдера чтобы искать авторизованный ключ"
  default     = "~/.yc-keys/key.json"
}
