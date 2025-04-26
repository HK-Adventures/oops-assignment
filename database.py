import sqlite3
import uuid
from models import Expense, Group
import json

class Database:
    def __init__(self, db_name='expense_splitter.db'):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create groups table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS groups (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    members TEXT NOT NULL
                )
            ''')

            # Create expenses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id TEXT PRIMARY KEY,
                    group_id TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    paid_by TEXT NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY (group_id) REFERENCES groups (id)
                )
            ''')
            conn.commit()

    def create_group(self, name, members):
        group_id = str(uuid.uuid4())
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO groups (id, name, members) VALUES (?, ?, ?)',
                (group_id, name, json.dumps(members))
            )
            conn.commit()
        return group_id

    def get_group(self, group_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM groups WHERE id = ?', (group_id,))
            row = cursor.fetchone()
            if row:
                return Group(row[0], row[1], json.loads(row[2]))
        return None

    def add_expense(self, group_id, description, amount, paid_by, date):
        expense_id = str(uuid.uuid4())
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO expenses (id, group_id, description, amount, paid_by, date) VALUES (?, ?, ?, ?, ?, ?)',
                (expense_id, group_id, description, amount, paid_by, date)
            )
            conn.commit()
        return expense_id

    def get_expenses(self, group_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM expenses WHERE group_id = ?', (group_id,))
            return [Expense(row[0], row[1], row[2], row[3], row[4], row[5]) for row in cursor.fetchall()]

    def calculate_balances(self, group_id):
        expenses = self.get_expenses(group_id)
        group = self.get_group(group_id)
        if not group:
            return {}

        balances = {member: 0 for member in group.members}
        total_amount = sum(expense.amount for expense in expenses)
        per_person = total_amount / len(group.members) if len(group.members) > 0 else 0

        for expense in expenses:
            balances[expense.paid_by] += expense.amount

        for member in balances:
            balances[member] -= per_person

        return balances 