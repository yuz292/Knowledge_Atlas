#!/usr/bin/env python3
"""
Knowledge Atlas Lightweight Auth Server
========================================
FastAPI + SQLite backend providing real JWT authentication for ATLAS.

Endpoints
---------
POST /auth/register          – create account (status=pending; instructor approves)
POST /auth/login             – returns access + refresh JWT
POST /auth/forgot-password   – generates reset token (printed to console / stored in DB)
POST /auth/reset-password    – validates token, sets new password
GET  /auth/me                – returns current user info (requires Bearer token)
GET  /api/assignments        – returns student's assigned questions (requires Bearer token)
GET  /api/questions          – list all available research questions
GET  /api/registrations      – instructor-only: pending registrations
POST /api/registrations/{id}/approve   – instructor-only
POST /api/registrations/{id}/reject    – instructor-only

Running
-------
    python3 ka_auth_server.py
    # Server starts on http://localhost:8765
    # CORS allows http://localhost and file:// origins (for local dev)

Notes
-----
- SQLite DB: ka_auth.db (created automatically in same directory as this file)
- JWT secret: auto-generated on first run, stored in ka_auth_secret.txt
- Password reset "email": reset link is printed to console (no SMTP needed for local dev)
- HTTPS: not used in local dev; do not deploy this as-is to a public server
"""

import os, sys, sqlite3, secrets, hashlib, time, json, re
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Third-party (install: pip3 install fastapi uvicorn python-jose[cryptography] passlib[bcrypt])
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt, JWTError

# ════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════
BASE_DIR   = Path(__file__).parent
DB_PATH    = BASE_DIR / "data" / "ka_auth.db"
SECRET_FILE = BASE_DIR / "data" / "ka_auth_secret.txt"
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES  = 60
REFRESH_TOKEN_EXPIRE_DAYS    = 30
RESET_TOKEN_EXPIRE_MINUTES   = 60

# Load or generate JWT secret
def _get_secret() -> str:
    if SECRET_FILE.exists():
        return SECRET_FILE.read_text().strip()
    s = secrets.token_hex(48)
    SECRET_FILE.parent.mkdir(parents=True, exist_ok=True)
    SECRET_FILE.write_text(s)
    print(f"[KA-AUTH] Generated new JWT secret → {SECRET_FILE}")
    return s

SECRET_KEY = _get_secret()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)

