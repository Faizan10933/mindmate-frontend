from flask import Flask, render_template

app = Flask(__name__)

@app.route('/summary')
def dashboard():
    summary = {
        "total_amount_spent": 238.75,
        "top_restaurants": [
            { "name": "McDonald's", "visits": 2 },
            { "name": "Domino's Pizza", "visits": 1 },
            { "name": "Starbucks", "visits": 1 },
            { "name": "Subway", "visits": 1 },
            { "name": "McDonald's Family Restaurant", "visits": 1 }
        ],
        "frequently_purchased_items": {
            "McDonald's Family Restaurant": [
                "2PC HHB Classic ScrambleEgg",
                "Diff: Conv. To Filterffee"
            ],
            "Domino's Pizza": [
                "Margherita Pizza",
                "Garlic Bread",
                "Choco Lava Cake"
            ],
            "McDonald's": [
                "McChicken",
                "French Fries",
                "Coke"
            ],
            "Starbucks": [
                "Caffe Latte",
                "Espresso"
            ],
            "Subway": [
                "Veggie Delight",
                "Pepsi"
            ]
        },
        "patterns": [
            {
                "type": "Restaurant Preference",
                "description": "Frequent visits to McDonald's and preference for fast food."
            },
            {
                "type": "Spending Habits",
                "description": "Higher spending at McDonald's Family Restaurant compared to other restaurants."
            }
        ],
        "recommendations": [
            "Consider exploring other cuisines to diversify your food choices.",
            "Track your spending at McDonald's to manage your budget effectively."
        ]
    }

    return render_template("dashboard.html", summary=summary)


from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/insights/total-spending', methods=['GET'])
def total_spending():
    # This would come from your data source
    spending_data = [
        {"restaurant": "McDonald's", "amount": 25.00, "date": "2025-07-20"},
        {"restaurant": "Domino's Pizza", "amount": 30.25, "date": "2025-07-18"},
        {"restaurant": "Starbucks", "amount": 40.00, "date": "2025-06-05"},
        {"restaurant": "Subway", "amount": 25.00, "date": "2025-07-02"},
        {"restaurant": "McDonald's", "amount": 30.00, "date": "2025-06-30"},
        {"restaurant": "McDonald's Family Restaurant", "amount": 58.50, "date": "2025-07-21"}
    ]

    total = sum(item["amount"] for item in spending_data)

    monthly = {}
    by_restaurant = {}

    for item in spending_data:
        month = item["date"][:7]  # "YYYY-MM"
        monthly[month] = monthly.get(month, 0) + item["amount"]
        restaurant = item["restaurant"]
        by_restaurant[restaurant] = by_restaurant.get(restaurant, 0) + item["amount"]

    return jsonify({
        "total_amount_spent": round(total, 2),
        "monthly_breakdown": {k: round(v, 2) for k, v in monthly.items()},
        "restaurant_spending": {k: round(v, 2) for k, v in by_restaurant.items()}
    })
