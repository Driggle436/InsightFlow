from components.html_render import render_html


def render_hero(title, subtitle, badge="KPI Intelligence-to-Action Engine"):
  render_html(
    f'<div class="if-hero">'
    f'<div class="if-hero-badge">{badge}</div>'
    f"<h1>{title}</h1>"
    f"<p>{subtitle}</p>"
    f"</div>"
  )


def render_section_header(title, subtitle=""):
  sub = f"<span>{subtitle}</span>" if subtitle else ""
  render_html(
    f'<div class="if-section-header"><h2>{title}</h2>{sub}</div>'
  )
