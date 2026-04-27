import streamlit as st

from engine import (
	biased_hiring_ai,
	generate_fair_version,
	generate_mirror_resume,
	get_bias_explanation,
)


# Page setup: title shown in browser tab and layout width.
st.set_page_config(page_title="HR Fairness Audit Tool", layout="wide")


# Small CSS block for a clean, professional HR dashboard look.
st.markdown(
	"""
	<style>
		@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

		:root {
			--bg: #f5f7fb;
			--surface: #ffffff;
			--surface-2: #f8fafc;
			--text: #172033;
			--muted: #64748b;
			--line: #dde5f0;
			--primary: #4285F4;
			--primary-dark: #3367d6;
			--success: #137333;
			--success-bg: #e7f6ed;
			--danger: #b42318;
			--danger-bg: #fee4e2;
		}

		.stApp {
			background:
				linear-gradient(180deg, rgba(245,247,251,0.92) 0%, rgba(238,243,250,0.98) 100%),
				linear-gradient(135deg, #f7f9fc 0%, #eef3ff 100%);
			color: var(--text);
			font-family: 'Inter', sans-serif;
		}

		.block-container {
			padding-top: 1.5rem;
			padding-bottom: 2.5rem;
			max-width: 1220px;
		}

		/* Hero section at the top of the dashboard */
		.hero-shell {
			background: linear-gradient(135deg, #4169e1 0%, #6f42f4 100%);
			border-radius: 24px;
			padding: 2rem 2.1rem;
			box-shadow: 0 18px 40px rgba(41, 67, 125, 0.18);
			color: #ffffff;
			margin-bottom: 1.25rem;
		}

		.hero-kicker {
			font-size: 0.82rem;
			font-weight: 700;
			letter-spacing: 0.08em;
			text-transform: uppercase;
			opacity: 0.9;
		}

		.hero-title {
			font-size: 2.2rem;
			font-weight: 800;
			line-height: 1.1;
			margin-top: 0.35rem;
			margin-bottom: 0.45rem;
		}

		.hero-copy {
			font-size: 1rem;
			max-width: 900px;
			opacity: 0.94;
			line-height: 1.6;
		}

		.section-title {
			font-size: 1.25rem;
			font-weight: 700;
			margin: 0 0 0.25rem 0;
		}

		.section-subtitle {
			color: var(--muted);
			font-size: 0.95rem;
			margin-bottom: 1rem;
		}

		.section-shell {
			background: rgba(255, 255, 255, 0.72);
			border: 1px solid rgba(221, 229, 240, 0.95);
			border-radius: 22px;
			padding: 1.2rem;
			box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
			backdrop-filter: blur(8px);
			margin-bottom: 1rem;
		}

		.audit-card {
			background: var(--surface);
			border: 1px solid var(--line);
			border-radius: 15px;
			padding: 1rem 1rem 1.1rem 1rem;
			box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
			height: 100%;
		}

		.card-title {
			font-size: 1.04rem;
			font-weight: 700;
			margin-bottom: 0.1rem;
		}

		.card-meta {
			color: var(--muted);
			font-size: 0.9rem;
			margin-bottom: 0.75rem;
		}

		.score-badge,
		.status-badge {
			display: inline-flex;
			align-items: center;
			gap: 0.35rem;
			padding: 0.42rem 0.75rem;
			border-radius: 999px;
			font-weight: 700;
			font-size: 0.85rem;
			line-height: 1;
			margin-bottom: 0.9rem;
		}

		.score-badge {
			background: #eaf1fe;
			color: #1f4fbf;
		}

		.status-low {
			background: var(--success-bg);
			color: var(--success);
		}

		.status-high {
			background: var(--danger-bg);
			color: var(--danger);
		}

		.badge-row {
			display: flex;
			gap: 0.55rem;
			flex-wrap: wrap;
			margin-top: 0.25rem;
			margin-bottom: 0.9rem;
		}

		.summary-strip {
			background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
			border: 1px solid var(--line);
			border-radius: 18px;
			padding: 1rem 1.1rem;
			margin-top: 1rem;
			box-shadow: 0 6px 16px rgba(15, 23, 42, 0.04);
		}

		.summary-label {
			font-size: 0.85rem;
			text-transform: uppercase;
			letter-spacing: 0.06em;
			color: var(--muted);
			font-weight: 700;
		}

		.summary-value {
			font-size: 1rem;
			font-weight: 600;
			color: var(--text);
			margin-top: 0.2rem;
			line-height: 1.55;
		}

		.stTextArea label {
			font-weight: 600 !important;
			color: var(--text) !important;
		}

		div[data-baseweb="textarea"] textarea {
			background: #ffffff !important;
			border: 1px solid #d7e0ed !important;
			border-radius: 16px !important;
			box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04) !important;
			padding: 0.95rem 1rem !important;
			color: var(--text) !important;
			font-family: 'Inter', sans-serif !important;
		}

		/* Force text area content to be visible and dark */
		div[data-baseweb="textarea"] textarea {
			color: #1e293b !important;
			-webkit-text-fill-color: #1e293b !important;
			opacity: 1 !important;
		}

		/* Ensure disabled text areas aren't washed out */
		div[data-baseweb="textarea"] .st-ae {
			color: #1e293b !important;
		}

		div[data-baseweb="textarea"] textarea:focus {
			border-color: rgba(66, 133, 244, 0.85) !important;
			box-shadow: 0 0 0 4px rgba(66, 133, 244, 0.14) !important;
		}

		.stButton > button {
			background: linear-gradient(135deg, #4285F4 0%, #5f97f5 100%);
			color: #ffffff;
			border: none;
			border-radius: 999px;
			padding: 0.8rem 1.2rem;
			font-weight: 700;
			box-shadow: 0 12px 26px rgba(66, 133, 244, 0.24);
			transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
		}

		.stButton > button:hover {
			transform: translateY(-1px);
			box-shadow: 0 16px 32px rgba(66, 133, 244, 0.3);
			filter: brightness(1.02);
		}

		.stButton > button:active {
			transform: translateY(0px);
		}
	</style>
	""",
	unsafe_allow_html=True,
)


