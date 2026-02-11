# 🌙 Natal Chart Web App

**Batteries-included natal chart generator for normies.**

A beautiful, user-friendly web application that generates accurate astrological birth charts with interpretations. No technical knowledge required - just enter your birth data and get instant insights.

## ✨ Features

- 🎨 **Beautiful Web Interface**: Simple Gradio UI that anyone can use
- 🎯 **Accurate Calculations**: Swiss Ephemeris via Kerykeion library
- 📊 **Visual Chart**: SVG birth chart diagram
- 💬 **Plain Language**: Interpretations written for normies, not astrologers
- 🌍 **Global Support**: 20+ pre-configured cities, custom coordinates for anywhere
- ⚡ **Instant Results**: Generate complete chart in seconds

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
python app.py
```

### 3. Open in Browser

The app will launch at: `http://localhost:7860`

## 📖 How to Use

1. **Enter Your Birth Information**
   - Full name
   - Birth date (YYYY-MM-DD format)
   - Birth time (hour and minute - 24h format)

2. **Select Your Birth Location**
   - Choose from 20+ pre-configured cities, OR
   - Enter custom coordinates (latitude/longitude)
   - Select appropriate timezone

3. **Generate Chart**
   - Click "Generate My Chart"
   - View your interpretation and chart visualization
   - Expand "Detailed Data" to see complete JSON

## 🎯 What You'll Get

### The Big Three
- **Sun Sign**: Your core identity and ego
- **Moon Sign**: Your emotional nature and needs
- **Rising Sign**: How others perceive you

### Complete Planetary Placements
All 10 planets with:
- Zodiac sign
- Exact degree position
- House placement
- Retrograde status

### Major Aspects
The most significant planetary relationships in your chart with precise orbs.

### Visual Chart
Beautiful SVG diagram showing your complete birth chart.

## 🛠️ Technical Details

**Backend**: `natal_backend.py`
- Clean API wrapper around Kerykeion skill
- Planetary calculations via Swiss Ephemeris
- JSON serialization for all chart data
- Human-readable interpretations

**Frontend**: `app.py`
- Gradio interface (batteries included)
- Auto-fill coordinates for common cities
- Timezone suggestions
- Markdown-formatted output

**Skill Foundation**: Built using the TÂCHES methodology
- Battle-tested with real birth data
- Error handling for common issues
- Comprehensive documentation

## 📦 Deployment Options

### Local Development
```bash
python app.py
```

### Public Share (Gradio)
Edit `app.py` line 290:
```python
app.launch(share=True)  # Generates public Gradio link
```

### Hugging Face Spaces
1. Create a new Space on Hugging Face
2. Upload these files:
   - `app.py`
   - `natal_backend.py`
   - `requirements.txt`
3. Space will auto-deploy

### Docker (Coming Soon)
Dockerfile will be added for containerized deployment.

## 🎓 Understanding Your Chart

### Birth Time Accuracy
- **Critical**: Rising sign and house positions require exact birth time
- **Acceptable**: If unknown, use noon (12:00) for planetary positions only
- **Note**: Charts without birth time won't show accurate houses or rising sign

### Timezone Considerations
- Use the timezone that was in effect at birth
- Account for daylight saving time if applicable
- When in doubt, check historical timezone records

### Interpreting Placements
- **Planets**: What areas of life
- **Signs**: How those energies express
- **Houses**: Where in your life
- **Aspects**: How planets interact

## 🔧 Troubleshooting

**"Missing data from geonames" error**
- Solution: Always use explicit coordinates (lat/lng/timezone)
- The app defaults to coordinates, avoiding this issue

**SVG chart not displaying**
- Check that `output/` directory exists
- Ensure write permissions
- Try regenerating the chart

**Incorrect timezone**
- Verify timezone was correct at birth date (historical changes)
- Use standard timezone names (e.g., "America/New_York")

## 📚 Additional Resources

- **Kerykeion Documentation**: https://github.com/g-battaglia/kerykeion
- **Timezone Database**: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
- **Swiss Ephemeris**: https://www.astro.com/swisseph/

## 🤝 Contributing

Built following the TÂCHES methodology:
1. Research best libraries
2. Expect and document failures
3. Test with real data
4. Heal the skill with learnings

See `../natal-chart-skill/SKILL.md` for the foundational skill documentation.

## 📄 License

Free to use and modify. Built with ❤️ for the normies.

## 🙏 Credits

- **Kerykeion**: Giacomo Battaglia (@g-battaglia)
- **Swiss Ephemeris**: Astrodienst AG
- **Gradio**: Hugging Face team
- **Methodology**: TÂCHES framework

---

**Ready to explore the stars?** Run `python app.py` and discover your cosmic blueprint! 🌟
