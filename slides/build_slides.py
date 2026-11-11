"""Build the Cyclistic case study deck (16:9) from the figures in ../figures.

Usage: .venv/bin/python slides/build_slides.py  ->  slides/cyclistic_case_study.pptx
Speaker notes hold the talking points and assumptions for each slide.
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
OUT = ROOT / "slides" / "cyclistic_case_study.pptx"

INK = RGBColor(0x1E, 0x1B, 0x3A)
SOFT = RGBColor(0x56, 0x53, 0x74)
MEMBER = RGBColor(0x3F, 0x3D, 0x9C)
CASUAL = RGBColor(0xD6, 0x33, 0x6C)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def text(slide, x, y, w, h, lines, size=20, color=INK, bold=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines if isinstance(lines, list) else [lines]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = p.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        p.space_after = Pt(8)
    return box


def slide(title, notes="", kicker=None):
    s = prs.slides.add_slide(BLANK)
    bar = s.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CASUAL
    bar.line.fill.background()
    if kicker:
        text(s, 0.6, 0.35, 12, 0.4, kicker, size=14, color=SOFT)
    text(s, 0.6, 0.7 if kicker else 0.45, 12.1, 1.0, title, size=30, bold=True)
    text(s, 0.6, 7.0, 12, 0.4, "Data: Divvy trip data, Nov 2025 – Oct 2026 (Motivate International Inc.). 6.13M cleaned rides.", size=10, color=SOFT)
    s.notes_slide.notes_text_frame.text = notes
    return s


def figure(s, name, x=0.6, y=1.8, w=12.1):
    path = FIG / name
    pic = s.shapes.add_picture(str(path), Inches(x), Inches(y), width=Inches(w))
    max_h = Inches(5.0)
    if pic.height > max_h:  # keep the chart inside the slide
        ratio = max_h / pic.height
        pic.height = max_h
        pic.width = Emu(int(pic.width * ratio))
        pic.left = int((prs.slide_width - pic.width) / 2)
    return pic


# 1. Title
s = prs.slides.add_slide(BLANK)
text(s, 0.8, 2.2, 11.5, 1.4, "How do casual riders and annual members use Cyclistic differently?", size=40, bold=True)
text(s, 0.8, 4.0, 11.5, 1.0, "A year of bike-share data, and three ways to grow memberships", size=22, color=SOFT)
text(s, 0.8, 6.3, 11.5, 0.5, "Google Data Analytics Capstone · Case Study 1", size=14, color=SOFT)
s.notes_slide.notes_text_frame.text = "Introduce yourself and the question from Lily Moreno."

# 2. Business task
s = slide("The question we were asked", kicker="Ask",
          notes="Finance found annual members are much more profitable, so marketing wants to convert casual riders. My part is question 1.")
text(s, 0.6, 1.9, 12, 4.5, [
    "Business task: understand how annual members and casual riders use Cyclistic bikes differently, to design a campaign that converts casual riders into members.",
    "Stakeholders: Lily Moreno (director of marketing), marketing analytics team, executive team.",
    "Metrics: share of rides, ride length (median), weekday vs weekend, time of day, seasonality, stations, round trips.",
], size=22)

# 3. Data
s = slide("Data: 6.29M trips over 12 months, 6.13M after cleaning", kicker="Prepare & Process",
          notes="Public Divvy data under the Divvy Data License Agreement. No rider IDs, so everything is about rides, not people.")
text(s, 0.6, 1.9, 6.2, 4.8, [
    "Source: Divvy trip data (Motivate International Inc.), Nov 2025 – Oct 2026, 12 monthly CSV files.",
    "Cleaning in SQL (DuckDB): removed 35 duplicates, 159k rides under 1 minute, 5k over 24 hours, 13 test-station rides and 108 rides outside the window (2.6% in total).",
    "Added ride length, day of week, hour, month and round-trip flag.",
], size=19)
text(s, 7.2, 1.9, 5.5, 4.8, [
    "Limitations",
    "• No rider IDs: rides, not people",
    "• No prices or revenue",
    "• 19.8% of rides have no station name (mostly e-bikes)",
], size=19, color=SOFT)

# 4–9. Findings
findings = [
    ("01_overview.png", "Casual riders take 1 in 3 rides, and their rides last 28% longer",
     "35.3% of rides. Median 11.1 vs 8.7 minutes; 13.2% of casual rides are over 30 minutes vs 5.4% for members. Medians, because ride length is heavily right-skewed."),
    ("02_rides_by_day.png", "Casual riding jumps on weekends",
     "37.6% of casual rides fall on Saturday or Sunday (Saturday alone 21.5%) vs 23.7% for members, whose rides are spread evenly across weekdays."),
    ("03_rides_by_hour.png", "Members commute; casual riding spreads across the day",
     "Both groups peak at 17:00 on weekdays, but members also peak at 07:00–08:59 (15.2% of their weekday rides vs 7.7%). On weekends both curves look alike."),
    ("04_rides_by_month.png", "Casual demand swings about 14× between winter and summer",
     "Peak month / quietest month: 14.5× for casual, 4.7× for members. Casual share goes from 17.9% in January to 40.8% in July; 69% of casual rides happen May–September."),
    ("05_ride_length.png", "Casual rides are longer at every percentile",
     "90th percentile 35.4 vs 23.4 minutes. Box plot on a log scale from a 200,000-ride random sample; outliers hidden."),
    ("06_top_casual_stations.png", "The lakefront and museums are casual territory",
     "Casual riders make 76–82% of rides at Navy Pier, Shedd Aquarium, Field Museum and DuSable Lake Shore Dr & Monroe St. Round trips: 7.4% of casual rides vs 2.2% (rides with known stations)."),
]
for i, (fig_name, title, note) in enumerate(findings, start=1):
    s = slide(title, notes=note, kicker=f"Finding {i}")
    figure(s, fig_name)

# 10. Commuter-like casual riders
s = slide("A quarter of casual rides already look like commutes", kicker="Finding 7",
          notes="Weekday rides at 07:00–09:59 or 16:00–18:59. About 540k casual rides. These riders are the easiest to convert.")
text(s, 0.6, 2.2, 12, 3.5, [
    "25.1% of casual rides (≈540,000) happen on weekdays at commute hours.",
    "Members: 38.5%. These casual riders already behave like members, but pay per ride.",
], size=26)

# 11. Recommendations
s = slide("Three ways to turn casual riders into members", kicker="Act",
          notes="Each recommendation is tied to findings. Pricing for the savings messages must come from finance.")
text(s, 0.6, 1.9, 12, 5, [
    "1. Summer weekend membership: a seasonal or weekend plan promoted May–September, upgradable to annual (findings 1, 3, 5).",
    "2. Lakefront campaign in peak season: geo-targeted ads, in-app messages and dock QR codes at Navy Pier, Shedd Aquarium, Field Museum, Millennium Park, DuSable Lake Shore Dr; weekends 12:00–18:00 (finding 6).",
    "3. Convert commuter-like casual riders: \"you already ride like a member\" with a savings calculator for weekday commute-hour riders (findings 2, 4, 7).",
], size=21)

# 12. Next steps
s = slide("Next steps", kicker="Further work",
          notes="Ask for anonymised account data to measure conversion; A/B test the offers.")
text(s, 0.6, 1.9, 12, 5, [
    "Join anonymised account data to count riders and measure conversion.",
    "Get current prices to quantify savings in the campaign messages.",
    "Add weather and event data to separate tourism from regular use.",
    "A/B test the three offers in summer 2027 and track membership sign-ups.",
], size=22)

OUT.parent.mkdir(exist_ok=True)
prs.save(OUT)
print(f"saved {OUT} ({len(prs.slides)} slides)")
