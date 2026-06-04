import json
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QComboBox, 
                             QScrollArea, QFrame, QGridLayout)

from database import init_db, load_json_to_db

# ============ ফিচার মডিউল ইম্পোর্ট ============
try:
    from feature_1_production_tracking import open_production_tracker_window
    from feature_2_farmer_profile import open_farmer_profile_window
    from feature_3_land_mapping import open_land_mapping_window
    from feature_4_fertilizer_calculator import open_fertilizer_calculator_window
    from feature_5_machinery_rental import open_machinery_rental_window
    from feature_6_seeds_equipment import open_seeds_equipment_window
    from feature_7_loan_checker import open_loan_eligibility_window
    from feature_8_crop_rotation import open_crop_rotation_window
    from feature_9_video_library import open_video_library_window
    from feature_10_report_export import open_report_export_window
except ImportError as e:
    print(f"⚠️ কিছু ফিচার ইম্পোর্ট ব্যর্থ হয়েছে: {e}")

# ============ কালার স্কিম ============
PRIMARY_GREEN = "#2e7d32"
LIGHT_GREEN = "#4caf50"
ACCENT_GREEN = "#66bb6a"
DARK_GREEN = "#1b5e20"
LIGHT_BG = "#f1f8f5"
WHITE = "#ffffff"
TEXT_DARK = "#333333"
TEXT_LIGHT = "#666666"

# ============ ফিচার ডেটা ============
FEATURES = [
    {
        "id": 1,
        "title": "ফসল উৎপাদন ট্র্যাকিং",
        "description": "আপনার ফসলের উৎপাদন রেকর্ড করুন এবং পর্যবেক্ষণ করুন",
        "icon": "📊",
        "color": "#1976D2",
        "callback": "open_production_tracker_window"
    },
    {
        "id": 2,
        "title": "কৃষক প্রোফাইল",
        "description": "আপনার ব্যক্তিগত তথ্য এবং জমির বিবরণ সংরক্ষণ করুন",
        "icon": "👤",
        "color": "#D32F2F",
        "callback": "open_farmer_profile_window"
    },
    {
        "id": 3,
        "title": "জমি ম্যাপিং",
        "description": "আপনার জমির ডিজিটাল ম্যাপ তৈরি করুন",
        "icon": "🗺️",
        "color": "#388E3C",
        "callback": "open_land_mapping_window"
    },
    {
        "id": 4,
        "title": "সার ক্যালকুলেটর",
        "description": "সঠিক পরিমাণ সার হিসাব করুন",
        "icon": "🧪",
        "color": "#F57C00",
        "callback": "open_fertilizer_calculator_window"
    },
    {
        "id": 5,
        "title": "যন্ত্রপাতি ভাড়া",
        "description": "কৃষি যন্ত্রপাতি ভাড়া নিন এবং দিন",
        "icon": "🚜",
        "color": "#7B1FA2",
        "callback": "open_machinery_rental_window"
    },
    {
        "id": 6,
        "title": "বীজ এবং সরঞ্জাম",
        "description": "উন্নত মানের বীজ ও সরঞ্জাম কিনুন",
        "icon": "🌾",
        "color": "#C2185B",
        "callback": "open_seeds_equipment_window"
    },
    {
        "id": 7,
        "title": "ঋণ পরীক্ষক",
        "description": "কৃষি ঋণের যোগ্যতা যাচাই করুন",
        "icon": "💰",
        "color": "#0097A7",
        "callback": "open_loan_eligibility_window"
    },
    {
        "id": 8,
        "title": "ফসল পর্যায়ন",
        "description": "সঠিক ফসল নির্বাচন এবং পর্যায়ন পরিকল্পনা",
        "icon": "🔄",
        "color": "#455A64",
        "callback": "open_crop_rotation_window"
    },
    {
        "id": 9,
        "title": "ভিডিও লাইব্রেরি",
        "description": "কৃষি প্রশিক্ষণ ভিডিও দেখুন",
        "icon": "📹",
        "color": "#E64A19",
        "callback": "open_video_library_window"
    },
    {
        "id": 10,
        "title": "রিপোর্ট এবং এক্সপোর্ট",
        "description": "আপনার ডেটা রিপোর্ট তৈরি এবং ডাউনলোড করুন",
        "icon": "📄",
        "color": "#1565C0",
        "callback": "open_report_export_window"
    }
]

