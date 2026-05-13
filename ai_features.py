import pandas as pd


def generate_insights(df):

    insights = []

    if df.empty:
        return ["No expense data available"]

    total_food = df[
        df['category'] == 'Food'
    ]['amount'].sum()

    if total_food > 5000:

        insights.append(
            "⚠️ High food spending detected"
        )

    highest = (
        df.groupby('category')['amount']
        .sum()
        .idxmax()
    )

    insights.append(
        f"💡 Highest spending category: {highest}"
    )

    return insights


def financial_health_score(income, expenses):

    if income == 0:
        return 0

    savings_ratio = (
        (income - expenses) / income
    )

    score = int(savings_ratio * 100)

    score = max(0, min(score, 100))

    return score


def savings_recommendations(expenses):

    recommendations = []

    if expenses > 20000:

        recommendations.append(
            "Reduce shopping expenses"
        )

    recommendations.append(
        "Track daily spending"
    )

    return recommendations