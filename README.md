# Job Portal - Full-Stack Django Web Application

A complete job portal with role-based access for Job Seekers and Recruiters.

## Tech Stack

- **Backend:** Django (latest stable)
- **Database:** SQLite (default)
- **Frontend:** HTML, CSS, Bootstrap 5
- **Authentication:** Django built-in auth
- **File Upload:** Resume (PDF only), profile picture

## Project Structure

```
jobportal/
├── manage.py
├── requirements.txt
├── jobportal/           # project config
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── accounts/             # user management & profiles
├── jobs/                 # job postings
├── applications/         # job applications
├── templates/
├── static/
└── media/
```

## Run Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run migrations

```bash
python manage.py migrate
```

### 3. Create superuser (admin)

```bash
python manage.py createsuperuser
```

### 4. Start the server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

- **Admin panel:** http://127.0.0.1:8000/admin/

## User Roles

- **Job Seeker:** Browse jobs, search/filter, apply with PDF resume, view application status.
- **Recruiter:** Post, edit, delete jobs; view applicants; set application status (Pending/Accepted/Rejected).
- **Admin:** Full access via Django admin (users, jobs, applications).

## Features

- Registration with role selection (Job Seeker / Recruiter)
- Login / Logout
- Job listing with pagination, search by title, filter by location
- Recruiter dashboard: post, edit, delete jobs; view applicants; update status
- Job seeker dashboard: my applications, apply with PDF resume
- Profile: phone, profile picture
- CSRF protection, login-required for post/apply, role-based permissions

## JWT API

REST API with JWT authentication is available under `/api/`.

### Install API dependencies

Already included in `requirements.txt`:
- `djangorestframework`
- `djangorestframework-simplejwt`

### Token endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Obtain access + refresh token (send `username`, `password`) |
| POST | `/api/token/refresh/` | Get new access token (send `refresh` in body) |
| POST | `/api/token/verify/` | Verify a token (send `token` in body) |

### Example: get tokens

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Example: call protected endpoint with JWT

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://127.0.0.1:8000/api/me/
```

### API endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/jobs/` | No | List active jobs (paginated) |
| GET | `/api/jobs/<id>/` | No | Job detail |
| GET | `/api/me/` | JWT required | Current user profile |

- **Access token lifetime:** 60 minutes  
- **Refresh token lifetime:** 7 days  
- Use header: `Authorization: Bearer <access_token>`
