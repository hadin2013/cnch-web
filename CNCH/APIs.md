# School Group & Student API Documentation

این فایل مستندات کامل APIهای مربوط به **ساخت گروه، ثبت دانش‌آموز، ویرایش اطلاعات و داشبورد گروه** است.

---

## Base URL

`http://127.0.0.1:8000/user`

---

## 1️⃣ Create School Group

### ایجاد گروه (مرحله اول)

**Endpoint**

`POST /groups/`

### Request Body

```json
{
  "group_name": "گروه نخبگان",
  "province": "تهران",
  "city": "تهران",
  "school_name": "دبیرستان نمونه",
  "school_phone": "02112345678"
}
```

### Response Body (201 Created)

```json
{
  "id": 1,
  "group_name": "گروه نخبگان",
  "province": "تهران",
  "city": "تهران",
  "school_name": "دبیرستان نمونه",
  "school_phone": "02112345678"
}
```

---

## 2️⃣ Create Student

### ثبت دانش‌آموز (مرحله دوم)

**Endpoint**

`POST /students/`

### Request Body

```json
{
  "school_group": 1,
  "first_name": "علی",
  "last_name": "احمدی",
  "national_id": "1234567890",
  "phone_number": "09123456789",
  "grade": "دهم",
  "major": "ریاضی"
}
```

### Response Body (201 Created)

```json
{
  "id": 1,
  "school_group": 1,
  "first_name": "علی",
  "last_name": "احمدی",
  "national_id": "1234567890",
  "phone_number": "09123456789",
  "grade": "دهم",
  "major": "ریاضی"
}
```

⚠️ هر گروه حداکثر می‌تواند **۶ دانش‌آموز** داشته باشد.

---

## 3️⃣ Update Student

### ویرایش اطلاعات دانش‌آموز

**Endpoint**

`PATCH /students/{student_id}/`

### Request Body (Partial Update)

```json
{
  "phone_number": "09120000000",
  "grade": "یازدهم"
}
```

### Response Body (200 OK)

```json
{
  "id": 1,
  "school_group": 1,
  "first_name": "علی",
  "last_name": "احمدی",
  "national_id": "1234567890",
  "phone_number": "09120000000",
  "grade": "یازدهم",
  "major": "ریاضی"
}
```

---

## 4️⃣ Group Dashboard

### داشبورد گروه + لیست دانش‌آموزان

**Endpoint**

`GET /groups/{group_id}/`

### Response Body (200 OK)

```json
{
  "id": 1,
  "group_name": "گروه نخبگان",
  "province": "تهران",
  "city": "تهران",
  "school_name": "دبیرستان نمونه",
  "school_phone": "02112345678",
  "students": [
    {
      "id": 1,
      "first_name": "علی",
      "last_name": "احمدی",
      "national_id": "1234567890",
      "phone_number": "09120000000",
      "grade": "یازدهم",
      "major": "ریاضی"
    }
  ]
}
```

---

## 🔐 Notes

* تمام URLها باید **Trailing Slash** داشته باشند (`/`)
* مناسب برای اتصال مستقیم به Front-end

---

## ✅ Status Codes

| Code | Description      |
| ---- | ---------------- |
| 201  | Created          |
| 200  | Success          |
| 400  | Validation Error |
| 404  | Not Found        |

---