# Программа для пометки корпоративных поездок на такси

## Разделы:

### - dal
Тут содержатся все запросы к базе данных. **connection.py** создает соединение, 
остальные файлы соответствуют каждый своей таблице.  
Таблица **rides** была создана на основе полей реестра Яндекса, остальные были сделаны на основе предположений о содержащейся информации.  
  
Также __init__.py в каждой папке необходим для корректного импортирования функций.

В качестве БД используется SQLITE3.

### - logic
Тут содержится вся логика работы. В **algorithm.py** содержится весь алгоритм программы, поэтапно анализирующий поездку. 
В **geocodes.py** содержатся функции для работы с адресами и координатами.

### - schemas
Тут содержатся схемы для всех необходимых запросов в базу данных, созданные на основе pydantic. 
Необходимо для более понятного взаимодействия с данными из БД.

**main.py** создает базу данных, если ее не существует, и запускает программу. В данном случае пока идет только создание, т.к. еще не до конца ясно, куда и как будут отправляться результаты работы программы.
