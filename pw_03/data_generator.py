"""
Генератор тестовых данных для задания 30: Анализ авиакомпаний
Создает три файла:
1. airlines.csv - данные об авиакомпаниях
2. flights.xlsx - данные о рейсах
3. tickets.json - данные о билетах
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random

# Настройка генератора случайных чисел для воспроизводимости
np.random.seed(42)
random.seed(42)

def generate_airlines_data():
    """Генерация данных об авиакомпаниях (CSV)"""
    airlines_data = [
        {"airline_id": "AL001", "name": "Аэрофлот", "country": "Россия", "founded_year": 1923},
        {"airline_id": "AL002", "name": "S7 Airlines", "country": "Россия", "founded_year": 1992},
        {"airline_id": "AL003", "name": "Уральские авиалинии", "country": "Россия", "founded_year": 1943},
        {"airline_id": "AL004", "name": "Победа", "country": "Россия", "founded_year": 2014},
        {"airline_id": "AL005", "name": "Россия", "country": "Россия", "founded_year": 1934},
        {"airline_id": "AL006", "name": "Red Wings", "country": "Россия", "founded_year": 1999},
        {"airline_id": "AL007", "name": "Nordwind Airlines", "country": "Россия", "founded_year": 2008},
        {"airline_id": "AL008", "name": "Azur Air", "country": "Россия", "founded_year": 2010},
        {"airline_id": "AL009", "name": "Smartavia", "country": "Россия", "founded_year": 1963},
        {"airline_id": "AL010", "name": "Ямал", "country": "Россия", "founded_year": 1997}
    ]
    
    df_airlines = pd.DataFrame(airlines_data)
    df_airlines.to_csv('data/airlines.csv', index=False, encoding='utf-8')
    print("✓ Файл airlines.csv создан")
    return airlines_data

def generate_flights_data(airlines_data):
    """Генерация данных о рейсах (Excel)"""
    cities = [
        "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
        "Нижний Новгород", "Челябинск", "Самара", "Омск", "Ростов-на-Дону",
        "Уфа", "Красноярск", "Воронеж", "Пермь", "Волгоград", "Краснодар",
        "Саратов", "Тюмень", "Тольятти", "Ижевск"
    ]
    
    aircraft_types = ["Boeing 737", "Airbus A320", "Boeing 777", "Airbus A330", "Sukhoi Superjet 100"]
    
    flights_data = []
    flight_counter = 1
    
    # Генерируем рейсы за последние 12 месяцев
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    
    for _ in range(5000):  # Генерируем 5000 рейсов
        airline = random.choice(airlines_data)
        departure_city = random.choice(cities)
        arrival_city = random.choice([c for c in cities if c != departure_city])
        
        # Генерируем случайную дату в диапазоне
        random_days = random.randint(0, 365)
        flight_date = start_date + timedelta(days=random_days)
        
        # Количество пассажиров зависит от типа самолета
        aircraft = random.choice(aircraft_types)
        if "Boeing 777" in aircraft or "Airbus A330" in aircraft:
            max_passengers = random.randint(200, 350)
        elif "Sukhoi Superjet" in aircraft:
            max_passengers = random.randint(80, 120)
        else:
            max_passengers = random.randint(120, 200)
        
        passengers_count = random.randint(int(max_passengers * 0.6), max_passengers)
        
        flight = {
            "flight_id": f"FL{flight_counter:05d}",
            "airline_id": airline["airline_id"],
            "flight_number": f"{airline['airline_id'][-3:]}{random.randint(100, 999)}",
            "departure_city": departure_city,
            "arrival_city": arrival_city,
            "departure_date": flight_date.strftime("%Y-%m-%d"),
            "passengers_count": passengers_count,
            "aircraft_type": aircraft
        }
        
        flights_data.append(flight)
        flight_counter += 1
    
    df_flights = pd.DataFrame(flights_data)
    df_flights.to_excel('data/flights.xlsx', index=False)
    print("✓ Файл flights.xlsx создан")
    return flights_data

def generate_tickets_data(flights_data):
    """Генерация данных о билетах (JSON)"""
    ticket_classes = ["Economy", "Business", "First"]
    
    tickets_data = []
    ticket_counter = 1
    
    for flight in flights_data:
        # Для каждого рейса создаем записи о билетах разных классов
        num_ticket_types = random.randint(1, 3)  # От 1 до 3 классов билетов на рейс
        
        for _ in range(num_ticket_types):
            ticket_class = random.choice(ticket_classes)
            
            # Базовая цена зависит от расстояния (упрощенно)
            base_price = random.uniform(3000, 25000)
            
            # Корректировка цены по классу
            if ticket_class == "Business":
                price_multiplier = random.uniform(2.5, 4.0)
            elif ticket_class == "First":
                price_multiplier = random.uniform(4.0, 8.0)
            else:  # Economy
                price_multiplier = random.uniform(0.8, 1.2)
            
            avg_ticket_price = round(base_price * price_multiplier, 2)
            
            ticket = {
                "ticket_id": f"TK{ticket_counter:06d}",
                "flight_id": flight["flight_id"],
                "avg_ticket_price": avg_ticket_price,
                "ticket_class": ticket_class
            }
            
            tickets_data.append(ticket)
            ticket_counter += 1
    
    # Сохраняем в JSON
    with open('data/tickets.json', 'w', encoding='utf-8') as f:
        json.dump(tickets_data, f, ensure_ascii=False, indent=2)
    
    print("✓ Файл tickets.json создан")
    return tickets_data

def main():
    """Основная функция генерации данных"""
    print("Генерация тестовых данных для анализа авиакомпаний...")
    print("=" * 50)
    
    # Генерируем данные
    airlines_data = generate_airlines_data()
    flights_data = generate_flights_data(airlines_data)
    tickets_data = generate_tickets_data(flights_data)
    
    print("=" * 50)
    print(f"Сгенерировано:")
    print(f"- Авиакомпаний: {len(airlines_data)}")
    print(f"- Рейсов: {len(flights_data)}")
    print(f"- Записей о билетах: {len(tickets_data)}")
    print("\nВсе файлы сохранены в папке 'data/'")

if __name__ == "__main__":
    main()
