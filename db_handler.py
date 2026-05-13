import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="newpassword123",
    database="expense_tracker"
)

cursor = conn.cursor()

# =====================================================
# ADD EXPENSE
# =====================================================

def add_expense(user_id, amount, category, description, expense_date):

    query = """
    INSERT INTO expenses
    (user_id, amount, category, description, date)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        user_id,
        amount,
        category,
        description,
        expense_date
    )

    cursor.execute(query, values)
    conn.commit()

# =====================================================
# GET EXPENSES
# =====================================================

def get_expenses(user_id):

    query = """
    SELECT id, amount, category, description, date
    FROM expenses
    WHERE user_id = %s
    ORDER BY date DESC
    """

    cursor.execute(query, (user_id,))

    return cursor.fetchall()

# =====================================================
# DELETE EXPENSE
# =====================================================

def delete_expense(expense_id):

    query = "DELETE FROM expenses WHERE id = %s"

    cursor.execute(query, (expense_id,))

    conn.commit()

# =====================================================
# TOTAL EXPENSES
# =====================================================

def get_total_expenses():

    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    result = cursor.fetchone()[0]

    return result if result else 0

# =====================================================
# TOTAL INCOME
# =====================================================

def get_total_income():

    cursor.execute(
        "SELECT SUM(amount) FROM income"
    )

    result = cursor.fetchone()[0]

    return result if result else 0