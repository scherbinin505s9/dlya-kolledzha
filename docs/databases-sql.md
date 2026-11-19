# Базы данных и SQL (ОП.08, МДК.11.01)

## Быстрый старт без установки

SQLite уже есть в Python, ничего ставить не нужно:

```bash
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
sqlite3 test.db          # открыть/создать базу
```

Внутри `sqlite3`: `.tables` — список таблиц, `.schema` — структура, `.quit` — выход.

## PostgreSQL и MySQL в Docker

```bash
# PostgreSQL
docker run -d --name pg -e POSTGRES_PASSWORD=root -p 5432:5432 postgres:16

# MySQL
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 mysql:8

# подключиться
docker exec -it pg psql -U postgres
docker exec -it mysql mysql -uroot -proot
```

Остановить и запустить снова:

```bash
docker stop pg && docker start pg
```

Данные пропадут при `docker rm`. Чтобы сохранить — добавьте `-v pgdata:/var/lib/postgresql/data`.

## Схема для тренировки

```sql
CREATE TABLE groups (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(20) NOT NULL UNIQUE,
    course   INT NOT NULL CHECK (course BETWEEN 1 AND 4)
);

CREATE TABLE students (
    id        SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    birth     DATE,
    group_id  INT REFERENCES groups(id) ON DELETE SET NULL
);

CREATE TABLE subjects (
    id    SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);

CREATE TABLE grades (
    id         SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    value      INT NOT NULL CHECK (value BETWEEN 2 AND 5),
    date       DATE NOT NULL DEFAULT CURRENT_DATE
);
```

В MySQL: `AUTO_INCREMENT`, `INT` вместо `SERIAL`, `ENGINE=InnoDB`.

## Данные

```sql
INSERT INTO groups (name, course) VALUES ('ИС-21', 2), ('ИС-22', 2);
INSERT INTO students (full_name, birth, group_id)
VALUES ('Иванов Иван', '2008-05-14', 1),
       ('Петрова Анна', '2008-11-02', 1);

UPDATE students SET group_id = 2 WHERE id = 2;
DELETE FROM grades WHERE value = 2;
```

## Выборка

```sql
SELECT * FROM students;
SELECT full_name, birth FROM students WHERE group_id = 1 ORDER BY full_name;
SELECT DISTINCT group_id FROM students;
SELECT * FROM students ORDER BY birth DESC LIMIT 5;

-- агрегаты
SELECT COUNT(*) AS всего FROM students;
SELECT group_id, COUNT(*) AS студентов FROM students GROUP BY group_id;
SELECT group_id, AVG(value) AS средний FROM grades GROUP BY group_id HAVING AVG(value) > 4;
```

## JOIN

```sql
-- студенты с названием группы
SELECT s.full_name, g.name AS группа
FROM students s
JOIN groups g ON g.id = s.group_id;

-- все группы, даже пустые
SELECT g.name, COUNT(s.id) AS студентов
FROM groups g
LEFT JOIN students s ON s.group_id = g.id
GROUP BY g.name;

-- оценки студентов с предметами
SELECT s.full_name, sub.title, gr.value, gr.date
FROM grades gr
JOIN students s ON s.id = gr.student_id
JOIN subjects sub ON sub.id = gr.subject_id
ORDER BY s.full_name, sub.title;
```

| JOIN | Что вернёт |
|---|---|
| `INNER JOIN` | только совпадающие строки |
| `LEFT JOIN` | все строки левой таблицы + совпадения |
| `RIGHT JOIN` | все строки правой таблицы + совпадения |
| `FULL JOIN` | все строки обеих таблиц |

## Подзапросы и представления

```sql
-- студенты со средним баллом выше общего среднего
SELECT full_name
FROM students
WHERE id IN (
    SELECT student_id FROM grades GROUP BY student_id
    HAVING AVG(value) > (SELECT AVG(value) FROM grades)
);

-- представление
CREATE VIEW student_avg AS
SELECT s.full_name, ROUND(AVG(g.value), 2) AS avg_grade
FROM students s
LEFT JOIN grades g ON g.student_id = s.id
GROUP BY s.full_name;

SELECT * FROM student_avg WHERE avg_grade < 4;
```

## Изменение структуры

```sql
ALTER TABLE students ADD COLUMN email VARCHAR(100);
ALTER TABLE students DROP COLUMN email;
CREATE INDEX idx_students_group ON students(group_id);
DROP TABLE grades;
```

## Транзакции

```sql
BEGIN;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;    -- или ROLLBACK, если что-то пошло не так
```

## Нормализация (спросят на защите)

| Форма | Требование | Плохой пример |
|---|---|---|
| 1НФ | атомарные значения, нет списков в ячейке | `subjects = 'математика, физика'` |
| 2НФ | нет частичной зависимости от составного ключа | оценка зависит только от студента |
| 3НФ | нет транзитивных зависимостей | название группы хранится и в students, и в groups |

Практическое правило: одна сущность — одна таблица, связи — через внешние ключи.

## ER-диаграмма

Сущности — прямоугольники, атрибуты — овалы, связи — ромбы.
Связи: 1:1, 1:N, M:N (M:N всегда разбивается промежуточной таблицей).
Рисовать: draw.io, dbdiagram.io, MySQL Workbench.

## Резервные копии

```bash
# PostgreSQL
docker exec pg pg_dump -U postgres postgres > backup.sql
docker exec -i pg psql -U postgres postgres < backup.sql

# MySQL
docker exec mysql mysqldump -uroot -proot mysql > backup.sql
```

## Типовые задания

1. Вывести всех студентов заданной группы.
2. Найти средний балл по каждому предмету.
3. Найти студентов без оценок.
4. Вывести лучшего студента по среднему баллу.
5. Посчитать количество оценок «5» по каждому предмету.
6. Создать представление «ведомость» с итоговой оценкой.
7. Написать запрос с `HAVING` и объяснить, чем он отличается от `WHERE`.

## Частые ошибки

| Ошибка | Причина | Решение |
|---|---|---|
| `column ... must appear in GROUP BY` | в `SELECT` столбец, которого нет в группировке | добавить в `GROUP BY` или обернуть в агрегат |
| `violates foreign key constraint` | ссылка на несуществующую строку | сначала вставить родителя |
| `duplicate key value` | повтор значения в `UNIQUE`/`PRIMARY KEY` | `ON CONFLICT DO NOTHING` или проверить данные |
| `syntax error at or near` | лишняя запятая или кавычки | проверить запрос по частям |
| `relation does not exist` | не та база / не создана таблица | `\dt` в psql, `SHOW TABLES` в MySQL |
| `permission denied` | нет прав | работать под владельцем БД |
| Пропали данные | контейнер удалён без тома | использовать `-v` |
