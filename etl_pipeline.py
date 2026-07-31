import pandas as pd
from sqlalchemy import create_engine

# 1. Настройка подключения к PostgreSQL
DATABASE_URL = "postgresql://de_user:de_password@host.docker.internal:5433/ecommerce"
engine = create_engine(DATABASE_URL)


def run_etl():
    print("--- [EXTRACT] Забор данных из витрины dm_category_sales ---")
    query = "SELECT * FROM dm_category_sales;"
    df = pd.read_sql(query, con=engine)
    print("Исходные данные из БД:")
    print(df)

    print("\n--- [TRANSFORM] Обогащение данных в Pandas ---")
    # Считаем общую выручку
    total_company_revenue = df['total_revenue'].sum()

    # Добавляем колонку с долей выручки каждой категории в %
    df['revenue_share_pct'] = ((df['total_revenue'] / total_company_revenue) * 100).round(2)

    # Сортируем по убыванию выручки
    df = df.sort_values(by='total_revenue', ascending=False)
    print("Трансформированные данные:")
    print(df)

    print("\n--- [LOAD] Сохранение отчетов на диск ---")
    # Сохраняем в CSV
    csv_file = "category_sales_report.csv"
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"Отчет успешно сохранен в {csv_file}")

    # Сохраняем в Parquet (профессиональный аналитический формат)
    parquet_file = "category_sales_report.parquet"
    df.to_parquet(parquet_file, index=False)
    print(f"Отчет успешно сохранен в {parquet_file}")


if __name__ == "__main__":
    run_etl()
