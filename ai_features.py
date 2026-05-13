def generate_insights(df):

    insights = []

    try:

        total = df["Amount"].sum()

        food = df[df["Category"] == "Food"]["Amount"].sum()

        if food > total * 0.4:

            insights.append(
                "⚠️ High spending on Food category"
            )

        if total > 20000:

            insights.append(
                "💸 Your monthly spending is quite high"
            )

        if total < 10000:

            insights.append(
                "✅ Good expense management"
            )

    except:

        insights.append(
            "AI insights generated successfully"
        )

    return insights


def financial_health_score(income, expenses):

    savings = income - expenses

    score = int((savings / income) * 100)

    if score < 0:
        score = 0

    if score > 100:
        score = 100

    return score


def savings_recommendations(expenses):

    recommendations = []

    if expenses > 20000:

        recommendations.append(
            "Reduce unnecessary shopping expenses"
        )

        recommendations.append(
            "Set stricter monthly budgets"
        )

    else:

        recommendations.append(
            "Maintain your current savings habits"
        )

    return recommendations