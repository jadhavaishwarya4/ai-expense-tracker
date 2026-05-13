def chatbot_response(user_input):

    user_input = user_input.lower()

    # =========================
    # SAVINGS
    # =========================

    if (
        "save" in user_input
        or "cut" in user_input
        or "reduce" in user_input
        or "less" in user_input
    ):

        return (
            "Try reducing shopping and entertainment expenses first. "
            "Tracking small daily expenses can also improve savings."
        )

    # =========================
    # OVERSPENDING
    # =========================

    elif (
        "overspending" in user_input
        or "too much" in user_input
        or "spending high" in user_input
    ):

        return (
            "You are likely overspending on food and shopping categories."
        )

    # =========================
    # FOOD
    # =========================

    elif (
        "food" in user_input
        or "restaurant" in user_input
        or "eating" in user_input
    ):

        return (
            "Food expenses can be optimized by limiting online orders "
            "and dining out frequently."
        )

    # =========================
    # BUDGET
    # =========================

    elif "budget" in user_input:

        return (
            "A good strategy is the 50-30-20 budgeting rule: "
            "50% needs, 30% wants, 20% savings."
        )

    # =========================
    # INVESTMENT
    # =========================

    elif (
        "invest" in user_input
        or "investment" in user_input
    ):

        return (
            "You can consider SIPs, index funds, or emergency savings "
            "depending on your risk profile."
        )

    # =========================
    # GREETING
    # =========================

    elif (
        "hello" in user_input
        or "hi" in user_input
    ):

        return "Hello! I am your AI Finance Assistant."

    # =========================
    # DEFAULT
    # =========================

    else:

        return (
            "I can help with budgeting, saving money, "
            "expense analysis, and financial planning."
        )