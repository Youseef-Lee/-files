#include "studentmanage.h"

StudentManage::StudentManage()
{
    for(int i=0;i<10;i++)
    {
        students[i].id=0;
        students[i].score=0;
        students[i].name="";
    }
}
void StudentManage::MainView()
{
    string chooseid;
    while(1)
    {
        cout<<"*********学生管理系统**********"<<endl;
        cout<<"1 添加学员信息"<<endl;
        cout<<"2 删除学员信息"<<endl;
        cout<<"3 查看学员信息"<<endl;
        cout<<"4 退出系统"<<endl;
        cout<<"******************************"<<endl;
        cout<<"请输入您的选项："<<endl;
        cin>>chooseid;
        if(chooseid == "1")
        {
            AddStudent();
        }
        else if(chooseid == "2")
        {
            DetStudent();
        }
        else if(chooseid == "3")
        {
            ShowStudent();
        }
        else if(chooseid == "4")
        {
            return ;
        }
        else
        {
            cout<<"您输入的选项有误，请重新输入"<<endl;
        }
    }
}
void StudentManage::AddStudent()
{
    int sum=0;
    for(int i=0;i<10;i++)
    {
        if(students[i].id != 0)
        {
            sum++;
        }
    }
    if(sum==10)
    {
        cout<< "学生数量已达上限，停止添加学员"<<endl;
        return;
    }
    cout<< "请输入您要添加的学员学号："<<endl;
    int inputid;
    cin>>inputid;
    for(int i=0;i<10;i++)
    {
        if(students[i].id == inputid)
        {
            cout<<"当前学号的学员已经录入，是否继续录入(y/n)"<<endl;
            string chooseif;
            cin>>chooseif;
            if(chooseif == "y")
            {
                cout<<"请输入学生姓名："<<endl;
                cin>>students[i].name;
                cout<<"请输入学员成绩："<<endl;
                cin>>students[i].score;
            }
            return ;
        }
    }
    for(int i=0;i<10;i++)
    {
        if(students[i].id == 0)
        {
            students[i].id=inputid;
            cout<<"请输入学生姓名："<<endl;
            cin>>students[i].name;
            cout<<"请输入学员成绩："<<endl;
            cin>>students[i].score;
            return ;
        }
    }
}
void StudentManage::DetStudent()
{}
void StudentManage::ShowStudent()
{}