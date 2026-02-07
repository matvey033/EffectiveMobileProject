# Effective Mobile Project – Система аутентификации и авторизации

## 1. Схема пользователей и ролей
Users
-------------------------------
id | email | first_name | last_name | patronymic | role_id | is_active | is_staff | is_superuser

Role
-------------------------------
id | name      | description

1  | admin     | полный доступ

2  | manager   | доступ к заказам и продуктам

3  | user      | обычный пользователь

BusinessElement
-------------------------------
id | name

1  | users

2  | orders

3  | products

AccessRoleRule
-------------------------------
role_id | element_id | read | read_all | create | update | update_all | delete | delete_all

1       | 1          | True | True     | True   | True   | True       | True   | True

2       | 2          | True | False    | True   | True   | False      | False  | False

3       | 2          | True | False    | True   | False  | False      | False  | False


### Описание:
- Users – учетные записи пользователей.
- Role – роли пользователей.
- BusinessElement – объекты приложения, к которым применяются права.
- AccessRoleRule – права роли на объекты: чтение, создание, редактирование, удаление.


## 2. Механизм аутентификации и авторизации
1. Пользователь логинится через /login/ → получает JWT токен.
2. Токен передается в заголовке запроса: Authorization: Bearer <JWT_TOKEN>
3. JWTAuthentication проверяет токен и извлекает пользователя. 
4. RolePermission проверяет права доступа по таблице AccessRoleRule.
5. Если прав нет → возвращается ошибка:
- 401 Unauthorized – если токен отсутствует или недействителен
- 403 Forbidden – если пользователь не имеет прав на ресурс

## 3. Примеры запросов
### 3.1 Регистрация
POST http://127.0.0.1:8000/auth/register/

Body (JSON):

    "email": "user@test.com",
    "password": "1234",
    "password_repeat": "1234",
    "first_name": "User",
    "last_name": "Userovich"

Ответ:

    "message": "Пользователь создан"

### 3.2 Вход
POST http://127.0.0.1:8000/auth/login/

Body (JSON):

    "email": "user@test.com",
    "password": "1234"

Ответ:

    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."


### 3.3 Получение mock-объектов (JWT обязателен)
GET http://127.0.0.1:8000/auth/objects/

Headers:

    Authorization: Bearer <JWT_TOKEN>

Ответ:
    
    {"id": 1, "name": "Объект A"},
    {"id": 2, "name": "Объект B"}


### 3.4 Обновление профиля
PUT http://127.0.0.1:8000/auth/update/

Headers:

    Authorization: Bearer <JWT_TOKEN>

Body (JSON):

    "first_name": "NewName",
    "last_name": "NewLastName",
    "patronymic": "NewPatronymic"

Ответ:
    
    "message": "Профиль обновлен"


### 3.5 Удаление пользователя
DELETE http://127.0.0.1:8000/auth/delete/

Headers:

    Authorization: Bearer <JWT_TOKEN>

Ответ:
    
    "message": "Пользователь удален"