# ════════════════════════════════════════════════
# DATABASE
# ════════════════════════════════════════════════
def get_db() -> sqlite3.Connection:
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    return db

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id     TEXT PRIMARY KEY,
        email       TEXT UNIQUE NOT NULL,
        first_name  TEXT NOT NULL,
        last_name   TEXT NOT NULL,
        role        TEXT NOT NULL DEFAULT 'student',
        password_hash TEXT NOT NULL,
        status      TEXT NOT NULL DEFAULT 'pending',
        track       TEXT,
        question_id TEXT,
        institution TEXT DEFAULT 'UC San Diego',
        department  TEXT,
        created_at  TEXT NOT NULL,
        approved_at TEXT,
        last_login  TEXT
    );
    CREATE TABLE IF NOT EXISTS reset_tokens (
        token       TEXT PRIMARY KEY,
        user_id     TEXT NOT NULL,
        expires_at  TEXT NOT NULL,
        used        INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS refresh_tokens (
        token       TEXT PRIMARY KEY,
        user_id     TEXT NOT NULL,
        expires_at  TEXT NOT NULL,
        revoked     INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS research_questions (
        question_id TEXT PRIMARY KEY,
        label       TEXT NOT NULL,
        domain      TEXT NOT NULL,
        text        TEXT NOT NULL,
        atlas_topic TEXT,
        notes       TEXT
    );
    """)
    # Seed research questions if table is empty
    count = db.execute("SELECT COUNT(*) FROM research_questions").fetchone()[0]
    if count == 0:
        questions = [
            # ── Lighting / Luminous Environment (4 questions) ──
            ("Q01", "Daylighting & Cognition",     "Luminous Environment",
             "Does access to natural daylight during working hours improve sustained attention? How large is the effect compared to equivalent artificial lighting, and does it depend on circadian timing?",
             "luminous__cog_attention", "High-VOI gap; Boubekri et al. 2014 gives one anchor."),
            ("Q08", "Colour Temperature & Alertness", "Luminous Environment",
             "Does correlated colour temperature of artificial lighting affect alertness independently of illuminance level? Is the effect robust across different tasks and times of day?",
             "luminous__cog_performance", "Direction unclear in older studies; recent LED research needed."),
            ("Q09", "Circadian Lighting & Sleep Quality", "Luminous Environment",
             "How does daytime exposure to circadian-effective light (melanopic EDI > 250 lux) in offices and classrooms affect nighttime sleep quality, and what minimum daily dose is required?",
             "luminous__health", "Boundary gap; dose-response poorly characterized outside clinical settings."),
            ("Q10", "Lighting & Spatial Navigation", "Luminous Environment",
             "Does ambient lighting distribution (uniform vs. non-uniform) affect wayfinding speed and route choice in complex indoor environments, independent of overall illuminance level?",
             "luminous__behav_navigation", "Mechanism gap; lighting typically treated as confound in wayfinding studies."),

            # ── Nature & Biophilia (4 questions) ──
            ("Q02", "Fractal Dimension & Stress",  "Nature & Biophilia",
             "Is fractal dimension of a visual scene causally related to psychophysiological stress recovery, or is the correlation mediated by familiarity with natural environments?",
             "natural__affect_negative_stress", "Mechanism gap; Taylor fractal work is correlational only."),
            ("Q06", "Window Views & Stress Recovery", "Nature & Biophilia",
             "What is the minimum exposure duration to a window view of nature sufficient to produce measurable cortisol reduction? Does view content matter independently of view presence?",
             "natural__affect_restoration", "Boundary gap; Ulrich 1984 seminal but not replicated with modern measures."),
            ("Q11", "Indoor Plants & Cognitive Restoration", "Nature & Biophilia",
             "Do indoor plants in a workspace improve attentional restoration beyond visual preference, and does the effect depend on plant density, species, or visibility from the workstation?",
             "natural__cog_attention", "Direction gap; Lohr et al. 1996 is widely cited but effect sizes unreplicated."),
            ("Q12", "Biophilic Design & Neural Reward", "Nature & Biophilia",
             "Does exposure to biophilic design elements (water features, natural textures, vegetation) activate reward-related neural circuits (ventral striatum, mPFC) more than aesthetically matched non-natural stimuli?",
             "natural__neural", "Mechanism gap; fMRI evidence almost absent from neuroarchitecture."),

            # ── Spatial Form (4 questions) ──
            ("Q03", "Ceiling Height & Creativity", "Spatial Form",
             "Does ceiling height influence divergent thinking independently of perceived spaciousness? What is the boundary condition at which the effect disappears?",
             "spatial__cog_performance", "Direction + Boundary gap; Meyers-Levy replication contested."),
            ("Q07", "Spatial Complexity & Wayfinding", "Spatial Form",
             "How does the visual complexity of a building interior affect wayfinding efficiency and associated stress — and does this interaction depend on the user's spatial ability?",
             "spatial__behav_navigation", "Mechanism gap; wayfinding literature is separate from neuroarchitecture."),
            ("Q13", "Enclosure Ratio & Stress Physiology", "Spatial Form",
             "What enclosure ratio (wall height to floor area) produces the lowest physiological stress markers (cortisol, EDA) during focused work, and does the optimal ratio shift between individual and collaborative tasks?",
             "spatial__physio", "Boundary gap; prospect-refuge theory predicts optimum but has not been tested parametrically."),
            ("Q14", "Spatial Openness & Social Interaction", "Spatial Form",
             "Does the degree of spatial openness in a shared workspace predict the frequency and quality of spontaneous social interaction, or do acoustic and visual privacy override spatial layout effects?",
             "spatial__social", "Direction gap; open-plan office debate lacks controlled spatial parametric studies."),

            # ── Acoustic Environment (4 questions) ──
            ("Q04", "Acoustic Environment & Mood", "Acoustic Environment",
             "What features of an acoustic environment — reverberation time, background noise level, spectral content — most reliably predict hedonic valence ratings from occupants?",
             "acoustic__affect_soundscape", "Multi-feature gap; almost no VR-based evidence."),
            ("Q15", "Background Noise & Working Memory", "Acoustic Environment",
             "At what sound pressure level does continuous background noise begin to impair working memory performance, and does the impairment threshold differ for speech-spectrum vs. broadband noise?",
             "acoustic__cog_memory", "Boundary gap; existing thresholds are task-specific and not generalized."),
            ("Q16", "Soundscape & Restorative Potential", "Acoustic Environment",
             "Can a designed soundscape (birdsong, flowing water, wind) in an indoor environment produce attentional restoration comparable to actual outdoor nature exposure as measured by ANT and PRS?",
             "acoustic__affect_restoration", "Direction gap; soundscape restoration literature is observational."),
            ("Q17", "Noise Exposure & Cardiovascular Health", "Acoustic Environment",
             "What is the dose-response relationship between chronic occupational noise exposure (40–70 dB LAeq) and cardiovascular health markers (blood pressure, resting heart rate) in office-type environments?",
             "acoustic__health", "Boundary gap; WHO noise guidelines extrapolate from transportation noise studies."),

            # ── Material & Surface (3 questions) ──
            ("Q05", "Wood Interiors & Wellbeing",  "Material & Surface",
             "Do visible wood surfaces in an interior environment predict wellbeing outcomes beyond what is explained by lighting and texture diversity alone?",
             "material__affect_wellbeing", "Low evidence base; Rice et al. 2006 is exploratory only."),
            ("Q18", "Surface Texture & Haptic Comfort", "Material & Surface",
             "Does the tactile roughness of interior surfaces (desks, walls, flooring) independently affect self-reported comfort and physiological arousal, or is the effect entirely mediated by visual texture perception?",
             "material__affect_comfort", "Mechanism gap; haptic vs. visual texture confounded in most material studies."),
            ("Q19", "Material Colour & Cognitive Performance", "Material & Surface",
             "Does the dominant colour of interior surfaces (warm vs. cool hues, saturation level) affect sustained attention or creative output when luminance and illuminance are controlled?",
             "material__cog_performance", "Direction gap; colour psychology findings rarely control for luminance confounds."),

            # ── Thermal & Air Quality (3 questions) ──
            ("Q20", "Temperature & Cognitive Performance", "Thermal & Air Quality",
             "What is the optimal indoor air temperature range for maximizing cognitive performance on complex tasks, and does the optimum shift with acclimatization, age, or clothing insulation?",
             "thermal__cog_performance", "Boundary gap; Seppänen et al. 2006 meta-analysis uses coarse categories."),
            ("Q21", "CO2 Concentration & Decision Quality", "Thermal & Air Quality",
             "At what CO2 concentration does strategic decision-making quality (measured by SMS or comparable instrument) begin to decline, and is the threshold lower for cognitively demanding vs. routine tasks?",
             "thermal__cog_cognitive_load", "Boundary gap; Allen et al. 2016 COGFX study needs replication across task types."),
            ("Q22", "Ventilation Rate & Subjective Wellbeing", "Thermal & Air Quality",
             "Does increasing ventilation rate above ASHRAE 62.1 minimums produce measurable gains in self-reported wellbeing and symptom reduction in occupied classrooms, and is the relationship linear or threshold-based?",
             "thermal__affect_wellbeing", "Direction gap; SBS literature is observational, few interventional classroom studies."),

            # ── Environmental Control (3 questions) ──
            ("Q23", "Personal Control & Stress Reduction", "Environmental Control",
             "Does giving occupants personal control over lighting, temperature, or acoustic conditions reduce physiological stress markers more than providing objectively optimal fixed conditions?",
             "control__affect_negative_stress", "Mechanism gap; perceived control confounded with actual environmental change."),
            ("Q24", "Autonomy Over Workspace & Task Performance", "Environmental Control",
             "Does the ability to reconfigure one's own workspace (desk position, partition height, lighting angle) improve task performance, and is the benefit mediated by sense of agency or by physical optimization?",
             "control__cog_performance", "Mechanism gap; autonomy effects conflated with ergonomic improvement."),
            ("Q25", "Smart Building Automation vs. Occupant Override", "Environmental Control",
             "When automated building systems override occupant preferences for energy efficiency, what is the net effect on occupant satisfaction, productivity, and physiological comfort compared to full manual control?",
             "control__affect_wellbeing", "Direction gap; smart building literature focuses on energy, not occupant outcomes."),

            # ── Social-Spatial (3 questions) ──
            ("Q26", "Density & Crowding Stress", "Social-Spatial",
             "What spatial density threshold (persons per square metre) triggers subjective crowding and elevated cortisol in shared workspaces, and does visual access to an exit or window moderate the threshold?",
             "social_spatial__affect_negative_stress", "Boundary gap; crowding literature is mostly residential or transportation."),
            ("Q27", "Privacy Gradient & Collaboration Quality", "Social-Spatial",
             "Does a graduated privacy gradient (open → semi-open → enclosed spaces within one floor) improve the quality of collaborative output compared to uniformly open or uniformly enclosed plans?",
             "social_spatial__social", "Direction gap; activity-based working studies are mostly survey-based."),
            ("Q28", "Shared vs. Assigned Seating & Belonging", "Social-Spatial",
             "Does hot-desking (unassigned seating) reduce employees' sense of belonging and territorial satisfaction compared to assigned desks, and does this effect persist after an acclimatization period?",
             "social_spatial__affect_wellbeing", "Direction gap; hot-desking studies confound policy with organisational culture."),

            # ── Multisensory / Cross-Domain (2 questions) ──
            ("Q29", "Multisensory Congruence & Restoration", "Multisensory",
             "Does congruence between visual (nature imagery), auditory (natural soundscape), and olfactory (forest scent) stimuli produce greater stress restoration than any single modality alone, and is the effect additive or superadditive?",
             "natural__affect_restoration", "Mechanism gap; crossmodal environment studies are rare and underpowered."),
            ("Q30", "Lighting × Acoustics Interaction on Focus", "Multisensory",
             "How do lighting level and background noise level interact in their effects on sustained attention — is the interaction additive, or does one modality dominate under specific conditions?",
             "luminous__cog_attention", "Mechanism gap; lighting and acoustics studied independently in most cognition work."),
        ]
        db.executemany(
            "INSERT INTO research_questions VALUES (?,?,?,?,?,?)", questions)

    # Seed instructor account if no instructor exists
    instr = db.execute("SELECT user_id FROM users WHERE role='instructor' LIMIT 1").fetchone()
    if not instr:
        uid = "instructor_kirsh"
        email = "dkirsh@ucsd.edu"
        ph = pwd_context.hash("atlas2026")
        now = datetime.now(timezone.utc).isoformat()
        db.execute("""INSERT OR IGNORE INTO users
            (user_id,email,first_name,last_name,role,password_hash,status,created_at,approved_at)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (uid, email, "David", "Kirsh", "instructor", ph, "approved", now, now))
        print("[KA-AUTH] Seeded instructor account: dkirsh@ucsd.edu / atlas2026")
        print("[KA-AUTH] ← Change this password immediately via POST /auth/change-password")

    db.commit()
    db.close()

# ════════════════════════════════════════════════
# JWT HELPERS
# ════════════════════════════════════════════════
def create_access_token(user_id: str, role: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": user_id, "role": role, "exp": exp, "type": "access"},
                      SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    token = secrets.token_urlsafe(48)
    exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    db = get_db()
    db.execute("INSERT INTO refresh_tokens VALUES (?,?,?,0)",
               (token, user_id, exp.isoformat()))
    db.commit(); db.close()
    return token

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise JWTError("wrong token type")
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if not creds:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_access_token(creds.credentials)
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE user_id=?", (payload["sub"],)).fetchone()
    db.close()
    if not row:
        raise HTTPException(status_code=401, detail="User not found")
    if row["status"] != "approved":
        raise HTTPException(status_code=403, detail="Account not yet approved by instructor")
    return dict(row)

def require_instructor(user=Depends(get_current_user)):
    if user["role"] not in ("instructor", "admin"):
        raise HTTPException(status_code=403, detail="Instructor access required")
    return user

# ════════════════════════════════════════════════
# PYDANTIC MODELS
# ════════════════════════════════════════════════
class RegisterRequest(BaseModel):
    email:       str
    password:    str
    first_name:  str
    last_name:   str
    department:  str = ""
    track:       str = ""
    question_id: str = ""

class LoginRequest(BaseModel):
    email:    str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token:        str
    new_password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password:     str

class ApproveRequest(BaseModel):
    track:       str = ""
    question_id: str = ""

class RejectRequest(BaseModel):
    reason: str = "Application not approved"

# ════════════════════════════════════════════════
# APP
# ════════════════════════════════════════════════
app = FastAPI(title="Knowledge Atlas Auth API", version="1.0.0",
              description="Lightweight JWT authentication for Knowledge Atlas (local dev)")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],   # file:// + localhost during local dev
    allow_methods=["*"],
    allow_headers=["*"])