def status_badge(text: str, variant: str) -> str:
	"""Return a simple HTML badge for the dashboard."""
	class_name = "status-low" if variant == "low" else "status-high"
	icon = "●"
	return f'<span class="status-badge {class_name}">{icon} {text}</span>'


def score_bucket(score: int) -> tuple[str, str]:
	"""Turn a score into a human-friendly status label."""
	if score >= 60:
		return "High Bias", "high"
	return "Low Risk", "low"


def score_summary(score: int) -> str:
	"""Make the raw score easier to read in the interface."""
	if score >= 60:
		return "The resume is triggering a stronger positive preference in the simulation."
	if score >= 35:
		return "The resume is in a neutral-to-moderate zone in this simulation."
	return "The resume is scoring low in this simulation."


# Hero section: short headline with a polished gradient background.
st.markdown(
	"""
	<div class="hero-shell">
		<div class="hero-kicker">HR Audit Dashboard</div>
		<div class="hero-title">🧭 Resume Fairness Review</div>
		<div class="hero-copy">
			A light-mode corporate dashboard for auditing résumé signals, comparing
			brand-heavy and anonymized versions, and presenting a clear mitigation view.
		</div>
	</div>
	""",
	unsafe_allow_html=True,
)


# Audit section groups the input and the first result view together.
with st.container():
	st.markdown(
		"""
		<div class="section-shell">
			<div class="section-title">📋 Audit</div>
			<div class="section-subtitle">Paste a résumé, run the review, and compare the scoring outcome.</div>
		</div>
		""",
		unsafe_allow_html=True,
	)

	resume_text = st.text_area(
		"Paste Resume Text",
		height=260,
		placeholder="Paste the full resume text here...",
	)

	col_left, col_right = st.columns([1, 1])
	with col_left:
		run_audit = st.button("Run Fairness Audit")

