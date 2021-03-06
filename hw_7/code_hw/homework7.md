## Домашнее задание №7 - Mock

### Цель домашнего задания:

- Научиться создавать HTTP-клиенты и Mock сервера с использованием различных библиотек и фреймворков;
- Научиться писать тесты, когда необходимо использовать Mock сервера.


### Условия:

Максимум 10 баллов.

Взаимодействие может производиться с теми же сущностями (люди), либо вы можете предложить собственную реализацию.


- Разобраться в библиотеке socket и написать собственный HTTP клиент с помощью библиотеки socket на базе кода из теста **test_by_socket()** из лекции:
  - **переписать и дополнить код клиента**, разнеся его на отдельные классы и методы (запуск, отправка get/post-запросов в мок) - **2 балла**; 
  - **реализовать обработчик ответов** и выводить в лог-файл результат запроса и ответа: код ответа, заголовки, тело ответа - **1 балл**;
  - **тесты (указаны далее) используют http клиент** на библиотеке socket - **2 балла**, если requests - **0.5 балла**.
- Используя mock из лекции, **реализовать обработку PUT (для обновления) и DELETE (для удаления) запросов** - **1 балл**.
- Написать тесты на собственный Mock сервер (необходимое и достаточное количество, чтобы убедиться, что Mock работает корректно) - **2 балла**
- Привести код из лекции в порядок согласно концепциям, рассмотренных на курсе - **2 балла**:
  - все разложено по классам
  - использутся фикстуры и хуки
  - код оптимизирован, убрана копипаста
  - можно трогать код приложения (app/app.py)


#### Сроки сдачи ДЗ

19 мая (включительно)