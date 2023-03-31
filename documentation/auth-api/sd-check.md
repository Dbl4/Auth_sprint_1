```mermaid
---
title: Запрос контента (SD)
---

sequenceDiagram
    actor Frontend
    participant FastAPI
    participant Flask

    Frontend ->> FastAPI: access token
    FastAPI ->> Flask: GET /users/{user_id}/check/(access token)

    alt access-токен просрочен (time > exp)
        Flask --) FastAPI: 403 Forbidden
        FastAPI ->> Flask: POST /refresh/
        Flask --) FastAPI: новые токены
        FastAPI --) Frontend: ok
    else user_id или подпись неверные
        Flask --) FastAPI: 401 Unauthorized
        FastAPI --) Frontend: 401 Unauthorized
    else
        Flask --) FastAPI: 200
        FastAPI --) Frontend: ok
    end
```

При получении запроса прикладной сервис проверяет приложенный 
к запросу access токен, делая запрос к сервису Auth API. Auth API
проверяет идентификатор пользователя и подпись токена не совершая запрос
к базе данных, что снижает нагрузку на систему.
