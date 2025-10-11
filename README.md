# Social-network

Современный чат-сервер с социальными возможностями, построенный на Django с WebSocket поддержкой.

## 🚀 Возможности

### Основной функционал
- **🔐 Аутентификация**: JWT токены, регистрация и вход в систему
- **💬 Чаты**: Комнаты с WebSocket подключением в реальном времени
- **👥 Социальные функции**: Друзья, подписки, заявки в друзья
- **📱 Посты**: Создание постов с изображениями, лайки и комментарии
- **📰 Лента новостей**: Персонализированная лента от друзей и подписок
- **🔔 Уведомления**: Система уведомлений с Celery
- **🌐 REST API**: Полный API для всех функций

### Технические особенности
- **WebSocket**: Реальное время для чата
- **Фоновые задачи**: Celery для обработки уведомлений
- **Медиа файлы**: Загрузка и обработка изображений
- **Масштабируемость**: Docker контейнеризация

## 🛠 Технологии

- **Django 5.2** - веб-фреймворк
- **Django Channels** - WebSocket поддержка
- **Django REST Framework** - API
- **PostgreSQL** - база данных
- **Redis** - кэш и брокер сообщений
- **Celery** - фоновые задачи
- **JWT** - аутентификация
- **Docker** - контейнеризация

## 📦 Установка и запуск

### Предварительные требования
- Docker и Docker Compose
- Python 3.12+ (для разработки)

### Быстрый запуск

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd simpleChatServer
```

2. **Создайте файл переменных окружения:**
```bash
cp .env.example .env
```

3. **Настройте переменные в `.env`:**
```env
# Database Configuration
DB_HOST=database
DB_NAME=dbname
DB_USER=dbuser
DB_PASS=dbpass

# Email Configuration (для уведомлений)
EMAIL_HOST_USER=your-email@gmail.com
GMAIL_HOST_PASSWORD=your-app-password

# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Celery Configuration
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

4. **Запустите все сервисы:**
```bash
docker-compose up --build
```

5. **Выполните миграции:**
```bash
docker-compose exec web python manage.py migrate
```

6. **Создайте суперпользователя:**
```bash
docker-compose exec web python manage.py createsuperuser
```

7. **Откройте приложение:**
- API: http://localhost:8000
- Админка: http://localhost:8000/admin
- WebSocket: ws://localhost:8000/ws/chat/{room_name}/

## 🔧 API Endpoints

### Аутентификация
- `POST /api/token/` - Получение JWT токена
- `POST /api/token/refresh/` - Обновление токена

### Пользователи
- `GET /api/users/` - Список пользователей
- `GET /api/users/{id}/` - Информация о пользователе
- `POST /api/users/{id}/friends/` - Добавить в друзья
- `DELETE /api/users/{id}/friends/` - Удалить из друзей
- `POST /api/users/{id}/friend_request/` - Отправить заявку в друзья
- `DELETE /api/users/{id}/friend_request/` - Отозвать заявку

### Комнаты и чат
- `GET /api/rooms/` - Список комнат
- `POST /api/rooms/` - Создать комнату
- `GET /api/rooms/user_room/` - Мои комнаты
- `GET /api/rooms/{id}/messages/` - Сообщения комнаты
- `WS /ws/chat/{room_name}/` - WebSocket для чата

### Посты
- `GET /api/posts/` - Список постов
- `POST /api/posts/` - Создать пост
- `GET /api/feed/` - Лента новостей
- `POST /api/posts/{id}/like/` - Лайк поста
- `DELETE /api/posts/{id}/like/` - Убрать лайк

## 🏗 Структура проекта

```
chatserver/
├── account/              # Управление пользователями
│   ├── models.py         # Модель CustomUser
│   ├── views.py          # Регистрация и вход
│   └── forms.py          # Формы аутентификации
├── api/                  # REST API
│   ├── views.py          # API представления
│   ├── serializers.py    # Сериализаторы
│   └── urls.py           # API маршруты
├── chat/                 # Чат функционал
│   ├── models.py         # Room, Message, Post, Comment
│   ├── consumers.py      # WebSocket потребители
│   ├── routing.py        # WebSocket маршруты
│   └── services.py       # Бизнес-логика
├── notification/         # Система уведомлений
│   ├── models.py         # Модель Notification
│   ├── tasks.py          # Celery задачи
│   └── signals.py        # Django сигналы
└── chatserver/          # Настройки проекта
    ├── settings.py       # Конфигурация
    ├── urls.py          # Основные маршруты
    └── asgi.py          # ASGI конфигурация
```

## 🐳 Docker

Проект полностью контейнеризован:

```bash
# Запуск всех сервисов
docker-compose up

# Запуск в фоне
docker-compose up -d

# Пересборка
docker-compose up --build

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f

# Выполнение команд Django
docker-compose exec web python manage.py <command>
```

## 🔧 Разработка

### Локальная разработка

1. **Установите зависимости:**
```bash
cd chatserver
pip install -r ../requirements.txt
```

2. **Настройте базу данных:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

3. **Запустите сервер:**
```bash
python manage.py runserver
```

4. **Запустите Celery worker:**
```bash
celery -A celery_app.app worker --loglevel=info
```

## 📊 Модели данных

### CustomUser
- `username`, `email` - основные поля
- `phone_number` - номер телефона
- `friends` - друзья (ManyToMany)
- `followers` - подписчики (ManyToMany)
- `friend_requests` - заявки в друзья (ManyToMany)

### Room
- `name` - название комнаты
- `owner` - владелец комнаты
- `users` - участники комнаты
- `created_at` - дата создания

### Message
- `room` - комната
- `text` - текст сообщения
- `author` - автор сообщения
- `created_at` - дата создания

### Post
- `text` - текст поста
- `owner` - автор поста
- `image` - изображение
- `likes` - лайки
- `created_at` - дата создания

### Comment
- `com` - текст комментария
- `author` - автор комментария
- `post` - пост
- `created_at` - дата создания

### Notification
- `recipient` - получатель
- `sender` - отправитель
- `notification_type` - тип уведомления
- `message` - текст уведомления
- `is_read` - прочитано ли
- `created_at` - дата создания

## 🔒 Безопасность

- **JWT аутентификация** - безопасные токены
- **CSRF защита** - защита от CSRF атак
- **Валидация данных** - проверка всех входных данных
- **Хеширование паролей** - безопасное хранение паролей
- **CORS настройки** - контроль доступа

## 🚀 Деплой

### Продакшен настройки

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port
```

### Переменные окружения для продакшена

- `SECRET_KEY` - секретный ключ Django
- `DEBUG` - режим отладки (False для продакшена)
- `ALLOWED_HOSTS` - разрешенные хосты
- `DATABASE_URL` - URL базы данных
- `REDIS_URL` - URL Redis
- `EMAIL_HOST_USER` - email для уведомлений
- `GMAIL_HOST_PASSWORD` - пароль приложения

## 📈 Мониторинг

### Логи
```bash
# Просмотр логов всех сервисов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f web
docker-compose logs -f worker
```

### Здоровье системы
- Проверка статуса: `docker-compose ps`
- Использование ресурсов: `docker stats`
- Мониторинг базы данных: подключение к PostgreSQL

## 🎯 Планы развития

- [ ] Голосовые сообщения
- [ ] Видеозвонки
- [ ] Чат-бот с ИИ
- [ ] Мобильное приложение
- [ ] Система групп
- [ ] Аналитика пользователей
- [ ] Push-уведомления
- [ ] Шифрование сообщений

---