if run_audit:
	if not resume_text.strip():
		st.warning("Please paste resume text before running the audit.")
		st.stop()

	original_score = biased_hiring_ai(resume_text)

	try:
		# Brand-blind rewrite used for the audit comparison.
		mirrored_resume = generate_mirror_resume(resume_text)
		mirrored_score = biased_hiring_ai(mirrored_resume)

		# Clean, anonymized version used in the mitigation view.
		fair_version = generate_fair_version(resume_text)
		fair_score = biased_hiring_ai(fair_version)
	except Exception as exc:
		st.error(f"Could not complete the audit: {exc}")
		st.stop()

	bias_changed = original_score != mirrored_score
	status_text = "High Bias" if bias_changed else "Low Risk"
	status_variant = "high" if bias_changed else "low"

	# Main comparison cards: left is original, right is mirrored.
	left_col, right_col = st.columns(2)

	with left_col:
		st.markdown('<div class="audit-card">', unsafe_allow_html=True)
		st.markdown('<div class="card-title">🧾 Original Resume</div>', unsafe_allow_html=True)
		st.markdown('<div class="card-meta">The résumé as submitted by the candidate.</div>', unsafe_allow_html=True)
		badge_label, badge_variant = score_bucket(original_score)
		st.markdown(
			status_badge(badge_label, badge_variant) + f' <span class="score-badge">Score {original_score}/100</span>',
			unsafe_allow_html=True,
		)
		st.text_area("Original Resume", value=resume_text, height=280, disabled=True, label_visibility="collapsed")
		st.markdown('</div>', unsafe_allow_html=True)

	with right_col:
		st.markdown('<div class="audit-card">', unsafe_allow_html=True)
		st.markdown('<div class="card-title">🪞 Brand-Blind Mirror</div>', unsafe_allow_html=True)
		st.markdown('<div class="card-meta">The same résumé after brand and identity cues are normalized.</div>', unsafe_allow_html=True)
		badge_label, badge_variant = score_bucket(mirrored_score)
		st.markdown(
			status_badge(badge_label, badge_variant) + f' <span class="score-badge">Score {mirrored_score}/100</span>',
			unsafe_allow_html=True,
		)
		st.text_area("Mirrored Resume", value=mirrored_resume, height=280, disabled=True, label_visibility="collapsed")
		st.markdown('</div>', unsafe_allow_html=True)

	# Status summary bar gives a quick yes/no view of bias.
	st.markdown(
		f'''
		<div class="summary-strip">
			<div class="summary-label">Audit Status</div>
			<div class="badge-row">
				{status_badge(status_text, status_variant)}
				<span class="score-badge">Score Delta {abs(mirrored_score - original_score)}</span>
			</div>
			<div class="summary-value">
				{get_bias_explanation(original_score, mirrored_score)}
			</div>
		</div>
		''',
		unsafe_allow_html=True,
	)

	# Mitigation section is grouped in its own container so it reads like a second panel.
	with st.container():
		st.markdown(
			"""
			<div class="section-shell">
				<div class="section-title">🛠️ Mitigation</div>
				<div class="section-subtitle">A cleaner version of the résumé that removes brand and identity signals.</div>
			</div>
			""",
			unsafe_allow_html=True,
		)

		mitigation_left, mitigation_right = st.columns(2)

		with mitigation_left:
			st.markdown('<div class="audit-card">', unsafe_allow_html=True)
			st.markdown('<div class="card-title">🧼 Anonymized Resume</div>', unsafe_allow_html=True)
			st.markdown('<div class="card-meta">A neutral version with college branding removed.</div>', unsafe_allow_html=True)
			mitigation_label, mitigation_variant = score_bucket(fair_score)
			st.markdown(
				status_badge(mitigation_label, mitigation_variant) + f' <span class="score-badge">Score {fair_score}/100</span>',
				unsafe_allow_html=True,
			)
			st.text_area("Anonymized Resume", value=fair_version, height=280, disabled=True, label_visibility="collapsed")
			st.markdown('</div>', unsafe_allow_html=True)

		with mitigation_right:
			st.markdown('<div class="audit-card">', unsafe_allow_html=True)
			st.markdown('<div class="card-title">📊 Review Notes</div>', unsafe_allow_html=True)
			st.markdown('<div class="card-meta">High-level interpretation for stakeholders.</div>', unsafe_allow_html=True)
			st.markdown(
				status_badge("High Bias" if bias_changed else "Low Risk", "high" if bias_changed else "low") +
				f' <span class="score-badge">Original {original_score}/100</span>' +
				f' <span class="score-badge">Mirrored {mirrored_score}/100</span>',
				unsafe_allow_html=True,
			)
			st.markdown(
				f'<div class="summary-value">{score_summary(mirrored_score)}</div>',
				unsafe_allow_html=True,
			)
			st.markdown(
				f'<div class="summary-value">The mitigation view keeps the content professional while stripping out specific brand and identity cues.</div>',
				unsafe_allow_html=True,
			)
			st.markdown('</div>', unsafe_allow_html=True)

else:
	st.info("👋 Welcome! Paste a resume above and click 'Run Fairness Audit' to begin the diagnostic review.")
