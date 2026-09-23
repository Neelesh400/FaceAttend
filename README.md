# FaceAttend — Face Recognition Attendance Management System

**FaceAttend** is an enterprise-grade, modern, and fully working biometric attendance management web application. Built with **Python Flask**, **OpenCV**, and **SQLite**, it features **two completely separate, role-protected dashboards** for **Administrators** and **Students/Users**.

---

## 🌟 Key Highlights & Architecture

- **Two Distinct Dashboards**:
  - **Admin Dashboard (`/admin/dashboard`)**: Full institutional control, student CRUD, biometric face enrollment, live webcam scanner, attendance logs, analytics charts, user permissions, and report exports.
  - **User/Student Dashboard (`/user/dashboard`)**: Student-friendly, personal attendance rates, chronological history, certificate transcripts, and safe profile updates.
- **Strict Role-Based Access Control (RBAC)**:
  - Backend Flask session authentication with password hashing (`werkzeug.security`).
  - Strict route protection decorators: unauthorized cross-dashboard navigation is blocked with *"Access Denied"* alerts.
- **Computer Vision & Biometrics**:
  - Powered by **OpenCV** (Haar Cascade detection + **LBPH Face Recognizer**).
  - Works **100% locally and offline on Windows** with zero external cloud dependencies.
  - Multi-sample face enrollment (5–10 quality samples per student).
  - Real-time duplicate attendance prevention: checks `(student_id, attendance_date)` at the database level and returns *"Attendance Already Marked Today"*.
  - Unknown face rejection: unmapped or low-confidence faces display *"Unknown Face"* without marking attendance.
- **Dynamic Analytics**:
  - Interactive **Chart.js** charts (Weekly attendance trends, department breakdowns, and student donut graphs).
  - All metrics are calculated live from the SQLite database.
- **Export Formats**:
  - Instant **CSV export**, styled **Excel (.xlsx)** export via `openpyxl`, and print-friendly styling for official transcripts.
- **Modern UI / UX**:
  - Responsive Bootstrap 5 layout with glassmorphism touches, FontAwesome 6 icons, dark/light theme switcher with `localStorage` persistence, and toast notifications.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python 3.10+ / 3.13 / 3.14, Flask 3.1, Werkzeug |
| **Computer Vision** | OpenCV (`opencv-contrib-python`), NumPy |
| **Database** | SQLite 3 with Foreign Keys & Unique Constraints |
| **Export Tools** | `openpyxl`, Python `csv` |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, FontAwesome 6.5 |
| **Data Viz** | Chart.js 4.4 |

---

## 🚀 Quick Start Guide (Windows)

Follow these exact commands in **PowerShell** or **Command Prompt**:

### 1. Clone or Navigate to Project Directory
```powershell
cd "d:\PYTHON PROJECT GSP"
```

### 2. Create and Activate Virtual Environment (Recommended)
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Seed Initial Demo Data (First-Time Setup)
```powershell
python database/seed.py
```

### 5. Launch Application
```powershell
python app.py
```

### 6. Open in Browser
Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔑 Demo Credentials

| Role | Username / Student ID | Password | Access Portal |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | `/admin/dashboard` |
| **Student / User** | `student` *(or `STU001`)* | `student123` | `/user/dashboard` |

> [!WARNING]
> These credentials are pre-seeded for development and demonstration. Change all passwords before deploying to production!

---

## 📋 Role-Based Permissions Matrix

| Feature | Admin | Student / User |
| :--- | :---: | :---: |
| **Dashboard** | ✅ Yes | ✅ Yes (Personal Only) |
| **View All Students** | ✅ Yes | ❌ No |
| **Add / Edit / Delete Student** | ✅ Yes | ❌ No |
| **Enroll / Delete Face Biometrics** | ✅ Yes | ❌ No |
| **Live Facial Attendance Scanner** | ✅ Yes | ❌ No |
| **Master Attendance Records** | ✅ Yes | ❌ No |
| **View Own Attendance & History** | ✅ Yes | ✅ Yes (Strictly Read-Only) |
| **Export Master CSV / Excel** | ✅ Yes | ❌ No |
| **User Account & Password Management** | ✅ Yes | ❌ No |
| **System Settings & Cutoff Rules** | ✅ Yes | ❌ No |
| **Update Safe Profile (Phone/Email/Password)** | ✅ Yes | ✅ Yes |

---

## 📸 Face Recognition Workflow

### 1. Face Registration (`/admin/register-face`)
1. Admin selects an enrolled student from the dropdown.
2. Click **Start Webcam** to initialize the browser camera.
3. The engine uses Haar Cascade detection to validate:
   - *No face*: "No face detected. Please position your face correctly."
   - *Multiple faces*: "Multiple faces detected. Please ensure only one person is visible."
   - *Valid face*: Captures 5 to 6 normalized face samples with live progress bar.
