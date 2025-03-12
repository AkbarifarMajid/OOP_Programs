import mysql.connector

# اتصال به پایگاه داده
connection = mysql.connector.connect(
    host="localhost",  # یا اگر سرور شما در جای دیگری است، آدرس آن را وارد کنید.
    user="root",       # نام کاربری
    password="your_password"  # رمز عبور
)

cursor = connection.cursor()

# ایجاد پایگاه داده جدید
cursor.execute("CREATE DATABASE IF NOT EXISTS your_database")

# انتخاب پایگاه داده برای استفاده
cursor.execute("USE your_database")

print("connect is ok!")
