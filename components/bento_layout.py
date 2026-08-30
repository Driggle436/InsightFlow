from components.html_render import render_html


def render_bento_shell():
  render_html(
    '<div class="if-scene">'
    '<div class="if-scene-orb if-scene-orb-1"></div>'
    '<div class="if-scene-orb if-scene-orb-2"></div>'
    '<div class="if-scene-orb if-scene-orb-3"></div>'
    "</div>"
  )


def render_panel(title, subtitle="", panel_class="if-panel", body_html=""):
  sub = f'<p class="if-panel-sub">{subtitle}</p>' if subtitle else ""
  render_html(
    f'<div class="{panel_class}">'
    f'<div class="if-panel-head"><h3>{title}</h3>{sub}</div>'
    f'<div class="if-panel-body">{body_html}</div>'
    f"</div>"
  )


def render_stat_tile(label, value, delta="", tone="neutral", badge=""):
  badge_html = f'<span class="if-tile-badge">{badge}</span>' if badge else ""
  render_html(
    f'<div class="if-stat-tile if-stat-{tone}">'
    f'<div class="if-stat-top"><span class="if-stat-label">{label}</span>{badge_html}</div>'
    f'<div class="if-stat-value">{value}</div>'
    f'<div class="if-stat-delta">{delta}</div>'
    f"</div>"
  )
