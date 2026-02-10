#pragma once
#include "buy.hpp"
using namespace std;

class Check : public Buy
{
public:
    void printCheck() const;
    void printRow() const;
};