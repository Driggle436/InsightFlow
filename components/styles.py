import streamlit as st

GLOBAL_CSS = """
:root {
    --if-primary: #60A5FA;
    --if-primary-light: #93C5FD;
    --if-accent: #F59E0B;
    --if-bg: #0B1120;
    --if-card: rgba(21, 30, 50, 0.85);
    --if-border: rgba(96, 165, 250, 0.18);
    --if-text: #E2E8F0;
    --if-muted: #94A3B8;
    --if-success: #34D399;
    --if-warning: #FBBF24;
    --if-danger: #F87171;
    --if-info: #38BDF8;
    --if-shadow-sm: 0 2px 12px rgba(0, 0, 0, 0.35);
    --if-shadow-md: 0 8px 28px rgba(0, 0, 0, 0.45), 0 2px 8px rgba(0, 0, 0, 0.25);
    --if-shadow-lg: 0 20px 50px rgba(0, 0, 0, 0.55), 0 8px 20px rgba(0, 0, 0, 0.3);
    --if-shadow-float: 0 24px 60px rgba(37, 99, 235, 0.25), 0 12px 28px rgba(0, 0, 0, 0.4);
}

html, body, [class*="css"] {
    font-family: 'Fira Sans', sans-serif;
    color: var(--if-text);
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(37, 99, 235, 0.22), transparent 55%),
        radial-gradient(ellipse 60% 40% at 90% 10%, rgba(245, 158, 11, 0.08), transparent 50%),
        linear-gradient(180deg, #0B1120 0%, #0F172A 50%, #0B1120 100%) !important;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2.5rem;
    max-width: 1320px;
}

header[data-testid="stHeader"] { background: transparent; }

/* Hide Streamlit's built-in multipage nav only — keep custom sidebar widgets */
[data-testid="stSidebarNav"] {
    display: none !important;
}

.if-scene { position: relative; height: 0; }
.if-scene-orb {
    position: fixed; border-radius: 50%; filter: blur(70px);
    opacity: 0.22; pointer-events: none; z-index: 0;
}
.if-scene-orb-1 { width: 340px; height: 340px; background: #2563EB; top: -100px; right: 6%; }
.if-scene-orb-2 { width: 260px; height: 260px; background: #D97706; bottom: 8%; left: -50px; }
.if-scene-orb-3 { width: 200px; height: 200px; background: #7C3AED; top: 38%; right: -40px; }

.if-hero {
    background: linear-gradient(135deg, rgba(30, 58, 138, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
    border-radius: 20px; padding: 32px 36px; margin-bottom: 28px;
    color: #F1F5F9; position: relative; overflow: hidden;
    box-shadow: var(--if-shadow-lg);
    border: 1px solid rgba(96, 165, 250, 0.25);
}
.if-hero::before {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(120deg, rgba(96,165,250,0.12) 0%, transparent 45%);
    pointer-events: none;
}
.if-hero h1 { font-size: 1.85rem; font-weight: 700; margin: 0 0 8px 0; position: relative; }
.if-hero p { font-size: 0.95rem; opacity: 0.88; margin: 0; max-width: 560px; position: relative; }
.if-hero-badge {
    display: inline-block; background: rgba(96,165,250,0.15);
    border: 1px solid rgba(96,165,250,0.3); border-radius: 20px;
    padding: 5px 14px; font-size: 0.72rem; font-weight: 600;
    margin-bottom: 14px; position: relative;
}

.if-panel {
    background: var(--if-card); backdrop-filter: blur(16px);
    border: 1px solid var(--if-border); border-radius: 18px;
    padding: 22px 24px; margin-bottom: 18px;
    box-shadow: var(--if-shadow-md);
}

.if-kpi-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 18px; margin-bottom: 12px;
}
.if-kpi-card {
    background: linear-gradient(145deg, rgba(30,41,59,0.95) 0%, rgba(21,30,50,0.9) 100%);
    border: 1px solid rgba(96,165,250,0.15); border-radius: 16px;
    padding: 20px 22px; box-shadow: var(--if-shadow-md);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.if-kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--if-shadow-float);
    border-color: rgba(96,165,250,0.35);
}
.if-kpi-card.material {
    border-top: 3px solid var(--if-accent);
    background: linear-gradient(160deg, rgba(30,41,59,0.98) 0%, rgba(120,53,15,0.15) 100%);
}
.if-kpi-card.sparse { border-top: 3px solid var(--if-info); }
.if-kpi-label {
    font-size: 0.72rem; font-weight: 600; color: var(--if-muted);
    text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;
}
.if-kpi-value {
    font-family: 'Fira Code', monospace; font-size: 1.55rem;
    font-weight: 700; color: #F8FAFC; line-height: 1.1;
}
.if-kpi-delta { font-size: 0.82rem; font-weight: 700; margin-top: 8px; }
.if-kpi-delta.up { color: var(--if-success); }
.if-kpi-delta.down { color: var(--if-danger); }
.if-kpi-delta.flat { color: var(--if-muted); }
.if-kpi-meta { font-size: 0.72rem; color: var(--if-muted); margin-top: 10px; }

.if-badge {
    display: inline-block; padding: 4px 10px; border-radius: 8px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.03em; text-transform: uppercase;
}
.if-badge-p1 { background: rgba(248,113,113,0.2); color: #FCA5A5; }
.if-badge-p2 { background: rgba(251,191,36,0.2); color: #FCD34D; }
.if-badge-p3 { background: rgba(96,165,250,0.2); color: #93C5FD; }
.if-badge-high { background: rgba(52,211,153,0.2); color: #6EE7B7; }
.if-badge-medium { background: rgba(251,191,36,0.2); color: #FCD34D; }
.if-badge-low { background: rgba(248,113,113,0.2); color: #FCA5A5; }
.if-badge-secure { background: rgba(96,165,250,0.2); color: #93C5FD; }
.if-badge-llm { background: rgba(167,139,250,0.2); color: #C4B5FD; }
.if-badge-sql { background: rgba(52,211,153,0.15); color: #6EE7B7; }
.if-badge-ml { background: rgba(129,140,248,0.2); color: #A5B4FC; }
.if-badge-stats { background: rgba(251,191,36,0.15); color: #FCD34D; }
.if-badge-rules { background: rgba(148,163,184,0.15); color: #CBD5E1; }
.if-badge-fresh { background: rgba(52,211,153,0.15); color: #6EE7B7; }
.if-badge-stale { background: rgba(248,113,113,0.15); color: #FCA5A5; }

.if-alert-strip { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 22px; }
.if-alert-item {
    flex: 1; min-width: 220px;
    background: rgba(21,30,50,0.9); border: 1px solid var(--if-border);
    border-radius: 14px; padding: 14px 18px; font-size: 0.85rem;
    display: flex; align-items: flex-start; gap: 12px;
    box-shadow: var(--if-shadow-sm);
}
.if-alert-item.critical { border-left: 4px solid var(--if-danger); }
.if-alert-item.warning { border-left: 4px solid var(--if-warning); }
.if-alert-item.info { border-left: 4px solid var(--if-info); }
.if-alert-dot { width: 9px; height: 9px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.if-alert-dot.critical { background: var(--if-danger); box-shadow: 0 0 8px rgba(248,113,113,0.6); }
.if-alert-dot.warning { background: var(--if-warning); }
.if-alert-dot.info { background: var(--if-info); }

.if-section-header {
    display: flex; align-items: center; justify-content: space-between;
    margin: 24px 0 16px 0; padding-bottom: 10px;
    border-bottom: 1px solid var(--if-border);
}
.if-section-header h2 { font-size: 1.2rem; font-weight: 700; margin: 0; color: var(--if-text); }
.if-section-header span { font-size: 0.78rem; color: var(--if-muted); }

.if-action-card {
    background: rgba(21,30,50,0.92); border: 1px solid var(--if-border);
    border-radius: 16px; padding: 20px 22px; margin-bottom: 14px;
    box-shadow: var(--if-shadow-md);
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}
.if-action-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--if-shadow-lg);
    border-color: rgba(96,165,250,0.3);
}
.if-action-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; }
.if-action-title { font-size: 1rem; font-weight: 700; color: var(--if-text); }
.if-action-chain {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px; margin: 14px 0;
}
.if-action-step {
    background: rgba(15,23,42,0.8); border-radius: 10px; padding: 12px 14px;
    font-size: 0.78rem; border: 1px solid rgba(96,165,250,0.1);
}
.if-action-step-label {
    font-weight: 700; color: var(--if-muted); font-size: 0.65rem;
    text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 5px;
}
.if-action-step-value { color: var(--if-text); font-weight: 600; }

.if-evidence-row {
    display: flex; align-items: center; padding: 12px 16px;
    border-bottom: 1px solid rgba(96,165,250,0.08); font-size: 0.85rem;
}
.if-evidence-source { font-weight: 700; min-width: 100px; color: var(--if-primary); }
.if-evidence-detail { flex: 1; color: var(--if-muted); }

.if-insight-card {
    background: linear-gradient(135deg, rgba(30,58,138,0.4) 0%, rgba(21,30,50,0.95) 100%);
    border: 1px solid rgba(96,165,250,0.25); border-radius: 16px;
    padding: 22px 26px; margin-bottom: 12px;
    box-shadow: var(--if-shadow-md); font-size: 0.92rem; line-height: 1.75; color: var(--if-text);
}

.if-abstain-banner {
    background: linear-gradient(135deg, rgba(120,53,15,0.5) 0%, rgba(21,30,50,0.9) 100%);
    border: 1px solid rgba(245,158,11,0.4); border-radius: 16px;
    padding: 20px 24px; margin: 16px 0;
}
.if-abstain-banner h3 { color: #FCD34D; font-size: 1rem; margin: 0 0 6px 0; }
.if-abstain-banner p { color: #FDE68A; font-size: 0.85rem; margin: 0; }
.if-abstain-banner li { color: #FDE68A; }

.if-contract-card {
    background: rgba(21,30,50,0.85); border: 1px solid var(--if-border);
    border-radius: 12px; padding: 16px; margin-bottom: 10px;
}
.if-contract-name { font-weight: 600; font-size: 0.95rem; margin-bottom: 8px; color: var(--if-text); }
.if-contract-detail { font-size: 0.8rem; color: var(--if-muted); line-height: 1.6; }

.if-pipeline { display: flex; gap: 0; margin: 16px 0; overflow-x: auto; }
.if-pipeline-step {
    flex: 1; min-width: 120px; text-align: center; padding: 14px 10px;
    background: rgba(21,30,50,0.9); border: 1px solid var(--if-border); color: var(--if-text);
}
.if-pipeline-step.llm { background: rgba(91,33,182,0.25); }

.if-telemetry-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }
.if-telemetry-card {
    background: rgba(21,30,50,0.9); border: 1px solid var(--if-border);
    border-radius: 12px; padding: 16px; text-align: center;
}
.if-telemetry-value { font-family: 'Fira Code', monospace; font-size: 1.2rem; font-weight: 700; color: var(--if-primary); }
.if-telemetry-label { font-size: 0.7rem; color: var(--if-muted); margin-top: 4px; text-transform: uppercase; }

section[data-testid="stSidebar"] {
    background: rgba(11,17,32,0.95) !important;
    border-right: 1px solid var(--if-border);
}

/* Sidebar nav links */
section[data-testid="stSidebar"] a {
    border-radius: 8px;
}

footer { visibility: hidden; }

@media (prefers-reduced-motion: reduce) {
    .if-kpi-card, .if-action-card { transition: none; }
}
"""


def inject_global_styles():
  st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Fira+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
  )
  st.html(f"<style>{GLOBAL_CSS}</style>")
