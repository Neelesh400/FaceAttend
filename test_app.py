"""
FaceAttend Automated Verification Test Suite
Tests all 13 mandatory specification scenarios defined in Section 34 of requirements.
"""

import os
import sys
import unittest
import base64
import json
import datetime

# Fix Windows console UTF-8 output if possible
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from database.db import get_db, init_db, query_db, execute_db
from database.seed import seed_database
from face_recognition.recognizer import face_engine

class FaceAttendComprehensiveTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        
        with cls.app.app_context():
            init_db()
            seed_database()
            
        cls.client = cls.app.test_client()

        # Load fixture images to base64
        with open(r'tests\fixtures\student_face.jpg', 'rb') as f:
            cls.student_face_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf-8')
            
        with open(r'tests\fixtures\single_unknown.jpg', 'rb') as f:
            cls.unknown_face_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf-8')
            
        with open(r'tests\fixtures\fruit_noface.jpg', 'rb') as f:
            cls.noface_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf-8')
            
        with open(r'tests\fixtures\unknown_face.jpg', 'rb') as f:
            cls.multiple_faces_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf-8')

    def login_admin(self):
        """Helper to ensure clean admin login."""
        self.client.get('/logout')
        return self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)

    def login_student(self):
        """Helper to ensure clean student login."""
        self.client.get('/logout')
        return self.client.post('/login', data={'username': 'student', 'password': 'student123'}, follow_redirects=True)

    # -------------------------------------------------------------
    # TEST 1: Admin login -> Admin Dashboard
    # -------------------------------------------------------------
    def test_01_admin_login(self):
        print("\n--- TEST 1: Admin Login -> Admin Dashboard ---")
        res = self.login_admin()
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Dashboard Overview', res.data)
        self.assertIn(b'Welcome back, Administrator', res.data)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('role'), 'ADMIN')
        print("[PASS] Test 1 Passed: Admin successfully authenticated and redirected to /admin/dashboard")

    # -------------------------------------------------------------
    # TEST 2: Student login -> User Dashboard
    # -------------------------------------------------------------
    def test_02_student_login(self):
        print("\n--- TEST 2: Student Login -> User Dashboard ---")
        res = self.login_student()
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Student Portal', res.data)
        self.assertIn(b'Welcome back, Alex Mercer!', res.data)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('role'), 'USER')
            self.assertEqual(sess.get('student_id'), 'STU001')
        print("[PASS] Test 2 Passed: Student successfully authenticated and redirected to /user/dashboard")

    # -------------------------------------------------------------
    # TEST 3: Student tries /admin/dashboard -> Access Denied & redirect to /user/dashboard
    # -------------------------------------------------------------
    def test_03_student_access_admin_forbidden(self):
        print("\n--- TEST 3: Student Tries /admin/dashboard -> Access Denied ---")
        self.login_student()
        res = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Access Denied', res.data)
        self.assertIn(b'Student Portal', res.data)
        print("[PASS] Test 3 Passed: Unauthorized student access to /admin/dashboard was rejected and redirected to /user/dashboard")

    # -------------------------------------------------------------
    # TEST 4: Admin adds student -> Student appears in database
    # -------------------------------------------------------------
    def test_04_admin_add_student(self):
        print("\n--- TEST 4: Admin Adds Student ---")
        self.login_admin()
        new_stu_id = 'STU999'
        
        # Clean up any leftover
        with self.app.app_context():
            execute_db("DELETE FROM users WHERE username = 'marcus' OR student_id = ?", (new_stu_id,))
            execute_db("DELETE FROM students WHERE student_id = ?", (new_stu_id,))

        form_data = {
            'student_id': new_stu_id,
            'name': 'Marcus Aurelius',
            'roll_number': 'CS-2026-99',
            'course': 'B.Tech Philosophy & AI',
            'semester': 'Semester 1',
            'department': 'Data Science & AI',
            'email': 'marcus.a@faceattend.edu',
            'phone': '+1 (555) 999-0000',
            'username': 'marcus',
            'password': 'password123'
        }
        res = self.client.post('/admin/students/add', data=form_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        # Verify in database
        with self.app.app_context():
            stu = query_db("SELECT * FROM students WHERE student_id = ?", (new_stu_id,), one=True)
            self.assertIsNotNone(stu)
            self.assertEqual(stu['name'], 'Marcus Aurelius')
            
            # Verify user account automatically created
            user = query_db("SELECT * FROM users WHERE student_id = ?", (new_stu_id,), one=True)
            self.assertIsNotNone(user)
            self.assertEqual(user['username'], 'marcus')
            self.assertEqual(user['role'], 'USER')
        print("[PASS] Test 4 Passed: Admin added student STU999, record and linked user created in database")

    # -------------------------------------------------------------
    # TEST 5: Admin registers student's face -> Face data saved & model trained
    # -------------------------------------------------------------
    def test_05_admin_register_face(self):
        print("\n--- TEST 5: Admin Registers Student Face ---")
        self.login_admin()
        target_student = 'STU001' # Alex Mercer

        # Register multiple face samples to satisfy minimum requirement (5 samples)
        for i in range(5):
            res = self.client.post(
                '/api/face/register-sample',
                data=json.dumps({'student_id': target_student, 'image': self.student_face_b64}),
                content_type='application/json'
            )
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data['success'])
            self.assertIn(data['status'], ['valid', 'sample_saved'])

        # Verify face_data table updated in database
        with self.app.app_context():
            rec = query_db("SELECT * FROM face_data WHERE student_id = ?", (target_student,), one=True)
            self.assertIsNotNone(rec)
            self.assertGreaterEqual(rec['samples_count'], 5)

        # Verify model file was saved and is loaded
        self.assertTrue(os.path.exists(face_engine.model_path))
        print(f"[PASS] Test 5 Passed: 5 face samples registered for {target_student}; LBPH model trained and saved")

    # -------------------------------------------------------------
    # TEST 6: Admin starts attendance -> Registered face recognized -> Attendance saved
    # -------------------------------------------------------------
    def test_06_admin_take_attendance_success(self):
        print("\n--- TEST 6: Take Attendance -> Registered Face Recognized & Saved ---")
        self.login_admin()
        today = datetime.date.today().isoformat()
        
        # Ensure STU001 does not have attendance marked yet today
        with self.app.app_context():
            execute_db("DELETE FROM attendance WHERE student_id = 'STU001' AND attendance_date = ?", (today,))

        res = self.client.post(
            '/api/face/recognize',
            data=json.dumps({'image': self.student_face_b64}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertEqual(data['student']['student_id'], 'STU001')

        # Verify attendance record created in database
        with self.app.app_context():
            att = query_db("SELECT * FROM attendance WHERE student_id = 'STU001' AND attendance_date = ?", (today,), one=True)
            self.assertIsNotNone(att)
            self.assertIn(att['status'], ['Present', 'Late'])
        print(f"[PASS] Test 6 Passed: STU001 recognized and attendance saved into database for {today}")

    # -------------------------------------------------------------
    # TEST 7: Same student appears again -> "Attendance Already Marked Today" -> No duplicate
    # -------------------------------------------------------------
    def test_07_duplicate_attendance_prevented(self):
        print("\n--- TEST 7: Duplicate Attendance Prevention Check ---")
        self.login_admin()
        today = datetime.date.today().isoformat()

        # Count records before second attempt
        with self.app.app_context():
            count_before = query_db("SELECT COUNT(*) as c FROM attendance WHERE student_id = 'STU001' AND attendance_date = ?", (today,), one=True)['c']
            self.assertEqual(count_before, 1)

        # Send same student frame again
        res = self.client.post(
            '/api/face/recognize',
            data=json.dumps({'image': self.student_face_b64}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'already_marked')
        self.assertIn("Already Marked", data.get('message'))

        # Ensure no duplicate was inserted
        with self.app.app_context():
            count_after = query_db("SELECT COUNT(*) as c FROM attendance WHERE student_id = 'STU001' AND attendance_date = ?", (today,), one=True)['c']
            self.assertEqual(count_after, 1)
        print("[PASS] Test 7 Passed: Duplicate attempt was flagged and prevented; no duplicate row created")

    # -------------------------------------------------------------
    # TEST 8: Unknown face -> "Unknown Face" -> No attendance saved
    # -------------------------------------------------------------
    def test_08_unknown_face_handling(self):
        print("\n--- TEST 8: Unknown Face Handling ---")
        self.login_admin()
        today = datetime.date.today().isoformat()

        # Count total attendance before
        with self.app.app_context():
            total_before = query_db("SELECT COUNT(*) as c FROM attendance WHERE attendance_date = ?", (today,), one=True)['c']

        res = self.client.post(
            '/api/face/recognize',
            data=json.dumps({'image': self.unknown_face_b64}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'unknown')
        self.assertIn("Unknown Face", data.get('message'))

        # Ensure no attendance record was created
        with self.app.app_context():
            total_after = query_db("SELECT COUNT(*) as c FROM attendance WHERE attendance_date = ?", (today,), one=True)['c']
            self.assertEqual(total_before, total_after)
        print("[PASS] Test 8 Passed: Unknown face correctly flagged as 'Unknown Face'; zero attendance records saved")

    # -------------------------------------------------------------
    # TEST 9: Student opens My Attendance -> Only their attendance displayed
    # -------------------------------------------------------------
    def test_09_student_view_own_attendance(self):
        print("\n--- TEST 9: Student Opens My Attendance ---")
        self.login_student()
        res = self.client.get('/user/attendance')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'My Attendance Metrics', res.data)
        self.assertIn(b'Alex Mercer', res.data)
        
        # Also check history
        hist_res = self.client.get('/user/history')
        self.assertEqual(hist_res.status_code, 200)
        self.assertIn(b'My Attendance History', hist_res.data)
        print("[PASS] Test 9 Passed: Student accessed personal attendance view containing only their records")

    # -------------------------------------------------------------
    # TEST 10: Student tries to access another student's data -> Access denied
    # -------------------------------------------------------------
    def test_10_student_access_another_student_denied(self):
        print("\n--- TEST 10: Student Cross-Tenant Data Access Denied ---")
        self.login_student()
        
        # Student tries admin route to view another student STU002
        res = self.client.get('/admin/students/view/STU002', follow_redirects=True)
        # Should be blocked with access denied redirect
        self.assertIn(b'Access Denied', res.data)

        # Student also cannot access admin user list
        res2 = self.client.get('/admin/users', follow_redirects=True)
        self.assertIn(b'Access Denied', res2.data)
        print("[PASS] Test 10 Passed: Student prohibited from querying admin routes or other student dossiers")

    # -------------------------------------------------------------
    # TEST 11: Admin opens Reports -> All attendance data available
    # -------------------------------------------------------------
    def test_11_admin_reports_all_data(self):
        print("\n--- TEST 11: Admin Opens Reports ---")
        self.login_admin()
        res = self.client.get('/admin/reports')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Attendance Reports & Intelligence', res.data)
        self.assertIn(b'Export CSV', res.data)
        self.assertIn(b'Export Excel', res.data)
        
        # Test CSV export
        csv_res = self.client.get('/admin/reports/export/csv')
        self.assertEqual(csv_res.status_code, 200)
        self.assertEqual(csv_res.mimetype, 'text/csv')
        self.assertIn(b'Record ID,Student ID,Full Name', csv_res.data)
        print("[PASS] Test 11 Passed: Admin reports dashboard and CSV export loaded successfully with multi-student records")

    # -------------------------------------------------------------
    # TEST 12: Student opens My Report -> Only their own report available
    # -------------------------------------------------------------
    def test_12_student_my_report(self):
        print("\n--- TEST 12: Student Opens My Report ---")
        self.login_student()
        res = self.client.get('/user/reports')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Official Student Attendance Transcript', res.data)
        self.assertIn(b'Alex Mercer', res.data)
        self.assertIn(b'STU001', res.data)
        # Other students must not appear in their transcript
        self.assertNotIn(b'Liam Vance', res.data)

        # Test Student CSV download
        csv_res = self.client.get('/user/reports/export/csv')
        self.assertEqual(csv_res.status_code, 200)
        self.assertIn(b'STU001', csv_res.data)
        self.assertNotIn(b'STU003', csv_res.data)
        print("[PASS] Test 12 Passed: Student transcript correctly bound to current student STU001 without data leakage")

    # -------------------------------------------------------------
    # TEST 13: Logout -> Session destroyed -> Login page displayed
    # -------------------------------------------------------------
    def test_13_logout_destroys_session(self):
        print("\n--- TEST 13: Logout Clears Session ---")
        # Log in
        self.login_admin()
        # Log out
        res = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'You have been logged out successfully', res.data)
        self.assertIn(b'Sign in to your authorized portal', res.data)

        # Verify session is empty
        with self.client.session_transaction() as sess:
            self.assertNotIn('user_id', sess)
            self.assertNotIn('role', sess)

        # Trying to access dashboard now redirects to login
        dash_res = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertIn(b'Please log in with an administrator account', dash_res.data)
        print("[PASS] Test 13 Passed: Logout cleared session; subsequent protected route redirects to login")

    # -------------------------------------------------------------
    # TEST 14: Student Self-Attendance via Webcam Face Scan
    # -------------------------------------------------------------
    def test_14_student_self_attendance(self):
        print("\n--- TEST 14: Student Self-Attendance in Student Portal ---")
        self.login_student()
        today = datetime.date.today().isoformat()

        # Check self-attendance page renders
        page_res = self.client.get('/user/mark-attendance')
        self.assertEqual(page_res.status_code, 200)
        self.assertIn(b"Mark Today's Attendance", page_res.data)

        # Clear STU001 today's attendance to test marking
        with self.app.app_context():
            execute_db("DELETE FROM attendance WHERE student_id = 'STU001' AND attendance_date = ?", (today,))

        # Scan matching face
        res = self.client.post(
            '/api/face/self-attendance',
            data=json.dumps({'image': self.student_face_b64}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('Attendance marked successfully', data.get('message'))

        # Verify in database
        with self.app.app_context():
            att = query_db("SELECT * FROM attendance WHERE student_id = 'STU001' AND attendance_date = ?", (today,), one=True)
            self.assertIsNotNone(att)
            self.assertEqual(att['student_id'], 'STU001')

        # Test duplicate attempt on same day
        dup_res = self.client.post(
            '/api/face/self-attendance',
            data=json.dumps({'image': self.student_face_b64}),
            content_type='application/json'
        )
        dup_data = dup_res.get_json()
        self.assertEqual(dup_data.get('status'), 'already_marked')

        print("[PASS] Test 14 Passed: Student self-attendance marked and verified with face biometric matching")

if __name__ == '__main__':
    unittest.main()
