import psycopg2, random
from math import ceil, sqrt
from psycopg2 import Error

import datetime, time, string, random
from functools import wraps
from random import randint 
from functools import wraps
from sqlalchemy import delete, Column, Integer, String, ForeignKey, TIMESTAMP, PrimaryKeyConstraint, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
import time
from datetime import datetime, timedelta

Base = declarative_base()

# Таблиця users
class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    # Відношення до таблиці contacts
    contacts = relationship("Contacts", back_populates="users", cascade="all, delete-orphan")
    # Відношення до таблиці reservations
    reservations = relationship("Reservations", back_populates="users", cascade="all, delete-orphan")

# Таблиця contacts
class Contacts(Base):
    __tablename__ = 'contacts'

    contact_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)

    # Відношення до таблиці users
    users = relationship("Users", back_populates="contacts")

# Таблиця restaurants
class Restaurants(Base):
    __tablename__ = 'restaurants'

    restaurant_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    table_quantity = Column(Integer, nullable=False)

    # Відношення до таблиці restaurant_tables
    tables = relationship("RestaurantTables", back_populates="restaurants", cascade="all, delete-orphan")

# Таблиця restaurant_tables
class RestaurantTables(Base):
    __tablename__ = 'restaurant_tables'

    table_id = Column(Integer, primary_key=True)
    capacity = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id', ondelete='CASCADE'), nullable=False)

    # Відношення до таблиці restaurants
    restaurants = relationship("Restaurants", back_populates="tables")
    # Відношення до таблиці reservations
    reservations = relationship("Reservations", back_populates="tables", cascade="all, delete-orphan")

# Таблиця reservations
class Reservations(Base):
    __tablename__ = 'reservations'

    reservation_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    table_id = Column(Integer, ForeignKey('restaurant_tables.table_id', ondelete='CASCADE'), nullable=False)
    reservation_date = Column(TIMESTAMP, nullable=False)
    duration = Column(Integer, nullable=False)

    # Відношення до таблиці users
    users = relationship("Users", back_populates="reservations")
    # Відношення до таблиці restaurant_tables
    tables = relationship("RestaurantTables", back_populates="reservations")

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/shinkarenko"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        print(f"\nFunction '{func.__name__}' executed in {elapsed_time:.4f} milliseconds\n")
        return result
    return wrapper

