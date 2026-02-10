#pragma once
#include <string>
using namespace std;

class Product
{
private:
    string name;
    string category;
    float price;
    float weight;

public:
    Product();
    void setName(const string &n);
    void setCategory(const string &c);
    void setPrice(float p);
    void setWeight(float w);

    string getName() const;
    string getCategory() const;
    float getPrice() const;
    float getWeight() const;
};