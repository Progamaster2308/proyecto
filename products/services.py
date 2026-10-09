from abc import ABC, abstractmethod

# Interfaz de la estrategia (Strategy Pattern)
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, price):
        pass

# Estrategia 1: Sin descuento
class NoDiscountStrategy(DiscountStrategy):
    def calculate_discount(self, price):
        return price

# Estrategia 2: Descuento por categoría electrónica (10%)
class ElectronicDiscountStrategy(DiscountStrategy):
    def calculate_discount(self, price):
        return price * 0.90

# Capa de Servicios que utiliza la estrategia
class PricingService:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def get_final_price(self, price):
        return self.strategy.calculate_discount(price)