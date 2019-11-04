#!/usr/bin/env python
# — coding: utf-8 —
from editor import Editor
from database_setup import db, Tool_list, Student, Tool, Tool_group, Association, Order
editor = Editor()

tools = editor.tool.list_by_type(editor.tool.list_all_type()[1])
tool1 = tools[1]
tool2 = tools[2]

print(tool1.group)
if tool1.group == None:
    group = Tool_group()
    tool1.group = group
else:
    group = tool1.group
a=Association()
a.tool = tool2
group.tools.append(a)

print(tool1.group)

for item in tool1.group.tools:
    print(item.tool)

print(tool1.group.main_tool)