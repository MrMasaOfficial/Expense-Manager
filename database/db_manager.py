import sqlite3
from datetime import datetime
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_name='expenses.db'):
        self.db_path = Path(__file__).parent / db_name
        self.connection = None
        self.init_database()
    
    def init_database(self):
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        cursor = self.connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#FF6B6B'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                type TEXT CHECK(type IN ('expense', 'income')) DEFAULT 'expense',
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        ''')
        
        self.connection.commit()
        self.insert_default_categories()
    
    def insert_default_categories(self):
        cursor = self.connection.cursor()
        default_categories = [
            ('طعام', '#FF6B6B'),
            ('مواصلات', '#4ECDC4'),
            ('ترفيه', '#FFE66D'),
            ('صحة', '#95E1D3'),
            ('تعليم', '#C7CEEA'),
            ('مسكن', '#FFDAB9'),
            ('أخرى', '#BDB2FF'),
            ('دخل', '#52B788')
        ]
        
        for category, color in default_categories:
            try:
                cursor.execute('INSERT INTO categories (name, color) VALUES (?, ?)',
                              (category, color))
            except sqlite3.IntegrityError:
                pass
        
        self.connection.commit()
    
    def add_expense(self, amount, category_id, date, description, expense_type='expense'):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO expenses (amount, category_id, date, description, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (amount, category_id, date, description, expense_type))
        self.connection.commit()
        return cursor.lastrowid
    
    def get_all_expenses(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT e.id, e.amount, c.name as category, e.date, e.description, e.type, c.color
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            ORDER BY e.date DESC
        ''')
        return cursor.fetchall()
    
    def get_expenses_by_month(self, year, month):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT e.id, e.amount, c.name as category, e.date, e.description, e.type, c.color
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE strftime('%Y', e.date) = ? AND strftime('%m', e.date) = ?
            ORDER BY e.date DESC
        ''', (str(year), f'{month:02d}'))
        return cursor.fetchall()
    
    def get_category_summary(self, year, month):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT c.name, c.color, SUM(e.amount) as total, e.type
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE strftime('%Y', e.date) = ? AND strftime('%m', e.date) = ?
            GROUP BY c.id, e.type
            ORDER BY total DESC
        ''', (str(year), f'{month:02d}'))
        return cursor.fetchall()
    
    def get_categories(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT id, name, color FROM categories ORDER BY name')
        return cursor.fetchall()
    
    def delete_expense(self, expense_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        self.connection.commit()
    
    def close(self):
        if self.connection:
            self.connection.close()
