#!/usr/bin/env python
# — coding: utf-8 —
from editor import Editor
from database_setup import db, Tool_list, Student, Tool, Tool_group, Association, Order
editor = Editor()

tools = editor.list_tool_by_type(editor.list_all_type_of_tool()[1])
tool1 = tools[1]
tool2 = tools[2]

if tool1.group_id == None:
    group = Tool_group(main_tool = tool1)
    tool1.group = group
group = tool1.group
# Check ว่ามี suggested_tool นั้นอยู่เเล้วมั้ยจะได้ไม่ใส่ซํ้า
already = []
for item in group.tools: already.append(item.tool) #group.tools เป็น Association ซึ่งมีสมาชิกที่เป็น Tool อยู่ด้านใน เรียกใช้ด้วย Association.tool
if tool2 not in already:
    a = Association()
    a.tool = tool2
    group.tools.append(a)

print(group.main_tool)
print(tool1.group)
print(tool1.tool_groups)

for item in tool1.group.tools:
    print(item.tool.name)

print(tool1.group.main_tool[0].name)