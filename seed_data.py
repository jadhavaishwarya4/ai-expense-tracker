# utils/seed_data.py
# ============================================================
# Sample Data Generator
# Creates realistic demo data for the expense tracker
# ============================================================

import random
from datetime import datetime, date, timedelta
from database.db_handler import execute_query, init_database
from utils.auth import hash_password


def generate_sample_data():
    """
    Creates demo user with 6 months of realistic expense/income data.
    Run this once after setting up the database.
    """
    print("🌱 Seeding sample data...")

    # Initialize schema
    init_database()

    # -------------------------------------------------------
    # Create demo user
    # -------------------------------------------------------
    demo_password = hash_password("demo123")
    try:
        execute_query(
            """INSERT IGNORE INTO users (username, email, password_hash, full_name, currency, monthly_goal)
               VALUES ('demo', 'demo@example.com', :pwd, 'Arjun Sharma', 'INR', 50000)""",
            {"pwd": demo_password},
            fetch=False
        )
        print("✅ Demo user created: username='demo', password='demo123'")
    except Exception as e:
        print(f"Note: {e}")

    # Get user ID
    user = execute_query("SELECT id FROM users WHERE username = 'demo'")
    if user is None or user.empty:
        print("❌ Could not find demo user.")
        return
    user_id = int(user.iloc[0]["id"])

    # -------------------------------------------------------
    # Generate expenses for last 6 months
    # -------------------------------------------------------
    categories_config = {
        "Food": {"min": 200, "max": 3000, "freq": 20},
        "Transport": {"min": 50, "max": 800, "freq": 15},
        "Shopping": {"min": 500, "max": 5000, "freq": 5},
        "Bills": {"min": 500, "max": 4000, "freq": 3},
        "Entertainment": {"min": 200, "max": 2000, "freq": 6},
        "Health": {"min": 100, "max": 2000, "freq": 3},
        "Education": {"min": 500, "max": 3000, "freq": 2},
        "Others": {"min": 100, "max": 1000, "freq": 4},
    }

    descriptions = {
        "Food": ["Zomato order", "Grocery shopping", "Restaurant dinner", "Chai & snacks", "Swiggy order", "Supermarket", "Local dhaba", "Meal prep"],
        "Transport": ["Uber ride", "Metro card recharge", "Ola cab", "Auto rickshaw", "Bus pass", "Petrol fill", "Rapido"],
        "Shopping": ["Amazon order", "Flipkart purchase", "Clothes", "Electronics", "Home decor", "Books", "Footwear"],
        "Bills": ["Electricity bill", "Internet bill", "Phone recharge", "DTH subscription", "Water bill", "Gas bill"],
        "Entertainment": ["Netflix subscription", "Movie tickets", "Spotify", "Concert tickets", "Gaming"],
        "Health": ["Doctor consultation", "Pharmacy", "Gym membership", "Yoga class", "Health checkup"],
        "Education": ["Udemy course", "Books", "Online subscription", "Coaching fee"],
        "Others": ["Gift for friend", "Donation", "Miscellaneous", "Stationery"],
    }

    today = date.today()
    expenses_added = 0

    for months_back in range(6, -1, -1):
        target_date = date(today.year, today.month, 1)
        for _ in range(months_back):
            if target_date.month == 1:
                target_date = date(target_date.year - 1, 12, 1)
            else:
                target_date = date(target_date.year, target_date.month - 1, 1)

        month = target_date.month
        year = target_date.year
        days_in_month = (date(year + (month // 12), (month % 12) + 1, 1) - date(year, month, 1)).days

        for category, config in categories_config.items():
            num_transactions = random.randint(max(1, config["freq"] - 3), config["freq"] + 3)
            for _ in range(num_transactions):
                day = random.randint(1, days_in_month)
                txn_date = date(year, month, day)
                if txn_date > today:
                    continue

                amount = round(random.uniform(config["min"], config["max"]), 2)
                desc = random.choice(descriptions.get(category, ["Expense"]))

                execute_query(
                    """INSERT INTO expenses (user_id, amount, category, description, date)
                       VALUES (:uid, :amt, :cat, :desc, :dt)""",
                    {"uid": user_id, "amt": amount, "cat": category, "desc": desc, "dt": str(txn_date)},
                    fetch=False
                )
                expenses_added += 1

    print(f"✅ Added {expenses_added} expense transactions")

    # -------------------------------------------------------
    # Generate income for last 6 months
    # -------------------------------------------------------
    income_added = 0
    for months_back in range(6, -1, -1):
        target_date = date(today.year, today.month, 1)
        for _ in range(months_back):
            if target_date.month == 1:
                target_date = date(target_date.year - 1, 12, 1)
            else:
                target_date = date(target_date.year, target_date.month - 1, 1)

        month = target_date.month
        year = target_date.year

        # Salary on 1st
        execute_query(
            """INSERT INTO income (user_id, amount, source, description, date, is_recurring, frequency)
               VALUES (:uid, :amt, 'Salary', 'Monthly Salary', :dt, 1, 'monthly')""",
            {"uid": user_id, "amt": round(random.uniform(75000, 85000), 2), "dt": f"{year}-{month:02d}-01"},
            fetch=False
        )
        income_added += 1

        # Freelance sometimes
        if random.random() > 0.5:
            execute_query(
                """INSERT INTO income (user_id, amount, source, description, date, is_recurring, frequency)
                   VALUES (:uid, :amt, 'Freelance', 'Web dev project', :dt, 0, 'one-time')""",
                {"uid": user_id, "amt": round(random.uniform(5000, 20000), 2),
                 "dt": f"{year}-{month:02d}-{random.randint(10, 28):02d}"},
                fetch=False
            )
            income_added += 1

    print(f"✅ Added {income_added} income records")

    # -------------------------------------------------------
    # Set monthly budgets for current month
    # -------------------------------------------------------
    budgets = {
        "Food": 15000,
        "Transport": 5000,
        "Shopping": 10000,
        "Bills": 8000,
        "Entertainment": 5000,
        "Health": 3000,
        "Education": 5000,
        "Others": 3000,
    }

    for category, amount in budgets.items():
        execute_query(
            """INSERT IGNORE INTO budgets (user_id, category, amount, month, year)
               VALUES (:uid, :cat, :amt, :month, :year)""",
            {"uid": user_id, "cat": category, "amt": amount, "month": today.month, "year": today.year},
            fetch=False
        )

    print("✅ Set monthly budgets")

    # -------------------------------------------------------
    # Add savings goals
    # -------------------------------------------------------
    goals = [
        ("Emergency Fund 🛡️", 100000, 40000, "2025-12-31"),
        ("Europe Trip ✈️", 200000, 35000, "2025-09-01"),
        ("New Laptop 💻", 80000, 20000, "2025-06-01"),
    ]

    for name, target, current, deadline in goals:
        execute_query(
            """INSERT IGNORE INTO savings_goals (user_id, goal_name, target_amount, current_amount, deadline)
               VALUES (:uid, :name, :target, :current, :deadline)""",
            {"uid": user_id, "name": name, "target": target, "current": current, "deadline": deadline},
            fetch=False
        )

    print("✅ Added savings goals")
    print("\n🎉 Sample data seeded successfully!")
    print("   Login with: username='demo', password='demo123'")


if __name__ == "__main__":
    generate_sample_data()
