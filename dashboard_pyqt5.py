import json
import os
import subprocess
import sys

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError as exc:
    raise ImportError(
        "PyQt5 is required to run the new dashboard. Install it with `pip install PyQt5`."
    ) from exc

from database import init_db, load_json_to_db


class FeatureCard(QtWidgets.QFrame):
    def __init__(self, title, description, color, callback, parent=None):
        super().__init__(parent)
        self.callback = callback
        self.setObjectName("featureCard")
        self.setStyleSheet(
            "#featureCard {"
            "  border: 1px solid rgba(0, 0, 0, 0.08);"
            "  border-radius: 18px;"
            "  background: white;"
            "}"
        )
        self.setFixedHeight(140)

        icon_frame = QtWidgets.QFrame(self)
        icon_frame.setFixedSize(48, 48)
        icon_frame.setStyleSheet(
            f"background: {color}; border-radius: 24px;"
        )
        icon_label = QtWidgets.QLabel("🌱", icon_frame)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        icon_label.setStyleSheet("color: white; font-size: 20px;")

        title_label = QtWidgets.QLabel(title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-size: 13px; font-weight: 700; color: #2e7d32;")

        desc_label = QtWidgets.QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 11px; color: #555555;")

        open_button = QtWidgets.QPushButton("▶️ খুলুন")
        open_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        open_button.clicked.connect(self.callback)
        open_button.setStyleSheet(
            "QPushButton {"
            "  background: #4caf50;"
            "  color: white;"
            "  border: none;"
            "  border-radius: 10px;"
            "  padding: 8px 14px;"
            "  font-weight: 700;"
            "}"
            "QPushButton:hover { background: #43a047; }"
        )

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)
        content_layout.addWidget(title_label)
        content_layout.addWidget(desc_label)
        content_layout.addStretch()
        content_layout.addWidget(open_button, 0, QtCore.Qt.AlignRight)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(icon_frame, 0, QtCore.Qt.AlignTop)
        left_layout.addStretch()

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(14)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(content_layout)


class DashboardWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.crop_data = self.load_crop_data()
        self.setWindowTitle("🌾 স্মার্ট কৃষি পরিকল্পনা")
        self.resize(1100, 820)
        self.setStyleSheet("background: #e8f5e9;")

        self.build_ui()

    def load_crop_data(self):
        crop_file = os.path.join(self.script_dir, "crop_data.json")
        if not os.path.exists(crop_file):
            return []
        with open(crop_file, "r", encoding="utf-8") as handle:
            try:
                return json.load(handle)
            except json.JSONDecodeError:
                return []

    def build_ui(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(20)

        root_layout.addLayout(self.build_header())
        root_layout.addLayout(self.build_action_row())
        root_layout.addWidget(self.build_search_card())
        root_layout.addWidget(self.build_feature_grid(), 1)

    def build_header(self):
        title = QtWidgets.QLabel("স্মার্ট কৃষি পরিকল্পনা")
        title.setStyleSheet("font-size: 36px; font-weight: 800; color: #1b5e20;")

        subtitle = QtWidgets.QLabel("তথ্যভিত্তিক সিদ্ধান্ত, সফল কৃষি ও সুখী জীবন")
        subtitle.setStyleSheet("font-size: 15px; color: #4e4e4e;")

        logo = QtWidgets.QFrame()
        logo.setFixedSize(72, 72)
        logo.setStyleSheet(
            "background: #4caf50; border-radius: 20px;"
        )
        logo_label = QtWidgets.QLabel("🌿", logo)
        logo_label.setAlignment(QtCore.Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 28px; color: white;")

        text_layout = QtWidgets.QVBoxLayout()
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addWidget(logo)
        header_layout.addSpacing(18)
        header_layout.addLayout(text_layout)
        header_layout.addStretch()

        return header_layout

    def build_action_row(self):
        action_container = QtWidgets.QFrame()
        action_container.setStyleSheet(
            "background: white; border-radius: 24px;"
        )
        action_container.setContentsMargins(24, 20, 24, 20)

        search_field = QtWidgets.QLineEdit()
        search_field.setPlaceholderText("ফসলের নাম লিখুন...")
        search_field.setFixedHeight(44)
        search_field.setStyleSheet(
            "border: 1px solid #cccccc; border-radius: 14px; padding: 0 14px; font-size: 14px;"
        )
        self.search_input = search_field

        search_button = QtWidgets.QPushButton("🔍 অনুসন্ধান")
        search_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        search_button.setFixedHeight(44)
        search_button.setStyleSheet(
            "QPushButton { background: #4caf50; color: white; border: none; border-radius: 14px; font-weight: 700; padding: 0 24px; }"
            "QPushButton:hover { background: #43a047; }"
        )
        search_button.clicked.connect(self.search_crop)

        manage_button = QtWidgets.QPushButton("✨ ফসলের সাধারণ গাইড পান")
        manage_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        manage_button.setFixedHeight(44)
        manage_button.setStyleSheet(
            "QPushButton { background: #2e7d32; color: white; border: none; border-radius: 14px; font-weight: 700; padding: 0 24px; }"
            "QPushButton:hover { background: #1b5e20; }"
        )
        manage_button.clicked.connect(self.show_guide)

        weather_button = QtWidgets.QPushButton("☁️ আবহাওয়া দেখুন")
        weather_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        weather_button.setFixedHeight(44)
        weather_button.setStyleSheet(
            "QPushButton { background: #0288d1; color: white; border: none; border-radius: 14px; font-weight: 700; padding: 0 24px; }"
            "QPushButton:hover { background: #0277bd; }"
        )
        weather_button.clicked.connect(self.show_weather)

        columns = QtWidgets.QHBoxLayout(action_container)
        columns.setContentsMargins(0, 0, 0, 0)
        columns.setSpacing(12)
        columns.addWidget(search_field, 2)
        columns.addWidget(search_button, 0)
        columns.addWidget(manage_button, 0)
        columns.addWidget(weather_button, 0)

        wrapper = QtWidgets.QVBoxLayout()
        wrapper.setContentsMargins(0, 0, 0, 0)
        wrapper.setSpacing(8)
        wrapper.addWidget(action_container)

        return wrapper

    def build_search_card(self):
        card = QtWidgets.QFrame()
        card.setStyleSheet(
            "background: white; border-radius: 20px;"
        )
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(14)

        heading = QtWidgets.QLabel("🔍 দ্রুত ফসলের তথ্য খুঁজুন")
        heading.setStyleSheet("font-size: 16px; font-weight: 700; color: #1b5e20;")

        body = QtWidgets.QLabel(
            "ফসলের নাম লিখে দ্রুত আপনার ফসলের সার, সেচ এবং বপন সময় সম্পর্কে তথ্য জানতে পারেন।"
        )
        body.setWordWrap(True)
        body.setStyleSheet("font-size: 12px; color: #555555;")

        self.result_label = QtWidgets.QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("font-size: 12px; color: #3e2723; background: #f1f8e9; border: 1px solid #dcedc8; border-radius: 14px; padding: 14px;")

        card_layout.addWidget(heading)
        card_layout.addWidget(body)
        card_layout.addWidget(self.result_label)

        return card

    def build_feature_grid(self):
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        container = QtWidgets.QWidget()
        grid_layout = QtWidgets.QGridLayout(container)
        grid_layout.setSpacing(18)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        self.features = [
            ("🌾 উৎপাদন ট্র্যাকিং", "ফসলের উৎপাদন এবং ফলন ট্র্যাক করুন", "#81C784", "feature_1_production_tracking.py"),
            ("👨‍🌾 কৃষক প্রোফাইল", "কৃষকের ব্যক্তিগত তথ্য ও জমি পরিচালনা করুন", "#66BB6A", "feature_2_farmer_profile.py"),
            ("🌏 জমির ম্যাপিং", "জমির অবস্থান ও সীমানা চিহ্নিত করুন", "#4CAF50", "feature_3_land_mapping.py"),
            ("📊 সার ক্যালকুলেটর", "ফসল অনুযায়ী সঠিক সার পরিমাণ জানুন", "#388E3C", "feature_4_fertilizer_calculator.py"),
            ("🚜 যন্ত্রপাতি ভাড়া", "যন্ত্রপাতি ভাড়া ও খরচ পরিচালনা করুন", "#00796B", "feature_5_machinery_rental.py"),
            ("📱 বীজ ডিরেক্টরি", "বীজ ও সরঞ্জাম সরবরাহকারী খুঁজুন", "#7B1FA2", "feature_6_seeds_equipment.py"),
            ("💰 ঋণ চেকার", "কৃষি ঋণের যোগ্যতা যাচাই করুন", "#F57F17", "feature_7_loan_checker.py"),
            ("📈 ফসল রোটেশন", "ফসল চক্র পরিকল্পনা করুন", "#F57C00", "feature_8_crop_rotation.py"),
            ("🎥 ভিডিও লাইব্রেরি", "কৃষি ভিডিও টিউটোরিয়াল দেখুন", "#E91E63", "feature_9_video_library.py"),
            ("📋 রিপোর্ট এক্সপোর্ট", "রিপোর্ট তৈরি করুন ও সেভ করুন", "#1565C0", "feature_10_report_export.py"),
        ]

        for index, (title, desc, color, script) in enumerate(self.features):
            row = index // 2
            col = index % 2
            card = FeatureCard(title, desc, color, lambda s=script: self.open_feature_script(s), self)
            grid_layout.addWidget(card, row, col)

        container.setLayout(grid_layout)
        scroll_area.setWidget(container)
        return scroll_area

    def open_feature_script(self, script_name):
        script_path = os.path.join(self.script_dir, script_name)
        if not os.path.exists(script_path):
            QtWidgets.QMessageBox.warning(
                self,
                "ফিচার পাওয়া যায়নি",
                f"স্ক্রিপ্ট খুঁজে পাওয়া যায়নি: {script_name}"
            )
            return

        try:
            subprocess.Popen([sys.executable, script_path], cwd=self.script_dir)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(
                self,
                "লঞ্চ ব্যর্থ হয়েছে",
                f"ফিচার লঞ্চ করা যায়নি:\n{exc}"
            )

    def show_guide(self):
        content = (
            "📚 ফসলের সাধারণ গাইড\n\n"
            "• বোঝার জন্য প্রতিটি ফসলের বপন, সার এবং সেচের তথ্য দেখে নিন।\n"
            "• এখানে আপনি উচ্চ ফলনশীল পদ্ধতি ও মৌসুম ভিত্তিক টিপস পাবেন।\n"
            "• নির্দিষ্ট ফসলের জন্য উপযুক্ত সার ও পানি ব্যবস্থাপনার টিপস।\n"
        )
        QtWidgets.QMessageBox.information(self, "ফসলের সাধারণ গাইড", content)

    def show_weather(self):
        content = (
            "🌤️ আজকের আবহাওয়া\n\n"
            "ঢাকা: ২৮°C, হালকা মেঘলা, বাতাস ১২ কিমি/ঘণ্টা\n"
            "চট্টগ্রাম: ২৬°C, আদ্র, বৃষ্টি সম্ভাবনা ৩০%\n"
            "রাজশাহী: ৩২°C, রৌদ্রোজ্জ্বল, আর্দ্রতা ৫৫%\n"
            "খুলনা: ২৯°C, মেঘলা, বৃষ্টির সম্ভাবনা ৪০%\n"
        )
        QtWidgets.QMessageBox.information(self, "আবহাওয়া দেখুন", content)

    def search_crop(self):
        query = self.search_input.text().strip()
        if not query:
            self.result_label.setText("অনুগ্রহ করে একটি ফসলের নাম লিখুন।")
            return

        matches = []
        for item in self.crop_data:
            name = item.get("crop") or item.get("name") or ""
            if query.lower() in name.lower():
                matches.append(item)

        if not matches:
            self.result_label.setText("কোনও ফলাফল পাওয়া যায়নি। অন্য নাম চেষ্টা করুন।")
            return

        lines = []
        for item in matches[:3]:
            crop = item.get("crop", "-")
            plant_time = item.get("plant_time", "-")
            fertilizer = item.get("fertilizer", "-")
            lines.append(f"• {crop} — বপন: {plant_time}, সার: {fertilizer}")

        self.result_label.setText("\n".join(lines))


def main():
    try:
        init_db()
        load_json_to_db("crop_data.json")
    except Exception:
        pass

    app = QtWidgets.QApplication([])
    dashboard = DashboardWindow()
    dashboard.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
