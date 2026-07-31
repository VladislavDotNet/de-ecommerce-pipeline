import random
from faker import Faker
from sqlalchemy import create_engine, text

# 1. Подключение к PostgreSQL в Docker (порт 5433!)
DATABASE_URL = "postgresql://de_user:de_password@127.0.0.1:5433/ecommerce"
engine = create_engine(DATABASE_URL)

fake = Faker('ru_RU')  # Генератор данных на русском языке


def generate_data():
    with engine.connect() as conn:
        print("Генерация пользователей...")
        for _ in range(50):
            conn.execute(
                text("INSERT INTO users (name, email) VALUES (:name, :email) ON CONFLICT DO NOTHING"),
                {"name": fake.name(), "email": fake.unique.email()}
            )

        print("Генерация товаров...")
        categories = ['Электроника', 'Одежда', 'Книги', 'Дом и сад']
        for _ in range(20):
            conn.execute(
                text("INSERT INTO products (title, price, category) VALUES (:title, :price, :cat)"),
                {
                    "title": fake.word().capitalize(),
                    "price": round(random.uniform(100, 50000), 2),
                    "cat": random.choice(categories)
                }
            )
        conn.commit()

        # Получаем ID созданных пользователей и товаров
        user_ids = [row[0] for row in conn.execute(text("SELECT user_id FROM users")).fetchall()]
        product_ids = [row[0] for row in conn.execute(text("SELECT product_id FROM products")).fetchall()]

        print("Генерация заказов...")
        for _ in range(200):
            conn.execute(
                text("""
                    INSERT INTO orders (user_id, product_id, quantity, order_date) 
                    VALUES (:u_id, :p_id, :qty, :date)
                """),
                {
                    "u_id": random.choice(user_ids),
                    "p_id": random.choice(product_ids),
                    "qty": random.randint(1, 5),
                    "date": fake.date_time_between(start_date='-1y', end_date='now')
                }
            )
        conn.commit()
        print("Готово! Данные успешно загружены.")


if __name__ == "__main__":
    generate_data()