# ============ কাস্টম কার্ড উইজেট ============
class FeatureCard(QFrame):
    clicked = QtCore.pyqtSignal()
    
    def __init__(self, feature, parent=None):
        super().__init__(parent)
        self.feature = feature
        self.is_hovered = False
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border: 2px solid #e8e8e8;
                border-radius: 16px;
                padding: 0px;
            }}
        """)
        self.setFixedHeight(200)
        self.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # রঙিন হেডার বার
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {feature['color']},
                    stop:1 rgba(46, 125, 50, 0.8));
                border-radius: 12px;
            }}
        """)
        header_frame.setFixedHeight(60)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        # আইকন
        icon_label = QLabel(feature["icon"])
        icon_label.setFont(QFont("Arial", 28))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(50, 50)
        icon_label.setStyleSheet(f"""
            background-color: rgba(255,255,255,0.2);
            border-radius: 10px;
            color: white;
            font-size: 28px;
        """)
        header_layout.addWidget(icon_label)
        
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
        
        # শিরোনাম
        title_label = QLabel(feature["title"])
        title_label.setFont(QFont("Arial", 13, QFont.Bold))
        title_label.setStyleSheet(f"color: {PRIMARY_GREEN}; letter-spacing: 0.3px;")
        layout.addWidget(title_label)
        
        # বর্ণনা
        desc_label = QLabel(feature["description"])
        desc_label.setFont(QFont("Arial", 10))
        desc_label.setStyleSheet(f"color: {TEXT_LIGHT}; line-height: 1.5;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # বাটন
        btn = QPushButton("▶ খুলুন")
        btn.setFont(QFont("Arial", 11, QFont.Bold))
        btn.setFixedHeight(40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_GREEN};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
                letter-spacing: 0.3px;
            }}
            QPushButton:hover {{
                background-color: {PRIMARY_GREEN};
            }}
            QPushButton:pressed {{
                background-color: {DARK_GREEN};
            }}
        """)
        btn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        btn.clicked.connect(self.on_click)
        layout.addWidget(btn)
    
    def on_click(self):
        self.clicked.emit()
    
    def mousePressEvent(self, event):
        self.on_click()
    
    def enterEvent(self, event):
        self.is_hovered = True
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border: 2px solid {ACCENT_GREEN};
                border-radius: 16px;
                padding: 0px;
            }}
        """)
    
    def leaveEvent(self, event):
        self.is_hovered = False
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border: 2px solid #e8e8e8;
                border-radius: 16px;
                padding: 0px;
            }}
        """)

# ============ মেইন ড্যাশবোর্ড উইন্ডো ============
class SmartFarmingDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌾 স্মার্ট কৃষি পরিকল্পনা - ড্যাশবোর্ড")
        self.setGeometry(100, 100, 1200, 900)
        self.setStyleSheet(f"background-color: {LIGHT_BG};")
        
        # ডাটাবেস ইনিশিয়ালাইজ করুন
        try:
            init_db()
            load_json_to_db("crop_data.json")
        except Exception as e:
            print(f"ডাটাবেস ইরর: {e}")
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # ============ হেডার সেকশন ============
        header = self.create_header()
        main_layout.addWidget(header)
        
        # ============ হিরো সেকশন ============
        hero = self.create_hero_section()
        main_layout.addWidget(hero)
        
        # ============ ফিল্টার সেকশন ============
        filter_section = self.create_filter_section()
        main_layout.addWidget(filter_section)
        
        # ============ ফিচার কার্ড গ্রিড ============
        cards_widget = self.create_features_grid()
        main_layout.addWidget(cards_widget, 1)
        
        # ============ ফুটার ============
        footer = self.create_footer()
        main_layout.addWidget(footer)
    
    def create_header(self):
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {DARK_GREEN}, stop:0.5 {PRIMARY_GREEN}, stop:1 {ACCENT_GREEN});
                padding: 12px 30px;
                border: none;
            }}
        """)
        header.setFixedHeight(70)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 8, 20, 8)
        layout.setSpacing(15)
        
        # লোগো কন্টেইনার
        logo_container = QFrame()
        logo_container.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(255,255,255,0.15);
                border: 2px solid {WHITE};
                border-radius: 12px;
                padding: 5px;
            }}
        """)
        logo_container.setFixedSize(55, 55)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        
        logo_label = QLabel("🌾")
        logo_label.setFont(QFont("Arial", 32, QFont.Bold))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(f"color: {WHITE}; background-color: transparent;")
        logo_layout.addWidget(logo_label)
        
        layout.addWidget(logo_container)
        
        # টাইটেল লেআউট
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)
        
        main_title = QLabel("স্মার্ট কৃষি পরিকল্পনা")
        main_title.setFont(QFont("Arial", 18, QFont.Bold))
        main_title.setStyleSheet(f"color: {WHITE}; letter-spacing: 0.5px;")
        title_layout.addWidget(main_title)
        
        subtitle = QLabel("আধুনিক প্রযুক্তি সহ কৃষকদের জন্য সমাধান")
        subtitle.setFont(QFont("Arial", 9))
        subtitle.setStyleSheet(f"color: rgba(255,255,255,0.85);")
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # ইউজার প্রোফাইল বাটন
        profile_btn = QPushButton("👤 আমার প্রোফাইল")
        profile_btn.setFont(QFont("Arial", 9, QFont.Bold))
        profile_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255,255,255,0.15);
                color: {WHITE};
                border: 1px solid rgba(255,255,255,0.4);
                border-radius: 8px;
                padding: 8px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255,255,255,0.25);
                border: 1px solid {WHITE};
            }}
        """)
        profile_btn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        layout.addWidget(profile_btn)
        
        # সেটিংস বাটন
        settings_btn = QPushButton("⚙️ সেটিংস")
        settings_btn.setFont(QFont("Arial", 9, QFont.Bold))
        settings_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255,255,255,0.15);
                color: {WHITE};
                border: 1px solid rgba(255,255,255,0.4);
                border-radius: 8px;
                padding: 8px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255,255,255,0.25);
                border: 1px solid {WHITE};
            }}
        """)
        settings_btn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        layout.addWidget(settings_btn)
        
        return header
    
    def create_hero_section(self):
        hero = QFrame()
        hero.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {ACCENT_GREEN}, 
                    stop:0.5 {PRIMARY_GREEN}, 
                    stop:1 {DARK_GREEN});
                padding: 50px 40px;
                border: none;
            }}
        """)
        hero.setFixedHeight(280)
        
        layout = QVBoxLayout(hero)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)
        
        # প্রধান শিরোনাম
        main_title = QLabel("স্মার্ট কৃষি সমাধান")
        main_title.setFont(QFont("Arial", 40, QFont.Bold))
        main_title.setStyleSheet(f"color: {WHITE}; letter-spacing: 1px;")
        main_title.setAlignment(Qt.AlignLeft)
        layout.addWidget(main_title)
        
        # সাবটাইটেল ১
        subtitle1 = QLabel("আধুনিক প্রযুক্তি দিয়ে আপনার কৃষি উন্নত করুন")
        subtitle1.setFont(QFont("Arial", 15))
        subtitle1.setStyleSheet(f"color: rgba(255,255,255,0.95); letter-spacing: 0.3px;")
        layout.addWidget(subtitle1)
        
        # সাবটাইটেল ২
        subtitle2 = QLabel("ফসল উৎপাদন, মার্কেট মূল্য এবং ঋণের তথ্য পান এক জায়গায়")
        subtitle2.setFont(QFont("Arial", 11))
        subtitle2.setStyleSheet(f"color: rgba(255,255,255,0.85);")
        layout.addWidget(subtitle2)
        
        layout.addSpacing(10)
        
        # দুটি মেইন বাটন
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        
        btn1 = QPushButton("✓ ফসলের সাপোর্ট")
        btn1.setFont(QFont("Arial", 12, QFont.Bold))
        btn1.setFixedHeight(48)
        btn1.setFixedWidth(250)
        btn1.setStyleSheet(f"""
            QPushButton {{
                background-color: {WHITE};
                color: {PRIMARY_GREEN};
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
            QPushButton:pressed {{
                background-color: #e0e0e0;
            }}
        """)
        btn1.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        btn_layout.addWidget(btn1)
        
        btn2 = QPushButton("☁ আবহাওয়া তথ্য")
        btn2.setFont(QFont("Arial", 12, QFont.Bold))
        btn2.setFixedHeight(48)
        btn2.setFixedWidth(250)
        btn2.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255,255,255,0.2);
                color: {WHITE};
                border: 2px solid {WHITE};
                border-radius: 10px;
                padding: 12px 24px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background-color: rgba(255,255,255,0.35);
                border: 2px solid {WHITE};
            }}
            QPushButton:pressed {{
                background-color: rgba(255,255,255,0.25);
            }}
        """)
        btn2.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        btn_layout.addWidget(btn2)
        
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        return hero
    
    def create_filter_section(self):
        filter_frame = QFrame()
        filter_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                padding: 25px 30px;
                border: none;
                border-bottom: 3px solid #e0e0e0;
            }}
        """)
        filter_frame.setFixedHeight(110)
        
        layout = QVBoxLayout(filter_frame)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # শিরোনাম
        title_label = QLabel("📋 অনুসন্ধান এবং পরিবর্তন নির্বাচন করুন")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setStyleSheet(f"color: {PRIMARY_GREEN}; letter-spacing: 0.3px;")
        layout.addWidget(title_label)
        
        # ফিল্টার কম্বোবক্স
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(20)
        
        # অঞ্চল নির্বাচন
        region_label = QLabel("অঞ্চল:")
        region_label.setFont(QFont("Arial", 11, QFont.Bold))
        region_label.setStyleSheet(f"color: {PRIMARY_GREEN};")
        region_label.setFixedWidth(60)
        filter_layout.addWidget(region_label)
        
        region_combo = QComboBox()
        region_combo.addItems(["সব অঞ্চল", "ঢাকা", "চট্টগ্রাম", "খুলনা", "সিলেট", "রাজশাহী"])
        region_combo.setFont(QFont("Arial", 10))
        region_combo.setFixedWidth(140)
        region_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {LIGHT_BG};
                border: 2px solid {ACCENT_GREEN};
                border-radius: 8px;
                padding: 8px 10px;
                color: {TEXT_DARK};
                font-weight: 500;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        filter_layout.addWidget(region_combo)
        
        # ফসল নির্বাচন
        crop_label = QLabel("ফসল:")
        crop_label.setFont(QFont("Arial", 11, QFont.Bold))
        crop_label.setStyleSheet(f"color: {PRIMARY_GREEN};")
        crop_label.setFixedWidth(60)
        filter_layout.addWidget(crop_label)
        
        crop_combo = QComboBox()
        crop_combo.addItems(["সব ফসল", "ধান", "গম", "ভুট্টা", "পাট", "আলু", "আখ"])
        crop_combo.setFont(QFont("Arial", 10))
        crop_combo.setFixedWidth(140)
        crop_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {LIGHT_BG};
                border: 2px solid {ACCENT_GREEN};
                border-radius: 8px;
                padding: 8px 10px;
                color: {TEXT_DARK};
                font-weight: 500;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        filter_layout.addWidget(crop_combo)
        
        # মাটির ধরন
        soil_label = QLabel("মাটি:")
        soil_label.setFont(QFont("Arial", 11, QFont.Bold))
        soil_label.setStyleSheet(f"color: {PRIMARY_GREEN};")
        soil_label.setFixedWidth(60)
        filter_layout.addWidget(soil_label)
        
        soil_combo = QComboBox()
        soil_combo.addItems(["সব ধরনের মাটি", "এঁটেল", "বালি", "দোআঁশ", "পলিমাটি"])
        soil_combo.setFont(QFont("Arial", 10))
        soil_combo.setFixedWidth(140)
        soil_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {LIGHT_BG};
                border: 2px solid {ACCENT_GREEN};
                border-radius: 8px;
                padding: 8px 10px;
                color: {TEXT_DARK};
                font-weight: 500;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        filter_layout.addWidget(soil_combo)
        
        filter_layout.addStretch()
        
        # সার্চ বাটন
        search_btn = QPushButton("🔍 সার্চ")
        search_btn.setFont(QFont("Arial", 10, QFont.Bold))
        search_btn.setFixedWidth(100)
        search_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_GREEN};
                color: {WHITE};
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {PRIMARY_GREEN};
            }}
            QPushButton:pressed {{
                background-color: {DARK_GREEN};
            }}
        """)
        search_btn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        filter_layout.addWidget(search_btn)
        
        layout.addLayout(filter_layout)
        
        return filter_frame
    
    def create_features_grid(self):
        scroll = QScrollArea()
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {LIGHT_BG};
            }}
            QScrollBar:vertical {{
                background-color: {LIGHT_BG};
                width: 12px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background-color: {ACCENT_GREEN};
                border-radius: 6px;
                min-height: 20px;
            }}
        """)
        scroll.setWidgetResizable(True)
        
        container = QWidget()
        container.setStyleSheet(f"background-color: {LIGHT_BG};")
        grid_layout = QGridLayout(container)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setSpacing(20)
        
        # ফিচার কার্ড তৈরি করুন
        for idx, feature in enumerate(FEATURES):
            card = FeatureCard(feature)
            callback_name = feature["callback"]
            
            # কলব্যাক সংযোগ করুন
            if callback_name in globals():
                card.clicked.connect(globals()[callback_name])
            
            row = idx // 3
            col = idx % 3
            grid_layout.addWidget(card, row, col)
        
        scroll.setWidget(container)
        return scroll
    
    def create_footer(self):
        footer = QFrame()
        footer.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {DARK_GREEN}, stop:1 {PRIMARY_GREEN});
                padding: 20px 30px;
                border: none;
                border-top: 3px solid {ACCENT_GREEN};
            }}
        """)
        footer.setFixedHeight(70)
        
        layout = QVBoxLayout(footer)
        layout.setContentsMargins(30, 15, 30, 15)
        layout.setSpacing(8)
        
        # মেইন ফুটার টেক্সট
        footer_label = QLabel("© ২০২৬ স্মার্ট কৃষি পরিকল্পনা - সকল অধিকার সংরক্ষিত | আমাদের সাথে থাকুন কৃষিতে সফল হতে")
        footer_label.setFont(QFont("Arial", 10))
        footer_label.setStyleSheet(f"color: {WHITE}; letter-spacing: 0.2px;")
        layout.addWidget(footer_label)
        
        # সাবটেক্সট
        sub_footer = QLabel("ডেভেলপার: স্মার্ট কৃষি টিম | সংস্করণ: v1.0.0 | সাপোর্ট: support@smartkrishi.bd")
        sub_footer.setFont(QFont("Arial", 9))
        sub_footer.setStyleSheet(f"color: rgba(255,255,255,0.8);")
        layout.addWidget(sub_footer)
        
        return footer

# ============ মেইন এক্সিকিউশন ============
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # গ্লোবাল স্টাইলশীট (অপশনাল)
    app.setStyle('Fusion')
    
    dashboard = SmartFarmingDashboard()
    dashboard.show()
    
    sys.exit(app.exec_())
