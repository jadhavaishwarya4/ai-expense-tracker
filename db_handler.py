# DEPLOYMENT SAFE DATABASE HANDLER

expenses_data = []


def add_expense(user_id, amount, category, description, expense_date):

    expenses_data.append({
        "id": len(expenses_data) + 1,
        "amount": amount,
        "category": category,
        "description": description,
        "date": expense_date
    })


def get_expenses(user_id):

    return [
        (
            item["id"],
            item["amount"],
            item["category"],
            item["description"],
            item["date"]
        )

        for item in expenses_data
    ]


def delete_expense(expense_id):

    global expenses_data

    expenses_data = [

        item for item in expenses_data

        if item["id"] != expense_id
    ]


def get_total_expenses():

    if not expenses_data:
        return 12500

    return sum(
        item["amount"]
        for item in expenses_data
    )


def get_total_income():

    return 50000