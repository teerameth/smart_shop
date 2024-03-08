# Smart Shop
**Smart Shop** is an **Inventory Management System** developed using Flask and SQLAlchemy

### Prerequisites
```shell
mkvirtualenv smart_shop
workon smart_shop
pip install -r requirements.txt
```

### Setup database
```shell
# Create database table
python database_setup.py
# generate users list
python gen_student.py
# generate assets list
python gen_tool.py
# generate create/request/approve events
python gen_list.py
```

### Bring up the server
```shell
# Use Flask to run with port 5000
flask --app finalProject run --host=0.0.0.0
# Or use system Python3 to run with port 80
sudo python3 finalProject.py
```



![](docs/images/admin_login.png)

![](docs/images/admin_inspect_request.png)

![](docs/images/admin_inspect_lent.png)

![](docs/images/admin_inspect_return.png)

![](docs/images/admin_menu_bar.png)

![](docs/images/admin_manage_stock.png)

![](docs/images/admin_add_item.png)

![](docs/images/admin_export_history.png)

![](docs/images/student_login.png)

![](docs/images/student_inspect_request.png)

![](docs/images/student_inspect_lent.png)

![](docs/images/student_inspect_return.png)

![](docs/images/student_share.png)

![](docs/images/student_create_request.png)

![](docs/images/student_submit_recommendation.png)







