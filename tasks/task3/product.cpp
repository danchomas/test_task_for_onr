#include "product.hpp"
#include <stdexcept>
using namespace std;

Product::Product() : price(0.0f), weight(0.0f) {}

void Product::setName(const string &n)
{
    if (n.empty())
        throw invalid_argument("нужно не пустое");
    if (n.length() > 30)
        throw invalid_argument("слишком большое");
    name = n;
}

void Product::setCategory(const string &c)
{
    if (c.empty())
        throw invalid_argument("не пустая");
    if (c.length() > 30)
        throw invalid_argument("слишком длинное название");
    category = c;
}

void Product::setPrice(float p)
{
    if (p < 0)
        throw invalid_argument("положительное надо");
    price = p;
}

void Product::setWeight(float w)
{
    if (w < 0)
        throw invalid_argument("положительное надо");
    weight = w;
}

string Product::getName() const { return name; }
string Product::getCategory() const { return category; }
float Product::getPrice() const { return price; }
float Product::getWeight() const { return weight; }