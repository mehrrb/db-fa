# پروژه وارد کردن CSV به دیتابیس

این پروژه برای وارد کردن داده‌های محصولات از فایل CSV به دیتابیس PostgreSQL طراحی شده است.

## ساختار پروژه

- `core/models.py`: مدل محصول برای ذخیره داده‌ها در دیتابیس
- `core/import_csv.py`: اسکریپت برای وارد کردن داده‌ها از CSV به دیتابیس
- `core/views.py`: ویوها برای نمایش محصولات
- `core/templates/core/product_list.html`: قالب برای نمایش لیست محصولات

## نحوه راه‌اندازی

1. ابتدا یک دیتابیس PostgreSQL ایجاد کنید:
```sql
CREATE DATABASE db_fa;
```

2. متغیرهای محیطی زیر را تنظیم کنید یا از مقادیر پیش‌فرض استفاده کنید:
```
DB_NAME=db_fa
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

3. مهاجرت‌ها را اجرا کنید:
```
python manage.py makemigrations
python manage.py migrate
```

4. یک کاربر ادمین ایجاد کنید:
```
python manage.py createsuperuser
```

5. برای وارد کردن داده‌ها از CSV به دیتابیس:
```
python core/import_csv.py
```

6. سرور توسعه را اجرا کنید:
```
python manage.py runserver
```

7. به آدرس زیر بروید:
   - http://127.0.0.1:8000/ - نمایش محصولات
   - http://127.0.0.1:8000/admin/ - پنل مدیریت 