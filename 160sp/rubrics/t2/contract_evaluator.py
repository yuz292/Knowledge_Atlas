"""
Contract Quality Evaluator — Shared module for T2 grading
==========================================================
Scans a student's submission for contracts, success conditions,
test checklists, and validation evidence. Returns a structured
quality assessment with a PASS / FAIL gate.

A contract is ADEQUATE if it has:
  1. Inputs section (what the program reads)
  2. Processing section (what the program does)
  3. Outputs section (what the program produces)
  4. Success conditions (how you know it worked — specific, not "it works")
  5. Test checklist (pre-build tests, not just "run it and see")

A submission with inadequate contracts is flagged:
  ⛔ CONTRACTS INSUFFICIENT — do not integrate student outputs
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ════════════════════════════════════════════════
# DATA MODEL
# ════════════════════════════════════════════════

@dataclass
class ContractAssessment:
    """Assessment of a single contract document."""
    source_file: str
    has_inputs: bool = False
    has_processing: bool = False
    has_outputs: bool = False
    has_success_conditions: bool = False
    has_test_checklist: bool = False
    success_conditions_specific: bool = False  # not just "it works"
    test_count: int = 0
    section_count: int = 0  # how many of the 4 core sections found
    quality: str = ""  # STRONG, ADEQUATE, WEAK, MISSING

    def evaluate(self):
        self.section_count = sum([
            self.has_inputs, self.has_processing,
            self.has_outputs, self.has_success_conditions,
        ])
        if self.section_count >= 4 and self.has_test_checklist and self.success_conditions_specific:
            self.quality = "STRONG"
        elif self.section_count >= 3 and (self.has_test_checklist or self.success_conditions_specific):
            self.quality = "ADEQUATE"
        elif self.section_count >= 2:
            self.quality = "WEAK"
        else:
            self.quality = "MISSING"
        return self


@dataclass
class ContractGateResult:
    """Aggregate result across all contracts in a submission."""
    contracts_found: list = field(default_factory=list)
    contracts_expected: int = 0
    gate_passed: bool = False
    gate_reason: str = ""
    summary: str = ""
    score: int = 0       # 0-20 points
    max_score: int = 20

    def render_table(self) -> str:
        """Render as markdown table for the grade report."""
        lines = [
            "## Contract Quality Assessment",
            "",
        ]
        if not self.gate_passed:
            lines += [
                "### ⛔ CONTRACTS INSUFFICIENT",
                "",
                f"**Reason:** {self.gate_reason}",
                "",
                "> Student outputs should NOT be integrated into the corpus until",
                "> contracts are revised and resubmitted.",
                "",
            ]

        lines += [
            f"**Score: {self.score} / {self.max_score}**",
            "",
            "| Source File | Inputs | Processing | Outputs | Success Conds | Tests | Quality |",
            "|------------|--------|------------|---------|---------------|-------|---------|",
        ]
        for c in self.contracts_found:
            def yn(b): return "✅" if b else "❌"
            lines.append(
                f"| {c.source_file} "
                f"| {yn(c.has_inputs)} "
                f"| {yn(c.has_processing)} "
                f"| {yn(c.has_outputs)} "
                f"| {yn(c.has_success_conditions)} "
                f"| {c.test_count} tests "
                f"| **{c.quality}** |"
            )

        if not self.contracts_found:
            lines.append("| (none found) | ❌ | ❌ | ❌ | ❌ | 0 | **MISSING** |")

        lines += ["", f"**Gate:** {'✅ PASSED' if self.gate_passed else '⛔ FAILED'} — {self.gate_reason}", ""]
        return "\n".join(lines)


# ════════════════════════════════════════════════
# DETECTION PATTERNS
# ════════════════════════════════════════════════

# Patterns for contract sections (case-insensitive)
INPUT_PATTERNS = [
    r"#+\s*inputs?\b", r"\*\*inputs?\*\*", r"^inputs?\s*[:—\-]",
    r"reads?\s+(from|the)", r"takes?\s+(as\s+)?input",
]
PROCESSING_PATTERNS = [
    r"#+\s*processing\b", r"\*\*processing\*\*", r"^processing\s*[:—\-]",
    r"#+\s*steps?\b", r"#+\s*algorithm\b", r"for\s+each\s+(template|gap|paper|query)",
]
OUTPUT_PATTERNS = [
    r"#+\s*outputs?\b", r"\*\*outputs?\*\*", r"^outputs?\s*[:—\-]",
    r"produces?\s+(a|the|structured)", r"returns?\s+(a|the|structured)",
]
SUCCESS_PATTERNS = [
    r"#+\s*success\s+cond", r"\*\*success\s+cond", r"success\s+cond\w*\s*[:—\-]",
    r"#+\s*acceptance\s+cri", r"how\s+(?:do\s+)?(?:you|we)\s+know\s+it\s+worked",
    r"must\s+(?:produce|generate|output|return)\s+at\s+least",
]
TEST_PATTERNS = [
    r"\[\s*\]\s+", r"\[x\]\s+", r"\[/\]\s+",  # checkbox items
    r"#+\s*tests?\b", r"\*\*tests?\*\*", r"test\s+checklist",
    r"validation\s+checklist", r"verify\s+that",
]

# Bad success conditions (too vague)
VAGUE_SUCCESS = [
    r"it\s+works", r"runs?\s+correctly", r"no\s+errors",
    r"produces?\s+output", r"everything\s+(is\s+)?ok",
]

# Specific success conditions (good)
SPECIFIC_SUCCESS = [
    r"at\s+least\s+\d+", r"≥\s*\d+", r">=\s*\d+", r"\d+%",
    r"sorted\s+by", r"each\s+\w+\s+has", r"never\s+(crash|fail|drop)",
    r"between\s+0\s+and\s+1", r"valid\s+(json|csv|format)",
]


# ════════════════════════════════════════════════
# SCANNER
# ════════════════════════════════════════════════

def _check_patterns(text: str, patterns: list[str]) -> bool:
    """Check if any pattern matches in the text."""
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE | re.MULTILINE):
            return True
    return False


def _count_test_items(text: str) -> int:
    """Count checklist items ([ ], [x], [/]) in text."""
    return len(re.findall(r"\[\s*[x/]?\s*\]", text, re.IGNORECASE))


def assess_contract_in_text(text: str, source: str) -> ContractAssessment:
    """Assess a single text blob for contract quality."""
    c = ContractAssessment(source_file=source)
    c.has_inputs = _check_patterns(text, INPUT_PATTERNS)
    c.has_processing = _check_patterns(text, PROCESSING_PATTERNS)
    c.has_outputs = _check_patterns(text, OUTPUT_PATTERNS)
    c.has_success_conditions = _check_patterns(text, SUCCESS_PATTERNS)
    c.has_test_checklist = _check_patterns(text, TEST_PATTERNS)
    c.test_count = _count_test_items(text)

    # Check if success conditions are specific (not vague)
    if c.has_success_conditions:
        has_vague = _check_patterns(text, VAGUE_SUCCESS)
        has_specific = _check_patterns(text, SPECIFIC_SUCCESS)
        c.success_conditions_specific = has_specific and not has_vague
        if has_specific and has_vague:
            c.success_conditions_specific = True  # specific ones present, vague ones tolerable

    c.evaluate()
    return c


def scan_for_contracts(repo: Path, expected_contracts: int = 2) -> ContractGateResult:
    """
    Scan a student repo for contract documents.
    
    Looks in:
    1. Standalone markdown files (contract*.md, spec*.md)
    2. Python file docstrings and comments
    3. README or submission docs
    """
    gate = ContractGateResult(contracts_expected=expected_contracts)
    assessed = []

    # 1. Scan markdown files
    for md_pat in ["*contract*.md", "*spec*.md", "*design*.md", "README*.md",
                   "docs/*.md", "submission*.md", "*requirements*.md"]:
        for f in repo.glob(md_pat):
            try:
                text = f.read_text(errors="replace")
                if len(text) > 100:  # skip trivially small files
                    a = assess_contract_in_text(text, str(f.relative_to(repo)))
                    if a.section_count >= 2:  # at least looks like a contract
                        assessed.append(a)
            except Exception:
                pass

    # 2. Scan Python files for embedded contracts (docstrings/comments)
    for py_pat in ["*.py", "scripts/*.py", "pipeline/*.py"]:
        for f in repo.glob(py_pat):
            try:
                text = f.read_text(errors="replace")
                # Extract docstrings and large comment blocks
                docstrings = re.findall(r'"""(.*?)"""', text, re.DOTALL)
                docstrings += re.findall(r"'''(.*?)'''", text, re.DOTALL)
                # Also check for comment blocks (lines starting with #)
                comment_blocks = []
                current_block = []
                for line in text.split("\n"):
                    stripped = line.strip()
                    if stripped.startswith("#") and not stripped.startswith("#!"):
                        current_block.append(stripped[1:].strip())
                    else:
                        if len(current_block) >= 5:  # substantial comment block
                            comment_blocks.append("\n".join(current_block))
                        current_block = []
                
                all_text = "\n".join(docstrings + comment_blocks)
                if len(all_text) > 100:
                    a = assess_contract_in_text(all_text, f"{f.relative_to(repo)} (docstring)")
                    if a.section_count >= 2:
                        assessed.append(a)
            except Exception:
                pass

    # 3. Score and gate
    gate.contracts_found = assessed

    if not assessed:
        gate.gate_passed = False
        gate.gate_reason = "No contracts found anywhere in submission"
        gate.score = 0
        gate.summary = "⛔ NO CONTRACTS FOUND"
        return gate

    # Score: best contract quality determines base, count adds bonus
    quality_scores = {"STRONG": 16, "ADEQUATE": 12, "WEAK": 6, "MISSING": 0}
    best_quality = max(assessed, key=lambda a: quality_scores.get(a.quality, 0))
    base = quality_scores[best_quality.quality]

    # Bonus for having multiple contracts
    strong_or_adequate = sum(1 for a in assessed if a.quality in ("STRONG", "ADEQUATE"))
    bonus = min(4, strong_or_adequate)  # up to 4 bonus points for multiple good contracts

    gate.score = min(20, base + bonus)

    # Gate logic: need at least one ADEQUATE contract
    has_adequate = any(a.quality in ("STRONG", "ADEQUATE") for a in assessed)
    has_tests = any(a.test_count >= 3 for a in assessed)
    has_success = any(a.success_conditions_specific for a in assessed)

    if has_adequate and has_tests and has_success:
        gate.gate_passed = True
        gate.gate_reason = f"{len(assessed)} contract(s) found, quality sufficient for integration"
    elif has_adequate:
        gate.gate_passed = True
        gate.gate_reason = (
            f"{len(assessed)} contract(s) found — ADEQUATE but missing "
            f"{'tests' if not has_tests else 'specific success conditions'}"
        )
    else:
        gate.gate_passed = False
        qualities = [a.quality for a in assessed]
        gate.gate_reason = (
            f"{len(assessed)} contract(s) found but quality insufficient: {qualities}. "
            "Need at least one ADEQUATE contract with specific success conditions."
        )

    gate.summary = (
        f"{'✅ GATE PASSED' if gate.gate_passed else '⛔ GATE FAILED'}: "
        f"{len(assessed)} contracts, best={best_quality.quality}, "
        f"score={gate.score}/{gate.max_score}"
    )
    return gate
