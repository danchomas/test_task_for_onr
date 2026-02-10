#include "check.hpp"
#include <iostream>
#include <iomanip>
using namespace std;

void Check::printCheck() const
{
    cout << "продукт: " << getName() << endl;
    cout << "категория: " << getCategory() << endl;
    cout << "количество: " << getQuantity() << endl;
    cout << "общий вес: " << getTotalWeight() << endl;
    cout << "общая цена: " << getTotalPrice() << endl;
}

void Check::printRow() const
{
    cout << left << setw(20) << getName()
         << setw(15) << getCategory()
         << setw(10) << getPrice()
         << setw(10) << getWeight() << endl;
}