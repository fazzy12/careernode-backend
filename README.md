# CareerNode API 🚀

**CareerNode** is a robust backend API designed to power modern job board platforms. It facilitates seamless connections between talent and employers through secure role-based access control, efficient job data management, and optimized search capabilities.

## 🛠 Tech Stack
* **Framework:** Django & Django REST Framework (DRF)
* **Database:** PostgreSQL (Production) / SQLite (Dev)
* **Authentication:** JWT (JSON Web Tokens) via `rest_framework_simplejwt`
* **Documentation:** Swagger / Redoc (`drf-yasg`)
* **Hosting:** Render/Railway (TBD)

## 🌟 Key Features
* **User Management:** Role-based authentication (Admin vs. Standard User/Applicant).
* **Job Operations:** CRUD endpoints for Job Postings and Categories.
* **Optimized Search:** High-performance filtering by location, industry, and job type using database indexing.
* **Security:** Secure password handling and token-based session management.
* **Documentation:** Fully interactive API documentation via Swagger UI.

## 🏗️ Architecture & Database
* [Link to ERD Diagram] (To be added)
* Normalized database schema designed for scalability.

## 🚀 Local Setup & Installation

You can run **CareerNode** easily using Docker (recommended) or manually using a virtual environment.

### Prerequisites
* **Git**
* **Docker Desktop** (if running with Docker)
* **Python 3.8+** & **PostgreSQL** (if running manually)

---

### Method 1: Using Docker 🐳 (Recommended)
This guarantees the environment matches production exactly, including the PostgreSQL database.

**1. Clone the Repository**
```bash
git clone [https://github.com/YOUR-USERNAME/careernode-backend.git](https://github.com/fazzy12/careernode-backend.git)
```

```
cd careernode-backen
```