#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <iomanip>
#include <nlohmann/json.hpp>
#include "check.hpp"

using json = nlohmann::json;
using namespace std;

void loadData(vector<Check> &products, const string &filename)
{
    ifstream file(filename);
    if (!file.is_open())
    {
        cout << "файл не найден" << endl;
        return;
    }

    json j;
    try
    {
        file >> j;
    }
    catch (...)
    {
        cout << "файл не читается" << endl;
        return;
    }

    products.clear();
    for (const auto &item : j)
    {
        Check p;
        if (item.contains("name") && item.contains("category"))
        {
            p.setName(item.at("name").get<string>());
            p.setCategory(item.at("category").get<string>());
            p.setPrice(item.at("price").get<float>());
            p.setWeight(item.at("weight").get<float>());
            products.push_back(p);
        }
    }
}

void saveData(const vector<Check> &products, const string &filename)
{
    json j = json::array();
    for (const auto &p : products)
    {
        j.push_back({{"name", p.getName()},
                     {"category", p.getCategory()},
                     {"price", p.getPrice()},
                     {"weight", p.getWeight()}});
    }
    ofstream file(filename);
    if (file.is_open())
    {
        file << j.dump(4);
    }
}

void printTable(const vector<Check> &products)
{
    cout << "\n"
         << left << setw(5) << "id" << setw(20) << "название" << setw(15) << "категория"
         << setw(10) << "цена" << setw(10) << "Вес" << endl;
    for (size_t i = 0; i < products.size(); ++i)
    {
        cout << setw(5) << i;
        products[i].printRow();
    }
}

int main()
{
    vector<Check> products;
    string filename = "products.json";
    loadData(products, filename);

    while (true)
    {
        cout << "\n1. список товаров";
        cout << "\n2. сортировать список";
        cout << "\n3. редактировать товар";
        cout << "\n4. чек по товару";
        cout << "\n5. поиск";
        cout << "\n7. выход";
        cout << "\nВыберите действие: ";

        int choice;
        cin >> choice;

        if (choice == 1)
        {
            printTable(products);
        }
        else if (choice == 2)
        {
            cout << "сортировать по 1 цене 2 названию 3 категории: ";
            int sortType;
            cin >> sortType;

            if (sortType == 1)
                sort(products.begin(), products.end(), [](const Check &a, const Check &b)
                     { return a.getPrice() < b.getPrice(); });
            else if (sortType == 2)
                sort(products.begin(), products.end(), [](const Check &a, const Check &b)
                     { return a.getName() < b.getName(); });
            else if (sortType == 3)
                sort(products.begin(), products.end(), [](const Check &a, const Check &b)
                     { return a.getCategory() < b.getCategory(); });
            printTable(products);
        }
        else if (choice == 3)
        {
            int id;
            cout << "введите id товара для редактирования ";
            cin >> id;
            if (id >= 0 && id < (int)products.size())
            {
                string s;
                float f;
                cout << "новое название ";
                cin >> s;
                products[id].setName(s);
                cout << "новая цена ";
                cin >> f;
                products[id].setPrice(f);
                cout << "новый вес ";
                cin >> f;
                products[id].setWeight(f);
                cout << "данные обновлены" << endl;
            }
        }
        else if (choice == 4)
        {
            int id, qty;
            cout << "введите id товара";
            cin >> id;
            if (id >= 0 && id < (int)products.size())
            {
                cout << "количество";
                cin >> qty;
                products[id].setBuyData(qty);
                products[id].printCheck();
            }
        }
        else if (choice == 5)
        {
            string q;
            cout << "введите название или категорию";
            cin >> q;
            for (const auto &p : products)
            {
                if (p.getName() == q || p.getCategory() == q)
                    p.printRow();
            }
        }
        else if (choice == 6)
        {
            saveData(products, filename);
            break;
        }
        else
        {
            cout << "неверный ввод, экстренное завершение программы" << endl;
            break;
        }
    }
    return 0;
}