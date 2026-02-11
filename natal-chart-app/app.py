"""
Natal Chart Web App - Batteries Included for Normies
Beautiful Gradio interface wrapping the natal chart skill
"""

import gradio as gr
from natal_backend import NatalChartGenerator, get_timezone_suggestions
from datetime import datetime
import json


# Initialize backend
generator = NatalChartGenerator()


def generate_natal_chart(
    name: str,
    birth_date: str,  # YYYY-MM-DD format from Gradio date picker
    birth_hour: int,
    birth_minute: int,
    city: str,
    latitude: float,
    longitude: float,
    timezone: str
) -> tuple:
    """
    Main function called by Gradio interface
    Returns: (interpretation_text, chart_image, detailed_json)
    """
    
    # Validate inputs
    if not name or not birth_date:
        return "❌ Please provide your name and birth date.", None, "Missing required fields"
    
    try:
        # Parse date
        year, month, day = map(int, birth_date.split('-'))
        
        # Generate chart
        result = generator.generate_chart(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=birth_hour,
            minute=birth_minute,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            city=city
        )
        
        if not result.get("success"):
            error_msg = result.get("error", "Unknown error")
            return f"❌ Error: {error_msg}", None, json.dumps(result, indent=2)
        
        # Format interpretation for display
        interpretation = format_interpretation(result)
        
        # Get chart SVG path
        chart_path = result.get("chart_svg")
        
        # Format detailed data
        detailed_data = format_detailed_data(result)
        
        return interpretation, chart_path, detailed_data
        
    except Exception as e:
        return f"❌ Error: {str(e)}", None, str(e)


def format_interpretation(result: dict) -> str:
    """Format the interpretation text for beautiful display"""
    
    interp = result["interpretation"]
    placements = result["placements"]
    
    # Build beautiful text output
    text = f"""
# 🌟 Natal Chart for {result['name']}

## Birth Information
📅 **Date**: {result['birth_data']['date']}  
🕐 **Time**: {result['birth_data']['time']}  
📍 **Location**: {result['birth_data']['location']}  
🌍 **Timezone**: {result['birth_data']['timezone']}

---

## ✨ Your Core Identity (Big Three)

{interp['sun']}

{interp['moon']}

{interp['rising']}

---

## 🪐 Planetary Placements

"""
    
    # Add planet placements
    for planet, data in placements.items():
        retrograde = " ℞" if data['retrograde'] else ""
        text += f"**{planet}**: {data['sign']} at {data['position']}° (House {data['house']}){retrograde}\n\n"
    
    # Add aspects if available
    aspects = result.get("aspects", [])
    if aspects:
        text += "\n---\n\n## 🔗 Major Aspects\n\n"
        for aspect in aspects[:5]:  # Top 5
            text += f"- {aspect['planets']}: {aspect['type']} (orb {aspect['orb']}°)\n"
    
    return text


def format_detailed_data(result: dict) -> str:
    """Format detailed JSON data for the accordion"""
    return json.dumps(result, indent=2)


# Common city coordinates helper
COMMON_CITIES = {
    "New York, USA": (40.7128, -74.0060, "America/New_York"),
    "Los Angeles, USA": (34.0522, -118.2437, "America/Los_Angeles"),
    "London, UK": (51.5074, -0.1278, "Europe/London"),
    "Paris, France": (48.8566, 2.3522, "Europe/Paris"),
    "Tokyo, Japan": (35.6762, 139.6503, "Asia/Tokyo"),
    "Sydney, Australia": (-33.8688, 151.2093, "Australia/Sydney"),
    "Berlin, Germany": (52.5200, 13.4050, "Europe/Berlin"),
    "Rome, Italy": (41.9028, 12.4964, "Europe/Rome"),
    "Madrid, Spain": (40.4168, -3.7038, "Europe/Madrid"),
    "Lisbon, Portugal": (38.7223, -9.1393, "Europe/Lisbon"),
    "Dubai, UAE": (25.2048, 55.2708, "Asia/Dubai"),
    "Singapore": (1.3521, 103.8198, "Asia/Singapore"),
    "Hong Kong": (22.3193, 114.1694, "Asia/Hong_Kong"),
    "Mumbai, India": (19.0760, 72.8777, "Asia/Kolkata"),
    "São Paulo, Brazil": (-23.5505, -46.6333, "America/Sao_Paulo"),
}