4. Once completed, the LBPH model trains and saves automatically to `face_recognition/models/face_model.xml`.

### 2. Live Attendance Scanner (`/admin/take-attendance`)
1. Admin clicks **Start Scanner**.
2. Frames are analyzed continuously:
   - **Recognized**: Bounding box turns **Green**, student card pops up with audio chime, and attendance is saved into SQLite.
   - **Duplicate (Same Day)**: Bounding box turns **Orange**, displays *"Attendance Already Marked Today"*, and prevents duplicate row insertion.
   - **Unknown**: Bounding box turns **Red**, displays *"Unknown Face"*, no attendance is saved, and a quick link to register the face is shown.

---

## 📊 Reports & Exports (`/admin/reports`)

- **Presets**: Daily, Weekly (7 Days), Monthly (30 Days), and Custom Date Ranges.
- **Filters**: By Department or Individual Student.
- **Visual Analytics**: Interactive Pie/Donut breakdown (Present vs Late vs Absent) and Department Bar charts.
- **Exports**:
  - Download formatted `.csv`
  - Download styled `.xlsx` workbook (with color-coded attendance badges)
  - One-click print-optimized view

---

## 🔒 Biometric Privacy & Security

1. **Local Processing**: Facial crops and embeddings are stored and processed on the local server filesystem and database. No biometric data is sent to third-party cloud APIs.
2. **Right to Erasure**: Administrators can delete biometric samples and models at any time with immediate model retraining.
3. **Defense Against SQL Injection**: All queries use parameterized SQLite statements.
4. **Credential Safety**: Passwords use PBKDF2 with SHA-256 via Werkzeug.

---

## 🧪 Automated Testing

The repository includes an automated test suite verifying all 13 test cases specified in the project requirements:

```powershell
python test_app.py
```

### Verified Test Cases:
- **TEST 1**: Admin login redirects to Admin Dashboard
- **TEST 2**: Student login redirects to User Dashboard
- **TEST 3**: Student unauthorized URL access to `/admin/...` rejected with *Access Denied*
- **TEST 4**: Admin student creation with automated portal user creation
- **TEST 5**: Face sample registration and LBPH model compilation
- **TEST 6**: Live webcam recognition and attendance database recording
- **TEST 7**: Duplicate daily attendance prevention check
- **TEST 8**: Unknown face detection and rejection
- **TEST 9**: Student personal attendance metrics isolation
- **TEST 10**: Cross-tenant authorization barrier enforcement
- **TEST 11**: Admin master reports and CSV/Excel generation
- **TEST 12**: Student attendance transcript isolation
- **TEST 13**: Session destruction on logout

---

## 💡 Troubleshooting & Camera Permissions

- **Camera Not Starting in Browser**:
  - Modern browsers require HTTPS or `localhost` / `127.0.0.1` for webcam access (`navigator.mediaDevices.getUserMedia`). Ensure you are accessing `http://127.0.0.1:5000`.
  - Check browser permissions (click the camera icon in the URL bar to allow camera access).
  - Ensure other applications (Zoom, Teams, Skype) are not locking the webcam device.
- **Database Reset**:
  - If you ever want a fresh database, delete `database/database.db` and run `python database/seed.py`.

---

## 📁 Project Directory Structure

```
face_attendance/
├── app.py                     # Flask application factory and server runner
├── config.py                  # System configuration and parameters
├── requirements.txt           # Python dependency specification
├── test_app.py                # 13-scenario automated test suite
├── README.md                  # Comprehensive documentation
├── database/
│   ├── schema.sql             # SQL table definitions and indexes
│   ├── db.py                  # Database connection manager
│   ├── seed.py                # Demo accounts & attendance seeder
│   └── database.db            # SQLite database file
├── face_recognition/
│   ├── detector.py            # Haar cascade face detector & preprocessor
│   ├── recognizer.py          # LBPH model trainer & predictor
│   └── models/                # Trained XML models & cascades
├── routes/
│   ├── auth.py                # Login, logout, session logic
│   ├── admin.py               # Admin dashboard, students, records, reports
│   ├── user.py                # Student dashboard, profile, history
│   └── api.py                 # REST APIs for face registration & recognition
├── templates/
│   ├── base.html              # Core HTML shell & theme provider
│   ├── auth/login.html        # Role-based login screen
│   ├── admin/                 # Dedicated Admin templates
│   └── user/                  # Dedicated Student templates
└── static/
    ├── css/                   # Stylesheets (style.css, admin.css, user.css)
    ├── js/                    # Client scripts (scanner, charts, registration)
    └── images/                # Brand vectors and icons
```

---
&copy; 2026 FaceAttend System. Built for Modern Educational Institutions.