# ── REGISTER
@app.post("/auth/register", status_code=201)
def register(req: RegisterRequest):
    if len(req.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    email = req.email.strip().lower()
    uid = "u_" + secrets.token_hex(8)
    ph  = pwd_context.hash(req.password)
    now = datetime.now(timezone.utc).isoformat()
    db  = get_db()
    try:
        db.execute("""INSERT INTO users
            (user_id,email,first_name,last_name,role,password_hash,status,
             track,question_id,department,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (uid, email, req.first_name.strip(), req.last_name.strip(),
             "student", ph, "pending",
             req.track, req.question_id, req.department, now))
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(409, "An account with that email already exists")
    finally:
        db.close()
    return {"message": "Registration received. Your account is pending instructor approval.",
            "user_id": uid, "status": "pending"}

# ── LOGIN
@app.post("/auth/login")
def login(req: LoginRequest):
    email = req.email.strip().lower()
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    db.close()
    if not row or not pwd_context.verify(req.password, row["password_hash"]):
        raise HTTPException(401, "Incorrect email or password")
    if row["status"] == "pending":
        raise HTTPException(403, "Your account is pending approval. Check back after the instructor reviews it.")
    if row["status"] == "rejected":
        raise HTTPException(403, "Your account application was not approved. Contact the course instructor.")
    # Update last_login
    db = get_db()
    db.execute("UPDATE users SET last_login=? WHERE user_id=?",
               (datetime.now(timezone.utc).isoformat(), row["user_id"]))
    db.commit(); db.close()
    access  = create_access_token(row["user_id"], row["role"])
    refresh = create_refresh_token(row["user_id"])
    return {
        "access_token":  access,
        "refresh_token": refresh,
        "token_type":    "bearer",
        "user": {
            "user_id":    row["user_id"],
            "email":      row["email"],
            "first_name": row["first_name"],
            "last_name":  row["last_name"],
            "role":       row["role"],
            "track":      row["track"],
            "question_id": row["question_id"],
        }
    }

# ── FORGOT PASSWORD
@app.post("/auth/forgot-password")
def forgot_password(req: ForgotPasswordRequest):
    email = req.email.strip().lower()
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    # Always return 200 to avoid leaking which emails are registered
    if not row:
        db.close()
        return {"message": "If that email is registered, a reset link has been sent."}
    token = secrets.token_urlsafe(32)
    exp   = (datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)).isoformat()
    db.execute("INSERT INTO reset_tokens VALUES (?,?,?,0)", (token, row["user_id"], exp))
    db.commit(); db.close()
    # In local dev: print the link to console instead of sending email
    reset_url = f"http://localhost:8765/reset?token={token}"
    print(f"\n[KA-AUTH] PASSWORD RESET REQUEST")
    print(f"  Email:     {email}")
    print(f"  Name:      {row['first_name']} {row['last_name']}")
    print(f"  Reset URL: {reset_url}")
    print(f"  Expires:   {exp}\n")
    return {
        "message": "If that email is registered, a reset link has been sent.",
        "_dev_note": "Running in local mode — reset link printed to server console.",
        "_dev_reset_url": reset_url  # Only exposed in local/dev mode
    }

# ── RESET PASSWORD
@app.post("/auth/reset-password")
def reset_password(req: ResetPasswordRequest):
    if len(req.new_password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    db = get_db()
    row = db.execute("""SELECT * FROM reset_tokens
                        WHERE token=? AND used=0""", (req.token,)).fetchone()
    if not row:
        db.close()
        raise HTTPException(400, "Reset token is invalid or has already been used")
    exp = datetime.fromisoformat(row["expires_at"])
    if exp < datetime.now(timezone.utc):
        db.close()
        raise HTTPException(400, "Reset token has expired. Request a new one.")
    ph = pwd_context.hash(req.new_password)
    db.execute("UPDATE users SET password_hash=? WHERE user_id=?", (ph, row["user_id"]))
    db.execute("UPDATE reset_tokens SET used=1 WHERE token=?", (req.token,))
    db.commit(); db.close()
    return {"message": "Password updated successfully. You can now log in."}

# ── CHANGE PASSWORD (authenticated)
@app.post("/auth/change-password")
def change_password(req: ChangePasswordRequest, user=Depends(get_current_user)):
    db = get_db()
    row = db.execute("SELECT password_hash FROM users WHERE user_id=?",
                     (user["user_id"],)).fetchone()
    if not pwd_context.verify(req.current_password, row["password_hash"]):
        db.close()
        raise HTTPException(400, "Current password is incorrect")
    if len(req.new_password) < 8:
        db.close()
        raise HTTPException(400, "New password must be at least 8 characters")
    db.execute("UPDATE users SET password_hash=? WHERE user_id=?",
               (pwd_context.hash(req.new_password), user["user_id"]))
    db.commit(); db.close()
    return {"message": "Password changed successfully"}

# ── ME
@app.get("/auth/me")
def me(user=Depends(get_current_user)):
    return {k: user[k] for k in
            ("user_id","email","first_name","last_name","role","status","track","question_id","last_login")}

# ── ASSIGNMENTS
@app.get("/api/assignments")
def get_assignment(user=Depends(get_current_user)):
    if not user["question_id"]:
        return {"assigned": False,
                "message": "No question assigned yet. Contact the course instructor."}
    db = get_db()
    q = db.execute("SELECT * FROM research_questions WHERE question_id=?",
                   (user["question_id"],)).fetchone()
    db.close()
    if not q:
        return {"assigned": False, "message": "Question not found in database"}
    return {
        "assigned":    True,
        "question_id": q["question_id"],
        "label":       q["label"],
        "domain":      q["domain"],
        "text":        q["text"],
        "atlas_topic": q["atlas_topic"],
        "notes":       q["notes"],
    }

# ── RESEARCH QUESTIONS LIST
@app.get("/api/questions")
def list_questions(user=Depends(require_instructor)):
    db = get_db()
    rows = db.execute("SELECT * FROM research_questions ORDER BY question_id").fetchall()
    db.close()
    return [dict(r) for r in rows]

# ── INSTRUCTOR: list pending registrations
@app.get("/api/registrations")
def list_registrations(status_filter: str = "pending", user=Depends(require_instructor)):
    db = get_db()
    rows = db.execute(
        "SELECT user_id,email,first_name,last_name,department,track,question_id,status,created_at FROM users WHERE status=? ORDER BY created_at DESC",
        (status_filter,)).fetchall()
    db.close()
    return [dict(r) for r in rows]

# ── INSTRUCTOR: approve registration
@app.post("/api/registrations/{uid}/approve")
def approve_registration(uid: str, req: ApproveRequest, user=Depends(require_instructor)):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE user_id=?", (uid,)).fetchone()
    if not row:
        db.close()
        raise HTTPException(404, "User not found")
    now = datetime.now(timezone.utc).isoformat()
    db.execute("""UPDATE users SET status='approved', approved_at=?, track=?, question_id=?
                  WHERE user_id=?""",
               (now, req.track or row["track"], req.question_id or row["question_id"], uid))
    db.commit(); db.close()
    return {"message": f"Approved {row['email']}",
            "track": req.track, "question_id": req.question_id}

# ── INSTRUCTOR: reject registration
@app.post("/api/registrations/{uid}/reject")
def reject_registration(uid: str, req: RejectRequest, user=Depends(require_instructor)):
    db = get_db()
    db.execute("UPDATE users SET status='rejected' WHERE user_id=?", (uid,))
    db.commit(); db.close()
    return {"message": f"Rejected registration for {uid}"}

# ── HEALTH CHECK
@app.get("/health")
def health():
    return {"status": "ok", "server": "Knowledge Atlas Auth", "version": "1.1.0",
            "modules": ["auth", "articles"]}

# ════════════════════════════════════════════════
# ARTICLE SUBMISSION MODULE
# ════════════════════════════════════════════════
# Import and configure the article submission endpoints (see ka_article_endpoints.py)
try:
    import ka_article_endpoints
    ka_article_endpoints.configure(
        get_db=get_db,
        get_current_user=get_current_user,
        get_current_user_optional=None,  # articles module uses its own optional auth
        require_instructor=require_instructor,
    )
    app.include_router(ka_article_endpoints.router)
    print("[KA-AUTH] Article submission module loaded ✓")
except ImportError as e:
    print(f"[KA-AUTH] Article submission module not available: {e}")
    print("[KA-AUTH] Server running with auth-only endpoints")

# ── RESET PAGE REDIRECT (convenience link in reset email)
@app.get("/reset")
def reset_page_redirect(token: str):
    from fastapi.responses import HTMLResponse
    return HTMLResponse(f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url=ka_reset_password.html?token={token}">
<title>Redirecting…</title></head>
<body><p>Redirecting to password reset page…
<a href="ka_reset_password.html?token={token}">Click here if not redirected</a></p>
</body></html>""")

# ════════════════════════════════════════════════
# ENTRY POINT
# ════════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn
    init_db()
    # Initialize article tables if module is loaded
    try:
        ka_article_endpoints._init_article_tables()
        print("[KA-AUTH] Article tables initialized ✓")
    except Exception as e:
        print(f"[KA-AUTH] Article table init skipped: {e}")
    print("\n" + "═"*60)
    print("  Knowledge Atlas Auth Server")
    print("  http://localhost:8765")
    print("  API docs: http://localhost:8765/docs")
    print("  Health:   http://localhost:8765/health")
    print()
    print("  Instructor login:")
    print("    Email:    dkirsh@ucsd.edu")
    print("    Password: atlas2026")
    print("    (Change this! POST /auth/change-password)")
    print("═"*60 + "\n")
    uvicorn.run("ka_auth_server:app", host="127.0.0.1", port=8765,
                reload=True, reload_dirs=[str(BASE_DIR)])
