# Gradebook Grove
Status: retired

## Description
* This is a python program that acts as a gradebook mainly for students. It has:
    - Student menu for students to view their grades
    - Teacher menu for teachers to add (using excel file) and delete grades to their students
    - Admin menu for admins to add and delete users.
* This project was made mainly for understanding python, implementing data structures and algorithms using python and applying the principles of CRUD in a database with python.
* This project uses libraries such as [tkinter](https://docs.python.org/3/library/tkinter.html), [pandas](https://pandas.pydata.org/) and [pillow](https://pypi.org/project/pillow/). SQLite is used for the database

## Setup 
> Python (3.11.4 and above) and [Git](https://git-scm.com) must be installed on your computer.  
> Running this in a virtual environment is common practice and better to do so if you know how.

1.) Clone this repository
```bash
git clone https://github.com/adobong-sunog/gradebook-test
cd gradebook-test
```  
2.) Install required libraries
```python
pip install pandas
pip install pillow
```  
3.) Select main.py on your IDE then run the program 

(Bugs and default student, teacher and admin usernames and passwords are provided in INFO.txt)
  
## Acknowledgements
> For knowing how to uploade an excel file to SQLite to the program:
* [Upload A CSV File (Or Any Data File) To SQLite Using Python by Jie Jenn](https://www.youtube.com/watch?v=UZIhVmkrAEs)
* [Python Excel - Reading Excel files with Pandas read_excel by Very Academy](https://www.youtube.com/watch?v=bI68wnoINwc&t=306s)
> For learning how to use tkinter:
* [Tkinter docs](https://docs.python.org/3/library/tkinter.html)
* [The complete guide to tkinter playlist by Atlas](https://www.youtube.com/watch?v=OfAqWspoBb4&list=PLpMixYKO4EXeaGnqT_YWx7_mA77bz2VqM)
* [Create Graphical User Interfaces With Python And TKinter playlist by Codemy.com](https://www.youtube.com/watch?v=yQSEXcf6s2I&list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV)