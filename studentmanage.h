#ifndef STUDENTMANAGE_H
#define STUDENTMANAGE_H
#include <iostream>
#include "student.h"
using namespace std;

class StudentManage
{
public:
    StudentManage();
    Student     students[10];
    void        MainView();
    void        AddStudent();
    void        DetStudent();
    void        ShowStudent();
};
#endif