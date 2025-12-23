from flask import Flask, request, jsonify
from pymongo import MongoClient
import abc

app = Flask(__name__)

# Strategy Pattern Interface
class PaymentStrategy(abc.ABC):
    @abc.abstractmethod
    def pay(self, amount):
        pass

# Concrete Strategies
class GPayStrategy(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} via Google Pay"

class PhonePeStrategy(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} via PhonePe"

class CardStrategy(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} via Credit/Debit Card"

# Context
class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def execute_payment(self, amount):
        return self._strategy.pay(amount)

@app.route('/process', methods=['POST'])
def process_payment():
    data = request.json
    amount = data.get('amount')
    method = data.get('method', 'card').lower()
    
    if not amount: return jsonify({"message": "Invalid amount"}), 400
    
    strategy = None
    if method == 'gpay': strategy = GPayStrategy()
    elif method == 'phonepe': strategy = PhonePeStrategy()
    else: strategy = CardStrategy()
    
    context = PaymentContext(strategy)
    message = context.execute_payment(amount)
    
    return jsonify({"status": "SUCCESS", "message": message}), 200

if __name__ == '__main__':
    print("Payment Service running on port 5005")
    app.run(port=5005, debug=True)
