#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
স্মার্ট কৃষি পরিকল্পনা - Modern Web Dashboard
WebView-based application serving the modern agriculture dashboard
"""

import os
import sys
import webview
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"
STYLES_FILE = BASE_DIR / "styles.css"
SCRIPT_FILE = BASE_DIR / "script.js"

# Verify files exist
for file in [INDEX_FILE, STYLES_FILE, SCRIPT_FILE]:
    if not file.exists():
        print(f"⚠️ Warning: {file.name} not found in {BASE_DIR}")

class CropAssistantAPI:
    """API backend for crop assistant functionality"""
    
    def __init__(self):
        self.crop_data = self._load_crop_data()
    
    def _load_crop_data(self):
        """Load crop data from JSON files"""
        crop_data = {}
        json_files = ['crop_data.json', 'rice_data.json', 'wheat_data.json', 'vegetable_data.json', 'potato_data.json']
        
        for filename in json_files:
            filepath = BASE_DIR / filename
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        crop_data[filename] = json.load(f)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        return crop_data
    
    def get_suggestions(self, division, district, soil, season):
        """Get crop suggestions based on location and environment"""
        suggestions = {
            'crops': [
                {'name': 'ধান', 'details': 'উৎপাদনশীল জাত - ব্রি ধান ২৮', 'yield': '৬.৫ টন/একর'},
                {'name': 'গম', 'details': 'শীতকালীন ফসল - আশ্রয়ী দাম', 'yield': '৪.৫ টন/একর'},
                {'name': 'ভুট্টা', 'details': 'উচ্চ ফলনশীল - ১২০ দিনে পরিপক্ক', 'yield': '৫.৮ টন/একর'}
            ],
            'fertilizer': 'ইউরিয়া ৩০০ কেজি/একর, ফসফেট ১৫০ কেজি/একর',
            'watering': 'গ্রীষ্মে ১৫ দিন পর পর, শীতে ২০ দিন পর পর',
            'expectedYield': '৬.৫ টন/একর',
            'plantingTime': 'জানুয়ারি-মার্চ',
            'harvestTime': 'জুন-আগস্ট'
        }
        return suggestions
    
    def get_weather(self):
        """Get weather information"""
        return {
            'temp': '২৮°C',
            'condition': 'আংশিক মেঘলা',
            'humidity': '৬৫%',
            'windSpeed': '১২ কিমি/ঘন্টা',
            'forecast': 'পরবর্তী ২ দিন বৃষ্টির সম্ভাবনা',
            'uvIndex': 'মধ্যম',
            'pressure': '১০১৩ মিলিবার'
        }
    
    def get_market_prices(self):
        """Get current market prices"""
        return {
            'crops': [
                {'name': 'ধান (খোসা ছাড়া)', 'price': '১৮০০-২০০০ টাকা/মণ'},
                {'name': 'গম', 'price': '২১০০-২৩০০ টাকা/মণ'},
                {'name': 'আলু', 'price': '১০-১৫ টাকা/কেজি'},
                {'name': 'পেঁয়াজ', 'price': '৩০-৪০ টাকা/কেজি'}
            ],
            'lastUpdated': '৩০ মিনিট আগে'
        }
    
    def get_nearby_offices(self):
        """Get nearby agriculture offices"""
        return {
            'offices': [
                {'name': 'ঢাকা জেলা কৃষি সম্প্রসারণ অফিস', 'distance': '২.৫ কিমি', 'phone': '০২-৫৫০০১২৩'},
                {'name': 'নারায়ণগঞ্জ উপজেলা কৃষি অফিস', 'distance': '৫.২ কিমি', 'phone': '০২-৭৭১০০৫০'},
                {'name': 'গাজীপুর জেলা কৃষি অফিস', 'distance': '৮.৭ কিমি', 'phone': '০২-৯২৩০০৫২'}
            ]
        }
    
    def calculate_profit(self, income, cost):
        """Calculate profit from income and cost"""
        profit = income - cost
        return {
            'income': f'{income:,.0f} টাকা',
            'cost': f'{cost:,.0f} টাকা',
            'profit': f'{profit:,.0f} টাকা',
            'profitMargin': f'{(profit/income*100):.1f}%' if income > 0 else '০%'
        }
    
    def get_disease_info(self, crop=None):
        """Get crop disease information"""
        return {
            'common_diseases': [
                {'name': 'পাতার দাগ রোগ', 'symptoms': 'পাতায় বাদামি দাগ', 'cure': 'ছত্রাকনাশক ২ সপ্তাহ পর পর প্রয়োগ করুন'},
                {'name': 'শীষ পচা রোগ', 'symptoms': 'শীষ পচে যায়', 'cure': 'সুস্থ বীজ ব্যবহার করুন এবং জল নিকাশ ভালো করুন'},
                {'name': 'গাছের গোড়া পচা', 'symptoms': 'গাছ হঠাৎ মুড়ে পড়ে', 'cure': 'আক্রান্ত জায়গায় বোরো এবং সিঙ্ক দ্বারা চিকিৎসা করুন'}
            ]
        }

# Initialize API
api = CropAssistantAPI()

# Create window with exposed API
if __name__ == '__main__':
    print('=' * 70)
    print('🌾 স্মার্ট কৃষি পরিকল্পনা - Modern Web Dashboard')
    print('=' * 70)
    
    window = webview.create_window(
        title='স্মার্ট কৃষি পরিকল্পনা',
        url=str(INDEX_FILE),
        js_api=api,
        width=1380,
        height=900,
        resizable=True,
        min_size=(1000, 700),
        background_color='#F0FDF4'
    )
    
    print('✅ Dashboard loading...')
    print('📍 Opening modern agriculture dashboard')
    print('=' * 70)
    
    webview.start(debug=False)