# 🛒 E-Commerce Data Pipeline & DWH (PostgreSQL + Airflow + Pandas)

Эндовый пет-проект по инженерии данных: эмуляция работы интернет-магазина, проектирование реляционной БД, создание аналитических витрин и оркестрация ETL-пайплайна с сохранением отчетов в колоночный формат Parquet.

---

## 🛠 Технологический стек

* **Инфраструктура:** Docker, Docker Compose
* **Базы данных & DWH:** PostgreSQL (OLTP schema + Analytical Views)
* **Язык & Библиотеки:** Python 3.10+, Pandas, SQLAlchemy, psycopg2, Faker, PyArrow
* **Оркестрация:** Apache Airflow 2.8+
* **Инструменты:** DBeaver, PyCharm

---

## 🏗 Архитектура пайплайна
[ Faker Script ] ──> [ PostgreSQL (OLTP) ] ──> [ SQL View (Data Mart) ]
│
(Airflow DAG)
│
▼
[ Output Files (.parquet / .csv) ] <── [ Python ETL (Pandas) ]
1. **Генерация данных (`generate_data.py`):** Скрипт генерирует реалистичные данные о клиентах, товарах и заказах с помощью библиотеки `Faker` и загружает их в Postgres.
2. **Аналитический слой (DWH):** В БД создаются таблицы с реляционными связями (`FK`/`PK`) и витрина данных `dm_category_sales` на основе SQL-запроса с `JOIN` и группировками.
3. **ETL-процесс (`etl_pipeline.py`):** Скрипт извлекает данные из витрины, рассчитывает бизнес-метрику (долю категории в общей выручке в %) и экспортирует итоговый отчёт в CSV и **Parquet** (для высоконагруженной аналитики).
4. **Оркестрация (Airflow):** Вся цепочка от проверки доступности БД до выгрузки отчета обернута в DAG и выполняется по расписанию.

---

## 📊 Структура базы данных (Схема)

БД `ecommerce` состоит из следующих сущностей:
* `users` — профили пользователей.
* `categories` — категории товаров.
* `products` — товары (связь 1:N с категориями).
* `orders` — заказы (связь N:1 с пользователями).
* `order_items` — позиции внутри заказов.
* `dm_category_sales` — аналитическая витрина, агрегирующая продажи по категориям.

---

## 🚀 Как запустить проект локально

### 1. Клонирование репозитория
```bash
git clone [https://github.com/Vladislav_DE/de-ecommerce-pipeline.git](https://github.com/YOUR_USERNAME/de-ecommerce-pipeline.git)
cd de-ecommerce-pipeline