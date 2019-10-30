#!/usr/bin/env python
# — coding: utf-8 —
from editor import Editor
editor = Editor()
default_password = "12345678"
student_type = ["ปริญญาตรี", "ปริญญาโท", "ปริญญาเอก", "อื่น ๆ"]
editor.student.create_new_student() # password, student_university_ID, name, surname, student_type, student_year, phone_number



