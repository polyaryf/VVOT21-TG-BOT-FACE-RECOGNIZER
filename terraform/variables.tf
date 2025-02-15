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

# Очередь

variable "face_cut_queue" {
  type        = string
  description = "очередь для таско по обрезке лиц"
  default     = "vvot21-task"
}

# Тригеры

variable "face_detection_trigger" {
  type        = string
  description = "триггер обнаружения лиц"
  default     = "vvot21-photo"
}

variable "face_cut_trigger" {
  type        = string
  description = "триггер обрезки лиц"
  default     = "vvot21-task"
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

# Шлюз

variable "api_gateway" {
  type        = string
  description = "Название апи шлюза для фотографий лиц"
  default     = "vvot21-apigw"
}

# Сервисные аккаунты

variable "sa_key_file_path" {
  type        = string
  description = "путь для провайдера чтобы искать авторизованный ключ"
  default     = "~/.yc-keys/key.json"
}

variable "sa_face_detection" {
  type        = string
  description = "сервисный аккаунт для функции обнаружения лиц"
  default     = "vvot21-sa-recognizer"
}

variable "sa_face_cut" {
  type        = string
  description = "сервисный аккаунт для функции вырезания лиц"
  default     = "vvot21-sa-cropper"
}

variable "sa_bot" {
  type        = string
  description = "сервисный аккаунт для работы с тг ботом"
  default     = "vvot21-sa-bot"
}