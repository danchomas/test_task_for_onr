#include "buy.hpp"
#include <stdexcept>
using namespace std;

Buy::Buy() : quantity(0), totalPrice(0.0f), totalWeight(0.0f) {}

void Buy::setBuyData(int qty)
{
    if (qty < 0)
        throw invalid_argument("нельзя вводить отрицательную цену");
    quantity = qty;
    totalPrice = getPrice() * static_cast<float>(quantity);
    totalWeight = getWeight() * static_cast<float>(quantity);
}

int Buy::getQuantity() const { return quantity; }
float Buy::getTotalPrice() const { return totalPrice; }
float Buy::getTotalWeight() const { return totalWeight; }