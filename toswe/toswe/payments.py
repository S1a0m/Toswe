import random

class PaymentGateway:
    @staticmethod
    def pay_with_moov(number, amount):
        # Simuler un paiement Moov
        return random.choice([True, False])  # Simule success/fail

    @staticmethod
    def pay_with_mtn(number, amount):
        # Simuler un paiement MTN
        return random.choice([True, False])
