```mermaid
---
title: Аутентификация (SD)
---

sequenceDiagram
    actor Frontend
    participant Flask

    Frontend ->> Flask: POST /auth/login/(login, password, user-agent, user-ip)

    alt Пароль неверный
        Flask -) Frontend: 403
    else
        Flask ->> Flask: Записать auth-history
        Flask ->> Flask: Сгенерировать токены
        Flask ->> Flask: Сохранить refresh-токен
        Flask --) Frontend: access и refresh токены
    end
```
