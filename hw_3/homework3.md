## Домашнее задание №3: API

#### Цель домашнего задания

  * Научиться тестировать REST API-сервисы


#### Задача
* Тестирование портала https://target.my.com/
* Настроить окружение для запуска API тестов
* API тесты должны запускаться через марк -m API
 
    API (7 баллов):
     * Написать API клиент, который будет иметь возможность авторизовываться на портале (3 балла)
     * Написать тест на создание кампании любого типа через API, кампания после теста должна удалиться автоматически (2 балла) 
     * Написать тест на создание сегмента через API и проверку что сегмент создан (1 балл)
     * Написать тест на удаление сегмента через API (1 балл)


#### Самостоятельное задание, без добавления кода в ДЗ и сдачи на проверку
* Адаптировать UI тесты из ДЗ №2 под использование API клиента в тех местах, где это возможно и необходимо:
    * Авторизация
    * Создание сегмента
    * etc


#### Советы
  * Тесты *НЕ* должны быть зависимыми
  * Все тесты *ДОЛЖНЫ* проходить
  * Тесты *ОБЯЗАТЕЛЬНО* должны что-то проверять. Например если мы что-то создали - необходимо проверить что оно создалось
  * Тесты *ДОЛЖНЫ* уметь запускаться параллельно и проходить в параллельном режиме (не конфликтовать)
  * Тесты *ДОЛЖНЫ* уметь запускаться несколько раз подряд
 
#### Срок сдачи ДЗ

  До 19 апреля (включительно)