class Model:
    
    # Перегляд
    @timeit
    def display_table_rows(self, table_name, start_row=0, num_rows=10):
        try:
            # Завантажуємо модель класу для таблиці за її назвою
            model_class = globals().get(table_name)
            if not model_class:
                raise ValueError(f"Table model {table_name} not found.")
            # Виконання запиту з обмеженням на кількість рядків та початок
            records = session.query(model_class).offset(start_row).limit(num_rows).all()
            
            if records:
                return records
            else:
                print(f"No records found in {table_name}.")
        except Exception as e:
            print(f"Error fetching data from {table_name}: {str(e)}")
        return []

    @timeit
    def get_data_in_range(self, table_name, id_field, id_start, id_end, order_field):
        try:
            
            model_class = globals().get(table_name)
            if not model_class:
                raise ValueError(f"Table model {table_name} not found.")
            query = session.query(model_class).filter(
                getattr(model_class, id_field).between(id_start, id_end)
            ).order_by(getattr(model_class, order_field))
            records = query.all()
            
            if records:
                return records
            else:
                print(f"No records found in {table_name} within the given range.")
        except Exception as e:
            session.rollback()
            print(f"Error fetching data from {table_name}: {str(e)}")
        return []

    # Пошук за шаблоном LIKE
    @timeit
    def get_data_by_field_like(self, table_name, req_field, search_req, order_field):
        try:
            model_class = globals().get(table_name)
            if not model_class:
                raise ValueError(f"Table model {table_name} not found.")
            
            query = session.query(model_class).filter(
                getattr(model_class, req_field).ilike(f"%{search_req}%")
            ).order_by(getattr(model_class, order_field))
            
            records = query.all()
            
            if records:
                return records
            else:
                print(f"No records found in {table_name} matching the search criteria.")
        except Exception as e:
            session.rollback()
            print(f"Error fetching data from {table_name}: {str(e)}")
        return []

    # ВИДАЛЕННЯ

    @timeit
    def delete_data(self, table_class, field_name, value):
        try:
            # Отримання атрибуту класу за назвою поля
            field = getattr(table_class, field_name)
            # Створення запиту на видалення
            stmt = delete(table_class).where(field == value)
            # Виконання запиту
            result = session.execute(stmt)
            session.commit()
            rows_deleted = result.rowcount
            print(f"\n{rows_deleted} rows affected")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")

    # Додавання нового користувача
    @timeit
    def add_user(self, name):
        """Додавання нового користувача до таблиці users."""
        try:
            latest_id = session.query(func.max(Users.user_id)).scalar() or 0  # Якщо таблиця порожня, latest_id = 0
            new_id = latest_id + 1

            user = Users(user_id=new_id, name=name)
            session.add(user)
            session.commit()
            print(f"User '{name}' added successfully with user_id = {new_id}.")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")

    # Оновлення даних користувача
    @timeit
    def update_user(self, user_id, new_name):
        """Оновлення імені користувача за user_id."""
        try:
            user = session.query(Users).filter_by(user_id=user_id).first()
            if user:
                user.name = new_name
                session.commit()
                print("\nUser successfully updated.")
            else:
                print(f"\nUser with user_id = {user_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error updating user: {str(e)}")

    # Видалення користувача
    @timeit
    def delete_user(self, user_id):
        """Видалення користувача за user_id."""
        try:
            user = session.query(Users).filter_by(user_id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
                print("\nUser successfully deleted.")
            else:
                print(f"\nUser with user_id = {user_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting user: {str(e)}")

    # Генерація користувачів
    @timeit
    def generate_users(self, num_users):
        """Генерація випадкових користувачів для таблиці users."""
        try:
            # Отримуємо максимальний user_id з таблиці, щоб уникнути дублювання
            max_user_id = session.query(func.max(Users.user_id)).scalar() or 0
            # Генерація користувачів
            users = []
            for _ in range(num_users):
                user_id = max_user_id + 1
                name = f"User_{randint(10000, 99999)}"  # Генерація випадкового імені
                users.append(Users(user_id=user_id, name=name))
                max_user_id += 1  # Оновлюємо максимальний user_id
            # Додавання нових користувачів до сесії
            session.add_all(users)
            session.commit()
            print(f"{num_users} users generated successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error generating users: {str(e)}")

    @timeit
    def generate_restaurants(self, num_restaurants):
        """Генерація нових ресторанів"""
        try:
            # Отримуємо максимальний restaurant_id з таблиці для уникнення дублювання
            max_restaurant_id = session.query(func.max(Restaurants.restaurant_id)).scalar() or 0
            # Генерація ресторанів
            restaurants = []
            for _ in range(num_restaurants):
                restaurant_id = max_restaurant_id + 1
                name = f"Restaurant_{randint(1, 1000)}"  # Генерація випадкової назви ресторану
                table_quantity = randint(1, 50)  # Генерація випадкової кількості столів (від 1 до 50)
                restaurants.append(Restaurants(restaurant_id=restaurant_id, name=name, table_quantity=table_quantity))
                max_restaurant_id += 1  # Оновлюємо максимальний restaurant_id
            # Додавання нових ресторанів до сесії
            session.add_all(restaurants)
            session.commit()
            print(f"{num_restaurants} restaurants generated successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error generating restaurants: {str(e)}")

    @timeit
    def add_restaurant(self, name, table_quantity):
        """Додавання нового ресторану з перевіркою максимального restaurant_id"""
        try:
            # Заміняємо одиночні апострофи на два апострофи
            name = name.replace("'", "''")
            # Отримуємо максимальний restaurant_id з таблиці для уникнення дублювання
            max_restaurant_id = session.query(Restaurants).order_by(Restaurants.restaurant_id.desc()).first()
            next_restaurant_id = max_restaurant_id.restaurant_id + 1 if max_restaurant_id else 1
            # Створюємо новий ресторан
            new_restaurant = Restaurants(restaurant_id=next_restaurant_id, name=name, table_quantity=table_quantity)
            # Додаємо новий ресторан до сесії і зберігаємо зміни
            session.add(new_restaurant)
            session.commit()
            print(f"Restaurant '{name}' added successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error adding restaurant: {str(e)}")

    @timeit
    def update_restaurant(self, restaurant_id, name, table_quantity):
        """Оновлення інформації про ресторан"""
        try:
            # Знаходимо ресторан за ID
            restaurant = session.query(Restaurants).filter(Restaurants.restaurant_id == restaurant_id).first()

            # Якщо ресторан знайдено, оновлюємо його
            if restaurant:
                restaurant.name = name
                restaurant.table_quantity = table_quantity
                session.commit()
                print(f"Restaurant with ID {restaurant_id} updated successfully.")
            else:
                print(f"Restaurant with ID {restaurant_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error updating restaurant: {str(e)}")

    @timeit
    def add_restaurant_table(self, capacity, restaurant_id):
        """Додавання нової таблиці до ресторану з унікальним ID"""
        try:
            # Знаходимо максимальний table_id для уникнення дублювання
            max_table_id = session.query(func.max(RestaurantTables.table_id)).scalar() or 0
            # Додавання нової таблиці
            new_table = RestaurantTables(table_id=max_table_id + 1, capacity=capacity, restaurant_id=restaurant_id)
            session.add(new_table)
            session.commit()

            print(f"Restaurant table added successfully with ID {max_table_id + 1}.")
        except Exception as e:
            session.rollback()
            print(f"Error adding restaurant table: {str(e)}")

    @timeit
    def update_restaurant_table(self, table_id, capacity, restaurant_id):
        """Оновлення таблиці ресторану"""
        try:
            # Знаходимо таблицю за table_id
            table_to_update = session.query(RestaurantTables).filter_by(table_id=table_id).first()

            if table_to_update:
                # Оновлюємо поля
                table_to_update.capacity = capacity
                table_to_update.restaurant_id = restaurant_id
                session.commit()
                print(f"Restaurant table {table_id} updated successfully.")
            else:
                print(f"Restaurant table with ID {table_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error updating restaurant table: {str(e)}")

    @timeit
    def generate_restaurant_tables(self, num_tables):
        """Генерація нових столів для ресторанів з перевіркою максимальних значень"""
        try:
            # Отримуємо максимальний table_id з таблиці для уникнення дублювання
            max_table_id = session.query(func.max(RestaurantTables.table_id)).scalar() or 0
            # Отримуємо максимальний restaurant_id з таблиці restaurants
            max_restaurant_id = session.query(func.max(Restaurants.restaurant_id)).scalar() or 0
            # Генерація столів
            for _ in range(num_tables):
                table_id = max_table_id + 1
                capacity = random.randint(1, 10)  # Випадкова кількість місць від 1 до 10
                restaurant_id = random.randint(1, max_restaurant_id)  # Випадковий restaurant_id
                # Створення нового столу
                new_table = RestaurantTables(table_id=table_id, capacity=capacity, restaurant_id=restaurant_id)
                session.add(new_table)
                max_table_id += 1  # Оновлюємо max_table_id
            session.commit()
            print(f"{num_tables} restaurant tables generated successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error generating restaurant tables: {str(e)}")

    @timeit
    def add_reservation(self, user_id, table_id, reservation_date, duration):
        """Додавання нового бронювання"""
        try:
            # Генерація нового reservation_id
            max_reservation_id = session.query(func.max(Reservations.reservation_id)).scalar() or 0
            new_reservation_id = max_reservation_id + 1
            # Створення нового об'єкта бронювання
            reservation = Reservations(
                reservation_id=new_reservation_id,
                user_id=user_id,
                table_id=table_id,
                reservation_date=reservation_date,
                duration=duration
            )
            # Додавання бронювання в сесію
            session.add(reservation)
            session.commit()
            print(f"Reservation added successfully for user {user_id} at table {table_id}.")
        except Exception as e:
            session.rollback()
            print(f"Error adding reservation: {str(e)}")

    @timeit
    def update_reservation(self, reservation_id, user_id, table_id, reservation_date, duration):
        """Оновлення бронювання"""
        try:
            # Отримуємо бронювання за reservation_id
            reservation = session.query(Reservations).filter_by(reservation_id=reservation_id).first()
            if reservation:
                # Оновлюємо поля бронювання
                reservation.user_id = user_id
                reservation.table_id = table_id
                reservation.reservation_date = reservation_date
                reservation.duration = duration
                # Зберігаємо зміни
                session.commit()
                print(f"Reservation {reservation_id} updated successfully.")
            else:
                print(f"Reservation {reservation_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error updating reservation: {str(e)}")
    
    @timeit
    def generate_reservations(self, num_reservations):
        """Генерація випадкових бронювань без циклів, через SQLAlchemy"""
        try:
            # Отримуємо максимальні значення для user_id, table_id
            max_user_id = session.query(func.max(Users.user_id)).scalar() or 0
            max_table_id = session.query(func.max(RestaurantTables.table_id)).scalar() or 0

            # Генерація випадкових бронювань
            for _ in range(num_reservations):
                # Випадкові значення
                user_id = random.randint(1, max_user_id)
                table_id = random.randint(1, max_table_id)
                reservation_date = datetime.now() + timedelta(days=random.randint(1, 30))
                duration = random.randint(1, 3)  # Тривалість у хвилинах (1-3 години)
                # Створення об'єкта бронювання
                reservation = Reservations(
                    user_id=user_id,
                    table_id=table_id,
                    reservation_date=reservation_date,
                    duration=duration
                )
                # Додавання та збереження бронювання
                session.add(reservation)
            session.commit()
            print(f"Successfully generated {num_reservations} reservations.")
        except Exception as e:
            session.rollback()
            print(f"Error generating reservations: {str(e)}")
    
    @timeit
    def add_contact(self, user_id, email, phone):
        """Додавання нового контакту з унікальним contact_id"""
        try:
            # Отримуємо максимальний contact_id для уникнення дублювання
            max_contact_id = session.query(func.max(Contacts.contact_id)).scalar() or 0
            # Створюємо новий контакт
            new_contact = Contacts(
                contact_id=max_contact_id + 1,  # Новий контактний ID
                user_id=user_id,
                email=email,
                phone=phone
            )
            # Додаємо та зберігаємо контакт
            session.add(new_contact)
            session.commit()
            print(f"Contact added successfully for user {user_id}.")
        except Exception as e:
            session.rollback()
            print(f"Error adding contact: {str(e)}")

    @timeit
    def update_contact(self, contact_id, field, value):
        """Оновлення даних контакту"""
        try:
            # Динамічно оновлюємо поле, використовуючи getattr для атрибутів моделі
            contact = session.query(Contacts).filter(Contacts.contact_id == contact_id).first()
            if contact:
                # Оновлюємо значення поля
                setattr(contact, field, value)
                session.commit()
                print(f"Contact with ID {contact_id} updated successfully.")
            else:
                print(f"Contact with ID {contact_id} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error updating contact: {str(e)}")

    @timeit
    def generate_contacts(self, num_contacts):
        try:
            # Отримуємо максимальний contact_id
            max_contact_id = session.query(func.max(Contacts.contact_id)).scalar() or 0
            for i in range(num_contacts):
                contact_id = max_contact_id + i + 1
                user_id = randint(1, session.query(func.max(Users.user_id)).scalar() or 1)  # Випадковий user_id
                email = f'user{contact_id}@mail.com'
                phone = f'{randint(1000000000, 9999999999)}'  # Генерація випадкового номера
                contact = Contacts(contact_id=contact_id, user_id=user_id, email=email, phone=phone)
                session.add(contact)
            session.commit()
            print(f"{num_contacts} contacts generated successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error generating contacts: {str(e)}")