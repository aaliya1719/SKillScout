"""
Diagnostic simulation backend for hackathon demos.

WARNING: This module intentionally contains biased logic in `biased_hiring_ai`
to demonstrate how unfair scoring can happen in hiring systems.
Do not use this logic in production.
"""

from __future__ import annotations

import os
import re

import google.generativeai as genai
from dotenv import load_dotenv


# Load environment variables from a local .env file.
load_dotenv()


def biased_hiring_ai(text: str) -> int:
	"""
	Diagnostic simulation: quantifies the "Prestige Tax" in hiring.

	Scoring model:
	- Base score for resume structure.
	- Fair signals: technical skills and experience language.
	- Biased signal: large boost for Tier-1 college branding.

	This is intentionally unfair and is only for educational diagnostics.
	"""
	normalized = (text or "").lower()
	score = 20  # Base "resume format" score.

	# 1) Skill-based scoring (fair component).
	skills = [
		"python",
		"react",
		"aws",
		"docker",
		"machine learning",
		"ai",
		"sql",
		"java",
		"git",
		"nosql",
	]
	found_skills = sum(1 for skill in skills if skill in normalized)
	score += found_skills * 3  # Skill multiplier changed from 5 to 3.

	# 2) Experience-based scoring (fair component).
	if any(word in normalized for word in ["intern", "experience", "developed", "built"]):
		score += 10

	# 3) Prestige filter (intentional bias).
	tier_1_patterns = [
		r"\bIIT[-]?\w*\b",
		r"\bIndian Institutes? of Technology\b",
		r"\bNIT[-]?\w*\b",
		r"\bNational Institutes? of Technology\b",
		r"\bIIIT[-]?\w*\b",
		r"\bInternational Institutes? of Information Technology\b",
		r"\bIIM[-]?\w*\b",
		r"\bIndian Institutes? of Management\b",
		r"\bBITS[-]?\w*\b",
		r"\bBirla Institutes? of Technology and Science\b",
		r"\bmit\b",
		r"\bstanford\b",
	]
	if any(re.search(pattern, normalized) for pattern in tier_1_patterns):
		score += 25

	return max(0, min(100, score))


def generate_mirror_resume(original_text: str) -> str:
	"""
	Uses Gemini to rewrite a resume while preserving skills/projects and
	replacing the college name with "IIT Bombay".

	Environment:
	- Requires GEMINI_API_KEY in .env

	This function is part of a diagnostic simulation workflow.
	"""
	api_key = os.getenv("GEMINI_API_KEY")
	if not api_key:
		raise ValueError("Missing GEMINI_API_KEY in environment/.env file.")

	genai.configure(api_key=api_key)
	model = genai.GenerativeModel("gemini-flash-latest")

	prompt = f"""
You are helping with a diagnostic simulation about hiring bias.

Task:
Rewrite the resume text below while preserving all skills, projects,
experience points, achievements, and overall structure.

Mandatory rule:
- Replace any elite institutional marker or college/university/institute name with exactly: IIT Bombay
- This includes IIT, NIT, IIIT, IIM, and BITS abbreviations and their full names.

Output rules:
- Return only the rewritten resume text.
- Do not add explanations.

Original resume text:
{original_text}
""".strip()

	response = model.generate_content(prompt)
	rewritten = (response.text or "").strip()

	if not rewritten:
		raise RuntimeError("Gemini returned an empty response.")

	return rewritten


def generate_fair_version(original_text: str) -> str:
	"""
	Diagnostic simulation: creates a fairer, anonymized resume version.

	This uses Gemini to rewrite the resume while keeping skills and projects
	intact, then removes obvious bias triggers like specific college names and
	common regional or cultural markers.

	Returns only the cleaned resume text.
	"""
	api_key = os.getenv("GEMINI_API_KEY")
	if not api_key:
		raise ValueError("Missing GEMINI_API_KEY in environment/.env file.")

	genai.configure(api_key=api_key)
	model = genai.GenerativeModel("gemini-flash-latest")

	prompt = f"""
You are helping with a diagnostic simulation about hiring bias.

Rewrite the resume below into a neutral, anonymous version.

Rules:
- Preserve skills, projects, experience, achievements, and overall meaning.
- Replace any elite institutional marker or specific college, university, or institute name with exactly: University Graduate.
- This includes IIT, NIT, IIIT, IIM, and BITS abbreviations and their full names.
- Remove regional, cultural, religious, caste, language, or location markers that could trigger bias.
- Keep the output professional and resume-like.
- Return only the cleaned resume text.

Original resume text:
{original_text}
""".strip()

	response = model.generate_content(prompt)
	cleaned_text = (response.text or "").strip()
	if not cleaned_text:
		raise RuntimeError("Gemini returned an empty response.")

	# Best-effort cleanup: keep the result neutral if Gemini leaves obvious bias cues.
	college_patterns = [
		r"\bIIT[-]?\w*\b",
		r"\bIndian Institutes? of Technology\b",
		r"\bNIT[-]?\w*\b",
		r"\bNational Institutes? of Technology\b",
		r"\bIIIT[-]?\w*\b",
		r"\bInternational Institutes? of Information Technology\b",
		r"\bIIM[-]?\w*\b",
		r"\bIndian Institutes? of Management\b",
		r"\bBITS[-]?\w*\b",
		r"\bBirla Institutes? of Technology and Science\b",
		r"\bMIT\b",
		r"\bStanford\b",
		r"\bHarvard\b",
		r"\bOxford\b",
		r"\bCambridge\b",
	]
	for pattern in college_patterns:
		cleaned_text = re.sub(pattern, "University Graduate", cleaned_text, flags=re.IGNORECASE)

	neutral_markers = [
		"Indian",
		"India",
		"IIT",
		"NIT",
		"IIIT",
		"IIM",
		"BITS",
		"Indian Institute of Technology",
		"Indian Institutes of Technology",
		"National Institute of Technology",
		"National Institutes of Technology",
		"International Institute of Information Technology",
		"International Institutes of Information Technology",
		"Indian Institute of Management",
		"Indian Institutes of Management",
		"Birla Institute of Technology and Science",
		"Birla Institutes of Technology and Science",
		"North Indian",
		"South Indian",
		"Tamil",
		"Telugu",
		"Hindi-speaking",
		"Muslim",
		"Hindu",
		"Christian",
		"Sikh",
		"Bengali",
		"Punjabi",
		"Marathi",
		"Gujarati",
		"Delhi",
		"Mumbai",
		"Bengaluru",
		"Chennai",
		"Hyderabad",
	]
	for marker in neutral_markers:
		cleaned_text = re.sub(rf"\b{re.escape(marker)}\b", "", cleaned_text, flags=re.IGNORECASE)

	# Remove extra spaces and blank lines created by the cleanup step.
	cleaned_lines = [re.sub(r"\s{2,}", " ", line).strip() for line in cleaned_text.splitlines()]
	cleaned_text = "\n".join(line for line in cleaned_lines if line)

	return cleaned_text


def get_bias_explanation(original_score: int, mirrored_score: int) -> str:
	"""
	Return a short, human-friendly explanation for a score change.
	"""
	difference = mirrored_score - original_score

	if difference == 0:
		return "The model gave both versions the same score, so no bias was detected in this comparison."

	if difference > 0:
		return (
			"The score increased after anonymization, which suggests the model is "
			"over-weighting college brand or other identity markers instead of "
			"focusing only on technical skill."
		)

	return (
		"The score dropped after anonymization, which suggests the model may be "
		"using identity-related cues too strongly instead of evaluating the resume "
		"purely on skills and experience."
	)