def fill_city_coords(city_selection):
    """Auto-fill coordinates when user selects a city"""
    if city_selection in COMMON_CITIES:
        lat, lng, tz = COMMON_CITIES[city_selection]
        return lat, lng, tz, city_selection
    return 0.0, 0.0, "UTC", ""


# Build Gradio Interface
with gr.Blocks(theme=gr.themes.Soft(), title="Natal Chart Generator") as app:
    
    gr.Markdown("""
    # 🌙 Natal Chart Generator
    
    Generate your complete astrological birth chart with beautiful visualizations and interpretations.
    
    **What you'll get:**
    - Your Sun, Moon, and Rising signs explained
    - All planetary placements
    - House positions
    - Major aspects between planets
    - Beautiful chart visualization
    
    ---
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Your Birth Information")
            
            name_input = gr.Textbox(
                label="Full Name",
                placeholder="Jane Doe",
                info="Your name for the chart"
            )
            
            birth_date_input = gr.Textbox(
                label="Birth Date",
                placeholder="1990-03-15",
                info="Format: YYYY-MM-DD"
            )
            
            with gr.Row():
                birth_hour = gr.Slider(
                    minimum=0,
                    maximum=23,
                    value=12,
                    step=1,
                    label="Birth Hour (24h format)"
                )
                birth_minute = gr.Slider(
                    minimum=0,
                    maximum=59,
                    value=0,
                    step=1,
                    label="Birth Minute"
                )
            
            gr.Markdown("### 📍 Birth Location")
            
            city_dropdown = gr.Dropdown(
                choices=["Custom Location"] + list(COMMON_CITIES.keys()),
                label="Select City (or choose Custom)",
                value="Custom Location",
                info="Quick select for common cities"
            )
            
            city_input = gr.Textbox(
                label="City Name (optional)",
                placeholder="New York",
                info="For display purposes"
            )
            
            latitude = gr.Number(
                label="Latitude",
                value=40.7128,
                info="North is positive, South is negative"
            )
            
            longitude = gr.Number(
                label="Longitude",
                value=-74.0060,
                info="East is positive, West is negative"
            )
            
            timezone = gr.Dropdown(
                choices=get_timezone_suggestions(),
                label="Timezone",
                value="America/New_York",
                info="Select your birth location timezone"
            )
            
            # Auto-fill coordinates when city selected
            city_dropdown.change(
                fn=fill_city_coords,
                inputs=[city_dropdown],
                outputs=[latitude, longitude, timezone, city_input]
            )
            
            generate_btn = gr.Button("✨ Generate My Chart", variant="primary", size="lg")
        
        with gr.Column(scale=2):
            gr.Markdown("### 🌟 Your Natal Chart")
            
            interpretation_output = gr.Markdown(
                value="Your chart interpretation will appear here...",
                label="Interpretation"
            )
            
            chart_output = gr.Image(
                label="Birth Chart Visualization",
                type="filepath"
            )
            
            with gr.Accordion("📊 Detailed Data (JSON)", open=False):
                detailed_output = gr.Code(
                    label="Complete Chart Data",
                    language="json"
                )
    
    # Wire up the generate button
    generate_btn.click(
        fn=generate_natal_chart,
        inputs=[
            name_input,
            birth_date_input,
            birth_hour,
            birth_minute,
            city_input,
            latitude,
            longitude,
            timezone
        ],
        outputs=[
            interpretation_output,
            chart_output,
            detailed_output
        ]
    )
    
    gr.Markdown("""
    ---
    
    ### 💡 Tips for Accurate Charts
    
    1. **Birth Time**: The more precise, the better. Your Rising sign and house placements depend on exact birth time.
    2. **Location**: Use the city dropdown for quick selection, or enter custom coordinates for precise locations.
    3. **Timezone**: Make sure to select the timezone that was in effect at your birth (consider daylight saving time).
    
    ### ℹ️ About This App
    
    This app uses **Kerykeion** with Swiss Ephemeris for astronomical accuracy. All calculations are performed locally with no data stored or shared.
    
    Built with ❤️ using the TÂCHES methodology.
    """)


# Launch the app
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=False,  # Set to True for public Gradio link
        show_error=True
    )
