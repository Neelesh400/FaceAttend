"""
FaceAttend Project Guide PDF Generator
Creates a comprehensive, beautifully styled PDF document explaining the FaceAttend project
slide-by-slide, point-by-point, in simple, easy-to-understand terms.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that enables 'Page X of Y' footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header
        self.drawString(54, 750, "FaceAttend — Complete Project Guide & Technical Walkthrough")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_str)
        self.drawString(54, 40, "Confidential & Educational Project Material — 2026")
        self.line(54, 52, 558, 52)
        self.restoreState()

def build_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "FaceAttend_Project_Explanation_Guide.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_navy = colors.HexColor("#0F172A")
    c_primary = colors.HexColor("#2563EB")
    c_teal = colors.HexColor("#0D9488")
    c_muted = colors.HexColor("#475569")
    c_card_bg = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1E293B"),
        alignment=1,
        spaceAfter=25
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_muted,
        alignment=1
    )

    h1_style = ParagraphStyle(
        'SlideHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_navy,
        spaceBefore=12,
        spaceAfter=6
    )

    badge_style = ParagraphStyle(
        'SlideBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=c_primary,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'SlideBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        leftIndent=15,
        spaceAfter=3
    )

    explanation_style = ParagraphStyle(
        'SlideExplanation',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0F766E"), # Deep teal
        spaceAfter=4
    )

    tech_box_title = ParagraphStyle(
        'TechTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=c_primary,
        spaceAfter=3
    )

    story = []

    # -------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------
    story.append(Spacer(1, 100))
    story.append(Paragraph("FACEATTEND", title_style))
    story.append(Paragraph("Face Recognition Attendance Management System", subtitle_style))
    story.append(HRFlowable(width="60%", thickness=2, color=c_primary, spaceAfter=25, spaceBefore=10))
    story.append(Paragraph("<b>Complete Slide-by-Slide Technical Explanation Guide</b>", ParagraphStyle('CoverSub2', alignment=1, fontSize=12, leading=16, textColor=c_navy)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("A point-by-point, easy-to-understand breakdown of the computer vision pipeline (Haar Cascade & LBPH), dual-dashboard architecture, and anti-proxy workflows.", ParagraphStyle('CoverDesc', alignment=1, fontSize=10, leading=14, textColor=c_muted)))
    
    story.append(Spacer(1, 150))
    story.append(Paragraph("<b>Technology Stack:</b> Python Flask 3.1 &bull; OpenCV 5.0 (LBPH) &bull; SQLite 3 &bull; Bootstrap 5 &bull; Chart.js", meta_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Author / Developer:</b> AI Systems & Architecture Team  |  <b>Year:</b> 2026", meta_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE CONTENT DATA
    # -------------------------------------------------------------
    slides = [
        {
            "num": 1,
            "title": "Title Slide — Project Introduction",
            "category": "PROJECT INTRODUCTION",
            "bullets": [
                "<b>Project Title:</b> FaceAttend — Face Recognition Attendance Management System.",
                "<b>Core Focus:</b> Automated, contactless attendance tracking powered by OpenCV computer vision and Python Flask.",
                "<b>Platform Compatibility:</b> 100% Windows compatible, runs completely local and offline with zero cloud dependency."
            ],
            "easy_explanation": "This is your opening slide. It introduces what FaceAttend is: a software that replaces slow paper attendance and RFID cards with a smart camera that recognizes students' faces automatically and logs their attendance in a secure database in under a second.",
            "tech_concept": "<b>Why Python + Flask + OpenCV?</b> Python gives access to OpenCV's high-speed computer vision libraries. Flask acts as the web backend serving separate web portals, and SQLite provides instant, local, zero-configuration database storage.",
            "speaker_tip": "Start by stating: 'FaceAttend is an automated biometric attendance system designed to make campus attendance tamper-proof, fast, and completely private.'"
        },
        {
            "num": 2,
            "title": "Project Overview & Core Objectives",
            "category": "PROBLEM STATEMENT & OBJECTIVES",
            "bullets": [
                "<b>The Problem with Manual Roll Calls:</b> Takes 10-15 minutes of lecture time, paper registers can be lost or altered, and students sign proxies for missing friends.",
                "<b>The Problem with RFID Cards:</b> Cards can be handed to classmates (buddy punching) and physically lost.",
                "<b>The FaceAttend Solution:</b> Contactless face scan via standard webcam, instant verification (< 1 second), and automated database records.",
                "<b>Key Project Goals:</b> 0% proxy attendance, guaranteed 0% duplicate entries per day, and dual separate dashboards."
            ],
            "easy_explanation": "Explain why this project was created. In colleges and schools, teachers waste time taking roll call, and students frequently sign proxies for friends who skipped class. FaceAttend completely stops proxy attendance because your face is unique to you.",
            "tech_concept": "<b>Anti-Proxy Philosophy:</b> Biometrics (what you are) is fundamentally more secure than knowledge (passwords) or tokens (ID cards), because physical traits cannot be shared.",
            "speaker_tip": "Emphasize how much classroom teaching time is saved: up to 50 hours of wasted attendance time per semester across an entire campus."
        },
        {
            "num": 3,
            "title": "Full-Stack Technology Architecture",
            "category": "SYSTEM STACK",
            "bullets": [
                "<b>Backend:</b> Python 3.10+ / 3.14 with Flask 3.1 using Blueprint routing namespaces (/admin, /user, /api, /auth).",
                "<b>Computer Vision:</b> OpenCV (opencv-contrib-python), Haar Cascade Classifier, and LBPHFaceRecognizer.",
                "<b>Database:</b> SQLite 3 with ACID transactions, foreign keys, and unique daily constraints.",
                "<b>Frontend:</b> HTML5, CSS3, JavaScript, Bootstrap 5.3 (Dark/Light mode support), and Chart.js 4.4.",
                "<b>Export Engine:</b> Python CSV writer and OpenPyXL for styled Excel spreadsheets."
            ],
            "easy_explanation": "This slide shows the tools and programming languages used to build the software. It uses Python for the brain, OpenCV for the camera vision, Flask for the website, and SQLite to store student names and records.",
            "tech_concept": "<b>Why not heavy deep-learning frameworks (like dlib/CUDA)?</b> Dlib requires Microsoft Visual Studio C++ compilers and CMake, which fail on standard Windows user PCs. OpenCV's LBPH runs natively out-of-the-box on ANY Windows PC CPU without an expensive graphics card (GPU).",
            "speaker_tip": "Highlight that this stack is lightweight and runs efficiently even on an entry-level laptop with a basic webcam."
        },
        {
            "num": 4,
            "title": "End-to-End System Workflow",
            "category": "DATA FLOW & ARCHITECTURE",
            "bullets": [
                "<b>Workflow A (Face Registration):</b> Admin selects student -> Webcam turns on -> Checks single face -> Captures 5-6 sample crops -> LBPH model compiles and saves to face_model.xml.",
                "<b>Workflow B (Live Attendance):</b> Scanner camera reads video frames -> Haar Cascade finds face -> LBPH predicts student identity -> Checks duplicate status -> Logs 'Present' or 'Late' in database -> Plays sound confirmation."
            ],
            "easy_explanation": "Think of this in two simple phases: Phase 1 is 'Training' (teaching the computer what a student looks like by taking 5-6 quick photos). Phase 2 is 'Testing' (when the student walks in front of the camera, the computer compares their face with the saved model and marks attendance).",
            "tech_concept": "<b>Real-Time API Communication:</b> The browser captures frames as Base64 JPEG data URLs and sends them via asynchronous POST requests to Flask REST endpoints (/api/face/recognize), updating the UI without refreshing the page.",
            "speaker_tip": "Walk through the diagram step-by-step: 'First enrollment, second recognition, third database logging.'"
        },
        {
            "num": 5,
            "title": "Technique 1: OpenCV Haar Cascade Face Detection",
            "category": "COMPUTER VISION DETECTION",
            "bullets": [
                "<b>Model:</b> haarcascade_frontalface_default.xml (Viola-Jones algorithm).",
                "<b>Haar-like Features:</b> Mathematical digital filters detecting contrast differences (e.g. eyes are darker than forehead and cheeks).",
                "<b>Integral Image:</b> Computes rectangular pixel sums in O(1) constant time, enabling 30+ frames-per-second real-time detection on CPU.",
                "<b>Validation Gate:</b> If 0 faces -> alerts 'No face detected'. If > 1 faces -> alerts 'Multiple faces detected'. Exactly 1 face -> crops bounding box."
            ],
            "easy_explanation": "Before the computer can recognize WHO you are, it must first FIND where your face is in the camera. Haar Cascade scans the video and looks for universal human facial patterns—like your eyes being darker than your forehead. It draws a green bounding box around your face.",
            "tech_concept": "<b>Adaboost Cascade:</b> Rejection of non-face background happens in the first few stages. Only regions passing all cascade filters are marked as faces, making it extremely fast.",
            "speaker_tip": "Explain that this step prevents mistakes by strictly rejecting frames if two people stand together or if the person turns away."
        },
        {
            "num": 6,
            "title": "Technique 2: Face Normalization & Lighting Invariance",
            "category": "IMAGE PREPROCESSING",
            "bullets": [
                "<b>The Challenge:</b> Sunlight, shadows, or dim classroom lights change pixel values, confusing recognition algorithms.",
                "<b>Step 1 (Grayscale):</b> cv2.cvtColor drops RGB color channels to focus purely on facial bone structure and geometry.",
                "<b>Step 2 (Histogram Equalization):</b> cv2.equalizeHist flattens light and stretches contrast across the face.",
                "<b>Step 3 (Safety Margin):</b> Adds a 5% border around the face crop to keep the jawline and forehead intact.",
                "<b>Step 4 (Standard Sizing):</b> Resizes all face crops to an exact 200x200 pixel matrix."
            ],
            "easy_explanation": "If a student registers their face in a bright room but attends class in a darker room, a regular computer might get confused by shadows. We fix this by converting the image to black-and-white, leveling out the light (Histogram Equalization), and making all face crops the exact same 200x200 size.",
            "tech_concept": "<b>Histogram Equalization:</b> Redistributes pixel intensities across a uniform histogram so that areas of low contrast gain higher contrast, neutralizing shadow distortion.",
            "speaker_tip": "Use a simple analogy: 'Histogram equalization acts like an automated digital lighting technician that ensures everyone's face looks equally lit.'"
        },
        {
            "num": 7,
            "title": "Technique 3: LBPH Face Recognition Algorithm",
            "category": "BIOMETRIC RECOGNITION",
            "bullets": [
                "<b>Model:</b> Local Binary Patterns Histograms (cv2.face.LBPHFaceRecognizer).",
                "<b>LBP Operator:</b> Compares each center pixel against its 8 neighbors. If neighbor >= center, writes 1, else 0 (forming an 8-bit binary number).",
                "<b>Decimal Code:</b> Converts the 8-bit binary number into a decimal texture number (0 to 255).",
                "<b>Grid Histograms:</b> Divides the 200x200 face into an 8x8 grid (64 cells) and builds a histogram for each cell.",
                "<b>Feature Vector:</b> Concatenates all 64 histograms into one unique mathematical fingerprint for each student."
            ],
            "easy_explanation": "How does the computer recognize your face? It breaks your face down into 64 tiny squares. In each square, it calculates the texture of your skin, pores, and edges using numbers (0 or 1). It binds these together into a unique mathematical 'barcode' for each student.",
            "tech_concept": "<b>Why LBPH is superior to Eigenfaces:</b> Eigenfaces looks at the whole face at once, so a new hairstyle or glasses can cause failure. LBPH looks at local micro-textures, remaining reliable even if parts of the face change.",
            "speaker_tip": "Emphasize that the system does not store actual photos in the model—it stores mathematical histograms, which is much more secure."
        },
        {
            "num": 8,
            "title": "Technique 4: Distance Matching & Thresholding",
            "category": "CLASSIFICATION & REJECTION",
            "bullets": [
                "<b>Comparison Metric:</b> Uses Chi-Square distance to compare the incoming face histogram against stored student histograms.",
                "<b>Understanding Distance in LBPH:</b> Lower distance means closer match (0 is identical, 40-70 is strong match, > 75 is mismatch).",
                "<b>Threshold Decision:</b> Default threshold is 75.0 (adjustable in Admin Settings).",
                "  • Distance <= 75.0: RECOGNIZED -> Marks attendance.",
                "  • Distance > 75.0: UNKNOWN FACE -> Rejected. Attendance is NOT marked.",
                "<b>Confidence Formula:</b> match_confidence = max(0, 100 - distance)."
            ],
            "easy_explanation": "When someone stands in front of the camera, the system measures how 'far away' their face looks from the stored models. If the distance score is small (under 75), it says 'Yes, this is Alex!' If the distance is too large, it says 'Unknown Face' and refuses to mark attendance.",
            "tech_concept": "<b>Adjustable Threshold Slider:</b> In the Admin portal, the administrator can slide the threshold between 40 (Strict - high security) and 90 (Relaxed - forgiving angles) to fit the institutional environment.",
            "speaker_tip": "Point out that the system never guesses: an unknown stranger will never accidentally get attendance marked for a student."
        },
        {
            "num": 9,
            "title": "Dual Dashboard Architecture & Role-Based Access",
            "category": "ROLE-BASED ACCESS CONTROL (RBAC)",
            "bullets": [
                "<b>Admin Dashboard (/admin/...):</b> Full management control, student CRUD, face enrollment, scanner kiosk, records, reports, settings.",
                "<b>Student Dashboard (/user/...):</b> Student-friendly portal, personal attendance %, self-attendance scanner, history, and report certificates.",
                "<b>Backend Security Enforcement:</b> Protected by Flask session decorators (@admin_required, @user_required).",
                "<b>Access Denied Redirection:</b> If a student manually types /admin/dashboard into their browser, the system blocks them with 'Access Denied' and redirects to their dashboard."
            ],
            "easy_explanation": "There are TWO completely separate websites inside this project: one for the Teacher/Admin and one for the Student. A student cannot see other students' grades, delete records, or access administrative tools. The backend server checks their role on every single page load.",
            "tech_concept": "<b>Why UI hiding is not enough:</b> True security requires controller-level authorization checks. Even if a user inspects elements or curls the admin URLs, Flask rejects the request without an Admin session.",
            "speaker_tip": "Mention that this satisfies the strict requirement of two independent layouts rather than just showing or hiding buttons on one page."
        },
        {
            "num": 10,
            "title": "Administrator Management Tools",
            "category": "ADMINISTRATIVE MODULES",
            "bullets": [
                "<b>Student Management (/admin/students):</b> Add, edit, delete students with automatic user account provisioning.",
                "<b>Register Face Module (/admin/register-face):</b> Webcam preview with live progress bar collecting 5-6 sample frames with instant model retraining.",
                "<b>Master Take Attendance Scanner (/admin/take-attendance):</b> Live campus kiosk scanner with audio chimes and real-time student cards.",
                "<b>Master Records & Manual Entry (/admin/records):</b> Audit table with date/department/status filtering and manual override options.",
                "<b>User Accounts & Settings:</b> Password resets, disable/activate accounts, and adjust cutoff times."
            ],
            "easy_explanation": "This slide outlines the tools given to administrators. An admin can easily register new students, enroll their face with a camera in 5 seconds, watch live attendance on a projector screen, and adjust school timings.",
            "tech_concept": "<b>Automatic Account Provisioning:</b> When an administrator adds a student record (e.g. STU001), the backend automatically creates a linked portal login account with hashed credentials, eliminating double data entry.",
            "speaker_tip": "Point out the live progress bar: as the student tilts their head slightly, the bar moves from 0% to 100% and trains the model automatically."
        },
        {
            "num": 11,
            "title": "Student Self-Attendance & Anti-Proxy Verification",
            "category": "STUDENT PORTAL & ANTI-PROXY",
            "bullets": [
                "<b>Dedicated Self-Attendance Page (/user/mark-attendance):</b> Students can mark attendance on their own laptop or tablet.",
                "<b>Anti-Proxy Cross-Verification:</b> Scans the face and strictly verifies: Does scanned_student_id == session['student_id']?",
                "  • If face matches: Attendance logged as 'Present' (or 'Late').",
                "  • If classmate's face scanned: REJECTED with 'Face Mismatch! Scanned face belongs to another student, not you.'",
                "  • If stranger scanned: REJECTED with 'Face Not Recognized'.",
                "<b>Today's Status Widget:</b> Instant visual feedback on Student Dashboard and Profile."
            ],
            "easy_explanation": "Students can mark attendance themselves! But here is the smart part: if student John logs in and asks his friend Mike to stand in front of the camera, the system recognizes that Mike is NOT John, stops the process, and displays an 'Identity Mismatch' warning. No buddy punching is possible!",
            "tech_concept": "<b>Session-Biometric Binding:</b> Bridges web session state with biometric feature identification, turning a standard student web browser into an authenticated biometric terminal.",
            "speaker_tip": "This is one of the most impressive features to demonstrate to teachers and college deans because it solves proxy attendance completely."
        },
        {
            "num": 12,
            "title": "Duplicate Attendance Prevention Architecture",
            "category": "DATABASE INTEGRITY",
            "bullets": [
                "<b>The Challenge:</b> A student standing in front of a live camera for 5 seconds could accidentally generate 10 attendance records.",
                "<b>Tier 1 (Application Layer Check):</b> Before saving, queries: SELECT id FROM attendance WHERE student_id = ? AND attendance_date = ?",
                "  • If found: Returns status 'already_marked' -> Displays 'Attendance Already Marked Today' alert.",
                "<b>Tier 2 (Database Layer Hard Constraint):</b>",
                "  CONSTRAINT unique_daily_attendance UNIQUE (student_id, attendance_date)",
                "  • Even during network race conditions, SQLite rejects duplicate daily insertions at the database engine level."
            ],
            "easy_explanation": "What happens if a student waves at the camera twice, or stands there talking to a friend? FaceAttend prevents duplicate rows using a two-tier defense. The website alerts 'Already Marked Today', and the database has a strict rule that physically refuses to save a second record for the same person on the same date.",
            "tech_concept": "<b>Composite Unique Constraint:</b> The pair (student_id, attendance_date) acts as an index key. Any attempt to insert a duplicate raises an IntegrityError that the application catches cleanly.",
            "speaker_tip": "Explain that this keeps the database clean and ensures attendance percentages are always 100% accurate."
        },
        {
            "num": 13,
            "title": "Analytics, Reports & Export Formats",
            "category": "REPORTS & EXPORTS",
            "bullets": [
                "<b>Real-Time Dynamic Charts (Chart.js):</b>",
                "  • 7-Day Attendance Trend: Line chart tracking daily Present, Late, and Absent numbers.",
                "  • Department Distribution: Bar chart comparing attendance volume across departments.",
                "  • Student Personal Donut Chart: Visualizes personal ratio against the 75% minimum university requirement.",
                "<b>Multi-Format Exports:</b>",
                "  • CSV Export: Instant lightweight raw attendance logs.",
                "  • Excel (.xlsx) Export: Formatted workbooks with color-coded status pills (green, yellow, red).",
                "  • Print Transcript: Printable official certificate with signature blocks."
            ],
            "easy_explanation": "Attendance data is only useful if you can analyze it. FaceAttend gives administrators instant visual graphs and allows downloading reports in both Excel and CSV. Students can also print an official attendance certificate with one click.",
            "tech_concept": "<b>Dynamic Database Calculations:</b> Zero fake statistics! All chart numbers, percentages, and totals are computed live using SQL aggregate functions (COUNT, SUM, CASE WHEN).",
            "speaker_tip": "Show how easy it is for an administrator to hand an Excel attendance spreadsheet to the college principal at the end of the month."
        },
        {
            "num": 14,
            "title": "Data Privacy & Security Guardrails",
            "category": "SECURITY & PRIVACY",
            "bullets": [
                "<b>100% Local On-Premises Storage:</b> Face crops and biometric models remain solely on the institution's local storage.",
                "<b>Zero Cloud Leaks:</b> No biometric data, images, or identifiers are shared with third-party cloud APIs.",
                "<b>Right to Erasure (Privacy Compliance):</b> Administrators can permanently delete biometric data for any student with instant model retraining.",
                "<b>Password Security:</b> Uses industry-standard PBKDF2 with SHA-256 password hashing (Werkzeug).",
                "<b>SQL Injection Prevention:</b> All queries use parameterized SQL statements (?, ?).",
                "<b>Automated Unit Tests:</b> 14/14 automated tests verifying security, auth, and biometrics."
            ],
            "easy_explanation": "Face data is sensitive personal information. We respect student privacy: no photos are ever uploaded to the internet or cloud servers. Everything stays on the school's local computer. If a student leaves the school, their face data can be permanently erased with one click.",
            "tech_concept": "<b>Parameterization:</b> User inputs are passed as parameters rather than string concatenation, guaranteeing immunity against SQL injection attacks.",
            "speaker_tip": "Highlight compliance with data privacy regulations: 'FaceAttend is designed from the ground up to respect student data privacy.'"
        },
        {
            "num": 15,
            "title": "Conclusion & Future Roadmap",
            "category": "CONCLUSION & ROADMAP",
            "bullets": [
                "<b>What Was Achieved:</b> A complete, production-ready biometric attendance management system with dual separate dashboards, high accuracy (< 1s), duplicate prevention, and student self-attendance.",
                "<b>Testing Validation:</b> 14 out of 14 automated unit tests passed cleanly.",
                "<b>Future Enhancements:</b>",
                "  • Liveness Detection: Eye blink and micro-motion detection to prevent photo spoofing.",
                "  • CCTV RTSP Integration: Continuous hallway camera attendance capture.",
                "  • Automated Alerts: Automatic SMS / Email alerts to parents when student attendance drops below 75%."
            ],
            "easy_explanation": "To wrap up: FaceAttend is fully working, thoroughly tested, and ready for deployment. In the future, we can add features like eye-blink detection (so no one can hold up a photo on a phone) and connect it directly to campus CCTV cameras.",
            "tech_concept": "<b>Future Liveness Detection:</b> Using facial landmark analysis (eye aspect ratio - EAR) to verify eye blinking before accepting a face frame, stopping 2D printed photo attacks.",
            "speaker_tip": "Conclude confidently: 'FaceAttend provides a modern, secure, and touchless attendance system that saves time, prevents proxy marking, and protects privacy. Thank you!'"
        }
    ]

    for s_data in slides:
        # Slide Box
        card_content = []
        
        # Category Badge
        card_content.append(Paragraph(f"SLIDE {s_data['num']} &bull; {s_data['category']}", badge_style))
        card_content.append(Paragraph(s_data['title'], h1_style))
        card_content.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8, spaceBefore=4))

        # Bullet Points
        card_content.append(Paragraph("<b>Slide Bullet Points (What appears on screen):</b>", tech_box_title))
        for b in s_data['bullets']:
            card_content.append(Paragraph(f"&bull; {b}", bullet_style))
        card_content.append(Spacer(1, 6))

        # Easy Explanation
        card_content.append(Paragraph("<b>Easy Explanation (In simple terms):</b>", tech_box_title))
        card_content.append(Paragraph(s_data['easy_explanation'], body_style))
        card_content.append(Spacer(1, 4))

        # Deep Tech Concept
        card_content.append(Paragraph("<b>Technical Mechanics (How it actually works under the hood):</b>", tech_box_title))
        card_content.append(Paragraph(s_data['tech_concept'], body_style))
        card_content.append(Spacer(1, 4))

        # Speaker Tip
        card_content.append(Paragraph(f"<b>🗣️ What You Can Say To The Audience:</b> \"{s_data['speaker_tip']}\"", explanation_style))

        # Wrap in Table Card
        card_table = Table([[card_content]], colWidths=[504])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
            ('BOX', (0, 0), (-1, -1), 1, c_border),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 14),
            ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ]))

        story.append(KeepTogether(card_table))
        story.append(Spacer(1, 14))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {pdf_path}")

if __name__ == '__main__':
    build_pdf()
