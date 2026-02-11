"""
Natal Chart Backend Service
Wraps the Kerykeion skill with clean API for the Gradio frontend
"""

from kerykeion import AstrologicalSubject, KerykeionChartSVG, NatalAspects
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path


class NatalChartGenerator:
    """Clean API wrapper for natal chart generation"""
    
    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_chart(
        self,
        name: str,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        latitude: float,
        longitude: float,
        timezone: str,
        city: Optional[str] = None
    ) -> Dict:
        """
        Generate complete natal chart with interpretations
        
        Returns:
            Dict with keys: subject_data, chart_svg_path, interpretation, aspects
        """
        try:
            # Create astrological subject
            subject = AstrologicalSubject(
                name=name,
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                lat=latitude,
                lng=longitude,
                tz_str=timezone
            )
            
            # Generate SVG chart
            chart = KerykeionChartSVG(subject)
            svg_path = self.output_dir / f"{name.replace(' ', '_')}_chart.svg"
            chart.makeSVG()
            
            # Get aspects
            aspects = NatalAspects(subject)
            
            # Extract key data
            chart_data = {
                "success": True,
                "name": name,
                "birth_data": {
                    "date": f"{year}-{month:02d}-{day:02d}",
                    "time": f"{hour:02d}:{minute:02d}",
                    "location": city or f"{latitude}, {longitude}",
                    "timezone": timezone
                },
                "placements": self._get_placements(subject),
                "houses": self._get_houses(subject),
                "aspects": self._get_aspects(aspects),
                "chart_svg": str(svg_path),
                "interpretation": self._generate_interpretation(subject)
            }
            
            return chart_data
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate natal chart. Please check your input data."
            }
    
    def _get_placements(self, subject: AstrologicalSubject) -> Dict[str, Dict]:
        """Extract planetary placements"""
        planets = {
            "Sun": subject.sun,
            "Moon": subject.moon,
            "Mercury": subject.mercury,
            "Venus": subject.venus,
            "Mars": subject.mars,
            "Jupiter": subject.jupiter,
            "Saturn": subject.saturn,
            "Uranus": subject.uranus,
            "Neptune": subject.neptune,
            "Pluto": subject.pluto
        }
        
        placements = {}
        for name, planet in planets.items():
            placements[name] = {
                "sign": planet.sign,
                "position": round(planet.position, 2),
                "house": planet.house,
                "retrograde": planet.retrograde
            }
        
        return placements
    
    def _get_houses(self, subject: AstrologicalSubject) -> Dict[str, str]:
        """Extract house cusps"""
        houses = {}
        for i in range(1, 13):
            house = getattr(subject, f"{'first' if i == 1 else 'second' if i == 2 else 'third' if i == 3 else ['fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth'][i-4]}_house")
            houses[f"House {i}"] = house.sign
        
        return houses
    
    def _get_aspects(self, aspects: NatalAspects) -> List[Dict]:
        """Extract major aspects"""
        aspect_list = []
        
        if hasattr(aspects, 'all_aspects'):
            for aspect in aspects.all_aspects:
                aspect_list.append({
                    "planets": f"{aspect['p1_name']} - {aspect['p2_name']}",
                    "type": aspect['aspect'],
                    "orb": round(aspect['orbit'], 2)
                })
        
        return aspect_list[:10]  # Top 10 aspects
    
    def _generate_interpretation(self, subject: AstrologicalSubject) -> Dict[str, str]:
        """
        Generate human-readable interpretations for normies
        Using basic astrology meanings
        """
        
        # Sun sign interpretation
        sun_sign = subject.sun.sign
        sun_interpretations = {
            "Aries": "Bold, energetic, and pioneering. You lead with courage and initiative.",
            "Taurus": "Grounded, reliable, and sensual. You value stability and comfort.",
            "Gemini": "Curious, adaptable, and communicative. You thrive on variety and mental stimulation.",
            "Cancer": "Nurturing, intuitive, and protective. You lead with emotion and care deeply.",
            "Leo": "Confident, creative, and charismatic. You shine brightest when expressing yourself.",
            "Virgo": "Analytical, practical, and helpful. You excel at refining and improving.",
            "Libra": "Diplomatic, harmonious, and fair. You seek balance and beauty in all things.",
            "Scorpio": "Intense, passionate, and transformative. You dive deep into life's mysteries.",
            "Sagittarius": "Adventurous, optimistic, and philosophical. You seek meaning and expansion.",
            "Capricorn": "Ambitious, disciplined, and responsible. You build lasting structures.",
            "Aquarius": "Innovative, independent, and humanitarian. You envision the future.",
            "Pisces": "Compassionate, imaginative, and spiritual. You feel deeply and dream big."
        }
        
        # Moon sign interpretation
        moon_sign = subject.moon.sign
        moon_interpretations = {
            "Aries": "Your emotions are direct and passionate. You need independence.",
            "Taurus": "You seek emotional security through comfort and stability.",
            "Gemini": "You process emotions intellectually and need variety.",
            "Cancer": "Deeply emotional and nurturing. Home is your sanctuary.",
            "Leo": "You need recognition and warmth in your emotional life.",
            "Virgo": "You feel secure when things are organized and useful.",
            "Libra": "Emotional balance comes through partnership and harmony.",
            "Scorpio": "Your emotions run deep and intense. You crave intimacy.",
            "Sagittarius": "Emotional freedom and adventure feed your soul.",
            "Capricorn": "You find security through achievement and structure.",
            "Aquarius": "You need emotional space and intellectual connection.",
            "Pisces": "Ultra-sensitive and empathic. You absorb others' feelings."
        }
        
        # Rising sign interpretation
        rising_sign = subject.first_house.sign
        rising_interpretations = {
            "Aries": "You come across as bold, direct, and energetic.",
            "Taurus": "You appear calm, steady, and approachable.",
            "Gemini": "You seem curious, talkative, and youthful.",
            "Cancer": "You give off a caring, protective vibe.",
            "Leo": "You have a warm, confident, magnetic presence.",
            "Virgo": "You appear helpful, modest, and detail-oriented.",
            "Libra": "You come across as charming, diplomatic, and refined.",
            "Scorpio": "You have an intense, mysterious, magnetic aura.",
            "Sagittarius": "You seem optimistic, adventurous, and frank.",
            "Capricorn": "You appear serious, responsible, and composed.",
            "Aquarius": "You seem unique, friendly, and unconventional.",
            "Pisces": "You give off a gentle, dreamy, compassionate vibe."
        }
        
        return {
            "sun": f"☉ **Sun in {sun_sign}**: {sun_interpretations.get(sun_sign, 'Your core identity.')}",
            "moon": f"☽ **Moon in {moon_sign}**: {moon_interpretations.get(moon_sign, 'Your emotional nature.')}",
            "rising": f"↑ **Rising {rising_sign}**: {rising_interpretations.get(rising_sign, 'How others see you.')}"
        }


def get_timezone_suggestions(city: str = None) -> List[str]:
    """Helper to suggest common timezones"""
    common_timezones = [
        "America/New_York",
        "America/Chicago",
        "America/Denver",
        "America/Los_Angeles",
        "America/Phoenix",
        "America/Anchorage",
        "Pacific/Honolulu",
        "Europe/London",
        "Europe/Paris",
        "Europe/Berlin",
        "Europe/Rome",
        "Europe/Madrid",
        "Europe/Lisbon",
        "Asia/Tokyo",
        "Asia/Shanghai",
        "Asia/Hong_Kong",
        "Asia/Singapore",
        "Asia/Dubai",
        "Asia/Kolkata",
        "Australia/Sydney",
        "Australia/Melbourne",
        "Pacific/Auckland"
    ]
    return common_timezones


if __name__ == "__main__":
    # Quick test
    generator = NatalChartGenerator()
    
    result = generator.generate_chart(
        name="Test User",
        year=1990,
        month=3,
        day=15,
        hour=14,
        minute=30,
        latitude=40.7128,
        longitude=-74.0060,
        timezone="America/New_York",
        city="New York"
    )
    
    print(json.dumps(result, indent=2))
