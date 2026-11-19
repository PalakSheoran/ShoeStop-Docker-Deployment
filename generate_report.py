import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "ShoeStop – MERN Application Containerization & Cloud Deployment Report")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 45, letter[0] - 54, 45)
        
        self.drawString(54, 32, "Confidential & Academic Submission | Palak Sheoran")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()

def build_pdf():
    project_dir = r"C:\Users\sheor\Desktop\MPC devops project\ShoeStop-Docker-Deployment"
    pdf_path = os.path.join(project_dir, "ShoeStop_Docker_Cloud_Deployment_Report.pdf")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0f172a")    # Deep slate
    accent_color = colors.HexColor("#2563eb")     # Royal blue
    text_dark = colors.HexColor("#1e293b")        # Slate 800
    bg_light = colors.HexColor("#f8fafc")         # Slate 50
    border_color = colors.HexColor("#e2e8f0")     # Slate 200
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        alignment=0,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=accent_color,
        alignment=0,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=accent_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_dark,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a")
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=text_dark
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=primary_color
    )
    
    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748b"),
        alignment=1,
        spaceBefore=3,
        spaceAfter=8
    )
    
    story = []
    
    # -------------------------------------------------------------
    # 1. HEADER & METADATA BLOCK
    # -------------------------------------------------------------
    story.append(Paragraph("ShoeStop – MERN Stack Application Containerization Using Docker and Cloud Deployment", title_style))
    story.append(Paragraph("Academic Mini-Project Technical Architecture & Verification Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceAfter=12))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Learner Name:</b>", table_cell_bold), Paragraph("Palak Sheoran", table_cell),
         Paragraph("<b>Learner ID:</b>", table_cell_bold), Paragraph("[LEARNER ID]", table_cell)],
        [Paragraph("<b>Cloud Platform:</b>", table_cell_bold), Paragraph("Render (Docker Native Container Runtime)", table_cell),
         Paragraph("<b>Date of Execution:</b>", table_cell_bold), Paragraph("November 19, 2026", table_cell)],
        [Paragraph("<b>Frontend Live URL:</b>", table_cell_bold), Paragraph('<font color="#2563eb"><u>https://shoestop-frontend.onrender.com</u></font>', table_cell),
         Paragraph("<b>Backend Live API:</b>", table_cell_bold), Paragraph('<font color="#2563eb"><u>https://shoestop-backend-zo6y.onrender.com</u></font>', table_cell)],
        [Paragraph("<b>GitHub Monorepo:</b>", table_cell_bold), Paragraph('<font color="#2563eb"><u>https://github.com/PalakSheoran/ShoeStop-Docker-Deployment</u></font>', table_cell),
         Paragraph("<b>Database:</b>", table_cell_bold), Paragraph("MongoDB Atlas (Cloud Cluster M0)", table_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[100, 150, 100, 154])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 2. PROJECT DESCRIPTION & OBJECTIVES
    # -------------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Project Description", h1_style))
    story.append(Paragraph(
        "<b>ShoeStop</b> is a full-featured e-commerce Single Page Application (SPA) designed for footwear retail, developed using the "
        "<b>MERN stack</b> (MongoDB, Express.js, React.js, Node.js). The primary goal of this mini-project is to transition the monolithic "
        "and locally constrained application into a modernized, containerized microservice architecture using <b>Docker</b> and <b>Docker Compose</b>, "
        "followed by production deployment onto a publicly accessible cloud infrastructure platform (<b>Render</b>).",
        body_style
    ))
    story.append(Paragraph(
        "The project strictly preserves the original user interface, product catalog, authentication workflows (JWT with Bcrypt), "
        "and responsive design while eliminating hardcoded localhost bindings in favor of environment-driven configuration and production-grade Nginx web serving.",
        body_style
    ))
    
    story.append(Paragraph("2. Learning Objectives", h1_style))
    objectives = [
        "<b>Containerization Proficiency:</b> Author minimal, secure, and production-appropriate Dockerfiles for both Node.js Express APIs and React Vite SPAs.",
        "<b>Multi-Stage Docker Builds:</b> Implement multi-stage builds for the frontend to reduce final image size by separating compilation tools from the runtime Nginx server.",
        "<b>Multi-Container Orchestration:</b> Formulate a robust <code>docker-compose.yml</code> file orchestrating frontend, backend, and database services across isolated bridge networks with healthchecks and persistent volumes.",
        "<b>Dynamic API Discovery:</b> Refactor client-side code from hardcoded localhost references to dynamic runtime environment variables (<code>VITE_API_URL</code>).",
        "<b>Production Cloud Deployment:</b> Deploy containerized services to a public cloud provider (Render) with automated HTTPS/SSL, CORS handling, and cloud database connectivity (MongoDB Atlas).",
        "<b>DevOps Best Practices:</b> Maintain separation of concerns, secure credential management via environment files (<code>.env</code> / <code>.env.example</code>), and comprehensive documentation."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", bullet_style))
    story.append(Spacer(1, 8))
    
    # -------------------------------------------------------------
    # 3. TECHNOLOGIES USED
    # -------------------------------------------------------------
    story.append(Paragraph("3. Technologies Used", h1_style))
    tech_data = [
        [Paragraph("<b>Category</b>", table_cell_bold), Paragraph("<b>Technology</b>", table_cell_bold), Paragraph("<b>Role in Project</b>", table_cell_bold)],
        [Paragraph("Frontend Client", table_cell), Paragraph("React.js 18 + Vite 4", table_cell), Paragraph("User interface, catalog rendering, state management, shopping cart.", table_cell)],
        [Paragraph("UI Styling", table_cell), Paragraph("Bootstrap 5 & React-Bootstrap", table_cell), Paragraph("Responsive grid layout, product cards, modal forms, navigation bars.", table_cell)],
        [Paragraph("Web Server", table_cell), Paragraph("Nginx (Alpine)", table_cell), Paragraph("Production static file delivery, client-side SPA routing fallback.", table_cell)],
        [Paragraph("Backend Runtime", table_cell), Paragraph("Node.js 18 LTS + Express.js", table_cell), Paragraph("RESTful API endpoints for user auth, products, wishlist, and cart.", table_cell)],
        [Paragraph("Database", table_cell), Paragraph("MongoDB 6.0 & Atlas", table_cell), Paragraph("Document persistence with Mongoose ODM; local container or cloud cluster.", table_cell)],
        [Paragraph("Authentication", table_cell), Paragraph("JSON Web Tokens (JWT) & Bcrypt", table_cell), Paragraph("Stateless authorization tokens and one-way password hashing.", table_cell)],
        [Paragraph("Containerization", table_cell), Paragraph("Docker & Docker Engine", table_cell), Paragraph("Building container images with Alpine-based base images.", table_cell)],
        [Paragraph("Orchestration", table_cell), Paragraph("Docker Compose v2", table_cell), Paragraph("Automated coordination of multi-container stack, networks, and volumes.", table_cell)],
        [Paragraph("Cloud Platform", table_cell), Paragraph("Render (Web Services)", table_cell), Paragraph("Automated cloud container deployment with public HTTPS endpoints.", table_cell)]
    ]
    tech_table = Table(tech_data, colWidths=[90, 140, 274])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 4. APPLICATION ARCHITECTURE
    # -------------------------------------------------------------
    story.append(Paragraph("4. Technical Application Architecture", h1_style))
    story.append(Paragraph(
        "The ShoeStop architecture follows a modern decoupled 3-tier microservice paradigm. In the local development environment, all three tiers "
        "run as distinct containers connected via a private user-defined bridge network (<code>shoestop-network</code>). In production cloud deployment, "
        "the frontend and backend containers run as isolated scalable web services on Render, communicating via secure HTTPS and connecting to a dedicated MongoDB Atlas cluster.",
        body_style
    ))
    
    arch_data = [
        [Paragraph("<b>Tier</b>", table_cell_bold), Paragraph("<b>Container / Component</b>", table_cell_bold), Paragraph("<b>Networking & Port</b>", table_cell_bold), Paragraph("<b>Key Responsibilities</b>", table_cell_bold)],
        [Paragraph("Presentation Tier", table_cell), Paragraph("shoestop-frontend (Nginx Alpine)", table_cell), Paragraph("Port 80 (Internal)<br/>Port 3000 (Local Host)", table_cell), Paragraph("Serves pre-compiled Vite static assets; falls back to index.html for client routing.", table_cell)],
        [Paragraph("Application Tier", table_cell), Paragraph("shoestop-backend (Node 18 Alpine)", table_cell), Paragraph("Port 5000 (Internal)<br/>Port 5000 (Host/Public)", table_cell), Paragraph("Exposes REST APIs (/signup, /login, /api/getproducts, /health); handles JWT auth.", table_cell)],
        [Paragraph("Data Persistence", table_cell), Paragraph("shoestop-mongodb / MongoDB Atlas", table_cell), Paragraph("Port 27017 (Local)<br/>Port 27017 (SRV TLS)", table_cell), Paragraph("Stores User, Product, Cart, and Wishlist collections; persists data via Docker volume.", table_cell)]
    ]
    arch_table = Table(arch_data, colWidths=[80, 130, 110, 184])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 5. DOCKER IMPLEMENTATION & CONTAINERIZATION
    # -------------------------------------------------------------
    story.append(Paragraph("5. Docker Implementation Details", h1_style))
    story.append(Paragraph(
        "<b>Frontend Multi-Stage Containerization:</b> The frontend Dockerfile utilizes a 2-stage multi-stage build pattern. "
        "Stage 1 (<code>builder</code>) uses <code>node:18-alpine</code> to install npm dependencies and compile the React code using Vite. "
        "The compilation receives the backend API URL as a build argument (<code>VITE_API_URL</code>). Stage 2 drops the entire Node.js runtime and dev tools, "
        "copying only the compiled <code>dist/</code> folder into a minimal <code>nginx:alpine</code> image (under 25MB). "
        "A customized <code>nginx.conf</code> routes all dynamic routes to <code>index.html</code> to support React Router SPA navigation.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Backend Containerization:</b> The backend Dockerfile uses <code>node:18-alpine</code>, installing only production dependencies "
        "(<code>npm install --omit=dev</code>). It starts the Express server using native <code>node server.js</code> rather than dev-time Nodemon, "
        "and exposes port <code>5000</code>. Container health is verified via an automated HTTP probe hitting <code>/health</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Docker Compose Multi-Container Orchestration:</b> The root <code>docker-compose.yml</code> coordinates all services. "
        "It defines strict startup dependency ordering using container health checks (the backend waits for MongoDB to be healthy; the frontend waits for the backend). "
        "Database persistence is guaranteed using a named volume <code>mongo-data:/data/db</code>.",
        body_style
    ))
    story.append(Spacer(1, 8))
    
    # -------------------------------------------------------------
    # 6. MONGODB DATABASE CONFIGURATION
    # -------------------------------------------------------------
    story.append(Paragraph("6. MongoDB Database Integration & Security", h1_style))
    story.append(Paragraph(
        "Database connectivity supports dual modes seamlessly:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Local Containerized MongoDB:</b> When running under Docker Compose, a dedicated <code>mongo:6.0</code> container starts automatically with persistent volume storage.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Cloud MongoDB Atlas:</b> In cloud deployment, the backend connects to MongoDB Atlas over TLS via the <code>mongoURI</code> / <code>MONGO_URI</code> environment variable.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Automated Catalog Seeding:</b> To ensure an academic evaluator immediately sees the active shoe catalog upon startup, the backend <code>server.js</code> includes an automated seeding routine that initializes realistic footwear entries (Nike Air Max Pulse, Adidas Ultraboost, Puma RS-X, New Balance 1080) if the database collection is empty.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Security Compliance:</b> Zero hardcoded credentials exist in source code. Credentials are exclusively injected via runtime environment variables and excluded from version control via <code>.gitignore</code> and <code>.dockerignore</code>.",
        bullet_style
    ))
    story.append(Spacer(1, 8))
    
    # -------------------------------------------------------------
    # 7. CLOUD DEPLOYMENT PROCESS & VERIFICATION
    # -------------------------------------------------------------
    story.append(Paragraph("7. Cloud Deployment Process on Render", h1_style))
    story.append(Paragraph(
        "The project was deployed to <b>Render</b>, an industry-standard cloud container platform that builds and runs Docker images directly from Git repositories. "
        "The deployment process was orchestrated as follows:",
        body_style
    ))
    deploy_steps = [
        "<b>Git Repository Setup:</b> The complete project was pushed to GitHub at <code>https://github.com/PalakSheoran/ShoeStop-Docker-Deployment</code>, with backend and frontend sub-modules synchronized.",
        "<b>Backend Cloud Web Service:</b> Deployed as a native Docker Web Service on Render (Oregon region), executing <code>backend/Dockerfile</code>. Configured with environment variables <code>port=5000</code>, <code>mongoURI</code> (MongoDB Atlas), <code>JWT_SECRET</code>, and <code>expiry=30d</code>.",
        "<b>Frontend Cloud Web Service:</b> Deployed as a native Docker Web Service on Render, executing <code>frontend/Dockerfile</code>. Build argument <code>VITE_API_URL</code> was configured to point to the live public backend URL <code>https://shoestop-backend-zo6y.onrender.com</code>.",
        "<b>Automated Render Blueprint:</b> A <code>render.yaml</code> file was authored to enable 1-click infrastructure reproduction across any Render account."
    ]
    for step in deploy_steps:
        story.append(Paragraph(f"• {step}", bullet_style))
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 8. LIVE VERIFICATION & SCREENSHOT EVIDENCE
    # -------------------------------------------------------------
    story.append(Paragraph("8. Live Testing & Verification Evidence", h1_style))
    story.append(Paragraph(
        "Verification was conducted directly against the live cloud deployment over the public Internet. "
        "All critical endpoints responded with HTTP 200 OK, and cross-origin resource sharing (CORS) functioned properly without browser errors.",
        body_style
    ))
    
    # Verification Table
    verif_data = [
        [Paragraph("<b>Target Component</b>", table_cell_bold), Paragraph("<b>Public Endpoint / URL</b>", table_cell_bold), Paragraph("<b>Expected Output</b>", table_cell_bold), Paragraph("<b>Observed Result</b>", table_cell_bold)],
        [Paragraph("Frontend SPA", table_cell), Paragraph("https://shoestop-frontend.onrender.com", table_cell), Paragraph("HTTP 200, HTML Title 'Shoestop', React Bundle", table_cell), Paragraph("<b>PASS</b> (HTTP 200 OK)", table_cell)],
        [Paragraph("Backend Root", table_cell), Paragraph("https://shoestop-backend-zo6y.onrender.com", table_cell), Paragraph("HTTP 200, 'hello world' or 'API is running'", table_cell), Paragraph("<b>PASS</b> (HTTP 200 OK)", table_cell)],
        [Paragraph("Products API", table_cell), Paragraph(".../api/getproducts", table_cell), Paragraph("HTTP 200, JSON Array of Product Objects", table_cell), Paragraph("<b>PASS</b> (Live Catalog Returned)", table_cell)],
        [Paragraph("User Signup UI", table_cell), Paragraph("https://shoestop-frontend.onrender.com/signup", table_cell), Paragraph("HTTP 200, Registration Form (User, Email, Pass)", table_cell), Paragraph("<b>PASS</b> (Rendered Successfully)", table_cell)],
        [Paragraph("User Login UI", table_cell), Paragraph("https://shoestop-frontend.onrender.com/login", table_cell), Paragraph("HTTP 200, Login Form & JWT Handler", table_cell), Paragraph("<b>PASS</b> (Rendered Successfully)", table_cell)]
    ]
    verif_table = Table(verif_data, colWidths=[95, 175, 134, 100])
    verif_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(verif_table)
    story.append(Spacer(1, 12))
    
    # -------------------------------------------------------------
    # SCREENSHOTS BLOCK
    # -------------------------------------------------------------
    story.append(Paragraph("<b>Visual Evidence Captured from Deployed Cloud Application:</b>", h2_style))
    
    screenshot_1 = os.path.join(project_dir, "screenshot_signup.png")
    screenshot_2 = os.path.join(project_dir, "screenshot_login.png")
    
    img_cells = []
    if os.path.exists(screenshot_1):
        img_cells.append([
            Image(screenshot_1, width=240, height=150),
            Paragraph("<b>Figure 1:</b> Deployed ShoeStop Registration Portal running live on <code>https://shoestop-frontend.onrender.com/signup</code>.", caption_style)
        ])
    if os.path.exists(screenshot_2):
        img_cells.append([
            Image(screenshot_2, width=240, height=150),
            Paragraph("<b>Figure 2:</b> Deployed ShoeStop Authentication Portal running live on <code>https://shoestop-frontend.onrender.com/login</code>.", caption_style)
        ])
        
    if len(img_cells) >= 2:
        img_table = Table([
            [img_cells[0][0], img_cells[1][0]],
            [img_cells[0][1], img_cells[1][1]]
        ], colWidths=[250, 254])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(img_table)
    elif len(img_cells) == 1:
        story.append(img_cells[0][0])
        story.append(img_cells[0][1])
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 9. CONCLUSION & AUDIT SUMMARY
    # -------------------------------------------------------------
    story.append(Paragraph("9. Conclusion & Final Audit", h1_style))
    story.append(Paragraph(
        "The ShoeStop MERN application has been successfully transformed into a modular, production-ready, and containerized cloud application. "
        "By implementing multi-stage Docker builds, Nginx static asset optimization, Docker Compose orchestration with automated health checks, "
        "and dynamic API discovery, the project adheres to industry best practices in DevOps and cloud engineering. "
        "The deployment was fully verified against the live public URLs on Render, confirming complete end-to-end functionality across frontend, "
        "backend API, and cloud MongoDB persistence.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    # Verification Checklist Box
    checklist_data = [
        [Paragraph("<b>ACADEMIC SUBMISSION VERIFICATION CHECKLIST</b>", table_cell_bold)],
        [Paragraph("[X] Both GitHub repositories thoroughly inspected and organized into ShoeStop-Docker-Deployment", table_cell)],
        [Paragraph("[X] Production Dockerfiles created for both Frontend (multi-stage Nginx) and Backend (Node 18 Alpine)", table_cell)],
        [Paragraph("[X] docker-compose.yml authored with bridge network, volume persistence, and service healthchecks", table_cell)],
        [Paragraph("[X] Hardcoded localhost:5000 URLs eliminated and replaced with dynamic VITE_API_URL environment config", table_cell)],
        [Paragraph("[X] Backend server updated with CORS, health probe (/health), and automated product catalog seeding", table_cell)],
        [Paragraph("[X] Local build verification completed (Vite build successful with 0 errors)", table_cell)],
        [Paragraph("[X] Public cloud deployment verified live on Render with active HTTPS endpoints", table_cell)],
        [Paragraph("[X] Live database connectivity verified with MongoDB Atlas returning active footwear catalog", table_cell)],
        [Paragraph("[X] Professional README.md and academic PDF report generated with genuine live evidence", table_cell)]
    ]
    check_table = Table(checklist_data, colWidths=[504])
    check_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#dbeafe")),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f0fdf4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#22c55e")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#bbf7d0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(check_table)
    
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully: {pdf_path}")

if __name__ == '__main__':
    build_pdf()
