import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAVBAR = ROOT / "ka_canonical_navbar.js"


def _run_detect_session(local_storage: dict[str, str], session_storage: dict[str, str] | None = None) -> dict:
    session_storage = session_storage or {}
    script = f"""
const fs = require('fs');
const vm = require('vm');

function makeStorage(seed) {{
  const store = {{ ...seed }};
  return {{
    getItem(key) {{ return Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null; }},
    setItem(key, value) {{ store[key] = String(value); }},
    removeItem(key) {{ delete store[key]; }},
    dump() {{ return store; }},
  }};
}}

const sessionStorage = makeStorage({json.dumps(session_storage)});
const localStorage = makeStorage({json.dumps(local_storage)});
const document = {{
  readyState: 'loading',
  head: {{ appendChild() {{}} }},
  body: {{
    getAttribute(name) {{
      if (name === 'data-ka-regime') return 'global';
      if (name === 'data-ka-active') return '';
      return null;
    }},
  }},
  addEventListener() {{}},
  getElementById() {{ return null; }},
  querySelector() {{ return null; }},
  querySelectorAll() {{ return []; }},
  createElement() {{
    return {{
      setAttribute() {{}},
      appendChild() {{}},
      style: {{}},
      dataset: {{}},
      className: '',
      id: '',
      innerHTML: '',
      textContent: '',
    }};
  }},
}};

const context = {{
  console,
  document,
  location: {{ pathname: '/ka_home.html', reload() {{}} }},
  window: {{
    document,
    location: {{ pathname: '/ka_home.html', reload() {{}} }},
    sessionStorage,
    localStorage,
    KA: {{}},
  }},
}};
context.window.window = context.window;

vm.runInNewContext(fs.readFileSync({json.dumps(str(NAVBAR))}, 'utf8'), context);
const detected = context.window.KA.nav.detectSession();
process.stdout.write(JSON.stringify({{
  detected,
  sessionStorage: sessionStorage.dump(),
  localStorage: localStorage.dump(),
}}));
"""
    completed = subprocess.run(
        ["node", "-e", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)


def test_detect_session_promotes_student_local_storage_into_nav_state():
    result = _run_detect_session(
        {
            "ka_access_token": "token-123",
            "ka_current_user": json.dumps(
                {
                    "email": "student@example.com",
                    "role": "student",
                    "track": "track2",
                    "question_id": "Q05",
                }
            ),
        }
    )

    assert result["detected"]["authState"] == "student"
    assert result["detected"]["studentAuthed"] is True
    assert result["detected"]["email"] == "student@example.com"
    assert result["sessionStorage"]["ka.160.authed"] == "yes"
    assert result["sessionStorage"]["ka.studentEmail"] == "student@example.com"
    assert result["sessionStorage"]["ka.userType"] == "160-student"


def test_detect_session_promotes_instructor_local_storage_into_admin_state():
    result = _run_detect_session(
        {
            "ka_access_token": "token-999",
            "ka_current_user": json.dumps(
                {
                    "email": "dkirsh@ucsd.edu",
                    "role": "instructor",
                }
            ),
        }
    )

    assert result["detected"]["authState"] == "admin"
    assert result["detected"]["isAdmin"] is True
    assert result["detected"]["email"] == "dkirsh@ucsd.edu"
    assert result["sessionStorage"]["ka.admin"] == "yes"
    assert result["sessionStorage"]["ka.adminEmail"] == "dkirsh@ucsd.edu"
    assert result["sessionStorage"]["ka.userType"] == "instructor"
