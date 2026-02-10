#pragma once
#include "product.hpp"
using namespace std;

class Buy : public Product
{
private:
    int quantity;
    float totalPrice;
    float totalWeight;

public:
    Buy();
    void setBuyData(int qty);
    int getQuantity() const;
    float getTotalPrice() const;
    float getTotalWeight() const;
};