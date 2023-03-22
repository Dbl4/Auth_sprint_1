# Задание на третий модуль

[https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/64127/topics/a7f525a1-6b75-4d7e-912a-c83b5681867b/lessons/ccf14121-12d4-4f07-8514-925124c921b2/](https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/64127/topics/a7f525a1-6b75-4d7e-912a-c83b5681867b/lessons/ccf14121-12d4-4f07-8514-925124c921b2/)

## Критерии готовности

Анонимный пользователь может:

- Создать аккаунт, если выбранный email ещё не зарегистрирован в системе.
- Зарегистрироваться через социальную сеть.
- Войти в свой аккаунт по логину и паролю.
- Войти в свой аккаунт через социальную сеть с использованием OAuth 2.0.

Авторизированный пользователь может:

- Изменить свои личные данные — логин или пароль.
- Просмотреть историю входов в аккаунт.
- Посмотреть связанные аккаунты в социальных сетях.
- Открепить аккаунт социальной сети.

## Пользовательский интерфейс

- Регистрация аккаунта при помощи email и пароля:

![https://pictures.s3.yandex.net/resources/S1_1_Practix_auth_1606729639.jpg](https://pictures.s3.yandex.net/resources/S1_1_Practix_auth_1606729639.jpg)

- Изменение пароля:

![https://pictures.s3.yandex.net/resources/S1_4_Practix_auth_1606729666.jpg](https://pictures.s3.yandex.net/resources/S1_4_Practix_auth_1606729666.jpg)

- Личный кабинет:

![https://pictures.s3.yandex.net/resources/S1_2_Practix_auth_1606729712.jpg](https://pictures.s3.yandex.net/resources/S1_2_Practix_auth_1606729712.jpg)

## Требования к объёму данных

- 500 000+ пользователей;
- 500 000+ связанных аккаунтов;
- 1 000 000+ записей о входах в аккаунт.

# Проектное задание шестого спринта

[Проектное задание шестого спринта](https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/64127/topics/0502debf-9247-45f5-936f-5a838e72095c/lessons/2c8e6cb7-90ed-4edd-b47e-a592c74b9703/)

К концу спринта у вас должен получиться сервис авторизации с системой ролей, написанный на Flask с использованием gevent. Первый шаг к этому — проработать и описать архитектуру вашего сервиса. Это значит, что перед тем, как приступить к разработке, нужно составить план действий: из чего будет состоять сервис, каким будет его API, какие хранилища он будет использовать и какой будет его схема данных. Описание нужно обсудить с наставником. Вам предстоит выбрать, какой метод организации доступов использовать для онлайн-кинотеатра, и систему прав, которая позволит ограничить доступ к ресурсам.

Для описания API рекомендуем использовать [OpenAPI](https://editor.swagger.io/). Обязательно продумайте и опишите обработку ошибок. Например, как отреагирует ваш API, если обратиться к нему с истёкшим токеном? Будет ли отличаться ответ API, если передать ему токен с неверной подписью? А если имя пользователя уже занято? Документация вашего API должна включать не только ответы сервера при успешном завершении запроса, но и понятное описание возможных ответов с ошибкой.

После обсуждения с наставником вы можете приступать к программированию.

Для успешного завершения первой части модуля в вашем сервисе должны быть реализованы API для аутентификации и система управления ролями. Роли понадобятся, чтобы ограничить доступ к некоторым категориям фильмов. Например, «Фильмы, выпущенные менее 3 лет назад» могут просматривать только пользователи из группы 'subscribers'.

## API для сайта и личного кабинета

- регистрация пользователя;
- вход пользователя в аккаунт (обмен логина и пароля на пару токенов: JWT-access токен и refresh токен);
- обновление access-токена;
- выход пользователя из аккаунта;
- изменение логина или пароля (с отправкой email вы познакомитесь в следующих модулях, поэтому пока ваш сервис должен позволять изменять личные данные без дополнительных подтверждений);
- получение пользователем своей истории входов в аккаунт;

## API для управления доступами

- CRUD для управления ролями:
    - создание роли,
    - удаление роли,
    - изменение роли,
    - просмотр всех ролей.
- назначить пользователю роль;
- отобрать у пользователя роль;
- метод для проверки наличия прав у пользователя.

## Подсказки

1. Продумайте, как реализовать работу с анонимными пользователями: они могут выполнять только те действия, для которых не нужны особые права.
2. Метод проверки авторизации будет всегда нужен пользователям. Ходить каждый раз в БД — не очень хорошая идея. Подумайте, как улучшить производительность системы.
3. Добавьте консольную команду для создания суперпользователя, которому всегда разрешено делать все действия в системе.
4. Чтобы упростить себе жизнь с настройкой суперпользователя, продумайте, как сделать так, чтобы при авторизации ему всегда отдавался успех при всех запросах.
5. Для реализации ограничения по фильмам подумайте о присвоении им какой-либо метки. Это потребует небольшой доработки ETL-процесса.

## Дополнительное задание

Реализуйте кнопку «Выйти на остальных устройствах», не прибегая к хранению в БД активных access-токенов.

## Напоминаем о требованиях к качеству

Перед тем как сдать ваш код на проверку, убедитесь, что:

- Код написан по правилам pep8: при запуске [линтера](https://semakin.dev/2020/05/python_linters/) в консоли не появляется предупреждений и возмущений;
- Все ключевые методы покрыты тестами: каждый ответ каждой ручки API и важная бизнес-логика тщательно проверены;
- У тестов есть понятное описание, что именно проверяется внутри. Используйте [pep257](https://www.python.org/dev/peps/pep-0257/);
- Заполните README.md так, чтобы по нему можно было легко познакомиться с вашим проектом. Добавьте короткое, но ёмкое описание проекта. По пунктам опишите как запустить приложения с нуля, перечислив полезные команды. Упомяните людей, которые занимаются проектом и их роли. Ведите changelog: описывайте, что именно из задания модуля уже реализовано в вашем сервисе и пополняйте список по мере развития.
- Вы воспользовались лучшими практиками описания конфигурации приложений из урока.

# Проектное задание седьмого спринта

[Проектное задание седьмого спринта](https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/108729/topics/a5022019-8fe6-438a-9fce-9d0d2acbf902/lessons/5d652865-4bd6-4822-b6e3-35847bf53023/)

Добавьте вход через социальные сервисы и упростите регистрацию и аутентификацию пользователей в Auth-сервисе. Список сервисов должен соответствовать целевой аудитории онлайн-кинотеатра — подумайте, какими социальными сервисами они пользуются. Например, использовать [OAuth от Github](https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps) — не самая удачная идея. Ваши пользователи – не разработчики и вряд ли имеют аккаунт на Github. А вот добавить VK, Google, Yandex или Mail будет хорошей идеей.

Вам не нужно делать фронтенд в этой задаче и реализовывать собственный сервер OAuth. Нужно реализовать протокол со стороны потребителя.

Информация по OAuth у разных поставщиков данных:

- [Yandex](https://yandex.ru/dev/oauth/?turbo=true),
- [VK](https://vk.com/dev/access_token),
- [Google](https://developers.google.com/identity/protocols/oauth2),
- [Mail](https://api.mail.ru/docs/guides/oauth/).

## Дополнительное задание

Реализуйте возможность открепить аккаунт в соцсети от личного кабинета.

Решение залейте в репозиторий текущего спринта и отправьте на ревью.