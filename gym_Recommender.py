"""
Gym Workout Recommendation Engine (Modern UI Edition)
------------------------------------------------------
Real Problem : Recommend personalized workouts to users
Algorithm    : Rule-based content matching (goal + level + equipment + target muscle)
GUI          : PyQt5 - modern dark theme, sidebar layout, card-based results

Author: Zain Ullah Khan
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QGroupBox, QFrame, QScrollArea, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


# ---------------------------------------------------------------------------
# 1. WORKOUT DATABASE
# ---------------------------------------------------------------------------
WORKOUT_DB = [
    {"name": "Bodyweight Squats", "goal": "Weight Loss", "level": "Beginner",
     "equipment": "None", "muscle": "Legs", "sets": "3x15", "note": "Keep chest up, knees tracking over toes."},
    {"name": "Jumping Jacks", "goal": "Weight Loss", "level": "Beginner",
     "equipment": "None", "muscle": "Full Body", "sets": "3x30s", "note": "Great warm-up / cardio burst."},
    {"name": "Mountain Climbers", "goal": "Weight Loss", "level": "Intermediate",
     "equipment": "None", "muscle": "Core", "sets": "4x20", "note": "Keep hips low, move fast but controlled."},
    {"name": "Kettlebell Swings", "goal": "Weight Loss", "level": "Intermediate",
     "equipment": "Kettlebell", "muscle": "Full Body", "sets": "4x15", "note": "Hip hinge, not a squat."},
    {"name": "Rowing Machine Intervals", "goal": "Weight Loss", "level": "Advanced",
     "equipment": "Machine", "muscle": "Full Body", "sets": "6x250m", "note": "30s rest between intervals."},

    {"name": "Push-Ups", "goal": "Muscle Gain", "level": "Beginner",
     "equipment": "None", "muscle": "Chest", "sets": "4x10", "note": "Elbows at 45 degrees, full range of motion."},
    {"name": "Dumbbell Bench Press", "goal": "Muscle Gain", "level": "Intermediate",
     "equipment": "Dumbbell", "muscle": "Chest", "sets": "4x8", "note": "Control the eccentric (lowering) phase."},
    {"name": "Barbell Squats", "goal": "Muscle Gain", "level": "Advanced",
     "equipment": "Barbell", "muscle": "Legs", "sets": "5x5", "note": "Use a spotter or safety rack."},
    {"name": "Dumbbell Rows", "goal": "Muscle Gain", "level": "Beginner",
     "equipment": "Dumbbell", "muscle": "Back", "sets": "4x10", "note": "Squeeze shoulder blade at the top."},
    {"name": "Pull-Ups", "goal": "Muscle Gain", "level": "Advanced",
     "equipment": "Machine", "muscle": "Back", "sets": "4xMax", "note": "Use assisted pull-up machine if needed."},
    {"name": "Barbell Overhead Press", "goal": "Muscle Gain", "level": "Advanced",
     "equipment": "Barbell", "muscle": "Shoulders", "sets": "4x6", "note": "Brace your core, avoid arching lower back."},

    {"name": "Plank", "goal": "Endurance", "level": "Beginner",
     "equipment": "None", "muscle": "Core", "sets": "3x45s", "note": "Keep body in a straight line."},
    {"name": "Bodyweight Lunges", "goal": "Endurance", "level": "Beginner",
     "equipment": "None", "muscle": "Legs", "sets": "3x12/leg", "note": "Front knee stays above ankle."},
    {"name": "Dumbbell Step-Ups", "goal": "Endurance", "level": "Intermediate",
     "equipment": "Dumbbell", "muscle": "Legs", "sets": "4x12/leg", "note": "Drive through the heel of the lead foot."},
    {"name": "Battle Ropes", "goal": "Endurance", "level": "Intermediate",
     "equipment": "Machine", "muscle": "Full Body", "sets": "5x30s", "note": "Keep core tight, alternate wave patterns."},
    {"name": "Treadmill Tempo Run", "goal": "Endurance", "level": "Advanced",
     "equipment": "Machine", "muscle": "Full Body", "sets": "20 min", "note": "Steady pace at ~80% max effort."},
]

GOALS = ["Weight Loss", "Muscle Gain", "Endurance"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
EQUIPMENT = ["Any", "None", "Dumbbell", "Barbell", "Kettlebell", "Machine"]
MUSCLES = ["Any", "Full Body", "Chest", "Back", "Legs", "Shoulders", "Core"]

# Accent color per goal, used for card highlight bars / badges
GOAL_COLORS = {
    "Weight Loss": "#FF6B6B",
    "Muscle Gain": "#4D96FF",
    "Endurance": "#3ADE9C",
}


# ---------------------------------------------------------------------------
# 2. RECOMMENDATION ALGORITHM
# ---------------------------------------------------------------------------
def recommend_workouts(goal, level, equipment, muscle, top_n=5):
    scored = []
    for w in WORKOUT_DB:
        score = 0
        if w["goal"] == goal:
            score += 3
        if w["level"] == level:
            score += 2
        elif abs(LEVELS.index(w["level"]) - LEVELS.index(level)) == 1:
            score += 1
        if equipment == "Any" or w["equipment"] == equipment:
            score += 2
        if muscle == "Any" or w["muscle"] == muscle:
            score += 1

        if score > 0:
            scored.append((score, w))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [w for _, w in scored[:top_n]]


# ---------------------------------------------------------------------------
# 3. GLOBAL STYLESHEET (modern dark theme)
# ---------------------------------------------------------------------------
STYLESHEET = """
QWidget {
    background-color: #12141C;
    color: #E7E9F0;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QLabel#AppTitle {
    color: #FFFFFF;
}

QLabel#AppSubtitle {
    color: #8A8FA3;
}

QGroupBox {
    background-color: #191C26;
    border: 1px solid #262A3A;
    border-radius: 12px;
    margin-top: 14px;
    padding: 16px 12px 12px 12px;
    font-weight: 600;
    color: #C7CBE0;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #9AA0C0;
}

QComboBox {
    background-color: #20232F;
    border: 1px solid #2E3244;
    border-radius: 8px;
    padding: 8px 10px;
    color: #E7E9F0;
    min-height: 18px;
}

QComboBox:hover {
    border: 1px solid #4D96FF;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #20232F;
    border: 1px solid #2E3244;
    selection-background-color: #4D96FF;
    selection-color: #FFFFFF;
    outline: none;
    padding: 4px;
}

QPushButton#PrimaryButton {
    background-color: #4D96FF;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 13px;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 0.5px;
}

QPushButton#PrimaryButton:hover {
    background-color: #6BA6FF;
}

QPushButton#PrimaryButton:pressed {
    background-color: #3B7EE0;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    background: #12141C;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #2E3244;
    border-radius: 5px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #3E4460;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""


# ---------------------------------------------------------------------------
# 4. CARD WIDGET — one styled card per recommended workout
# ---------------------------------------------------------------------------
class WorkoutCard(QFrame):
    def __init__(self, rank, workout):
        super().__init__()
        accent = GOAL_COLORS.get(workout["goal"], "#4D96FF")

        self.setStyleSheet(f"""
            QFrame#Card {{
                background-color: #191C26;
                border: 1px solid #262A3A;
                border-left: 4px solid {accent};
                border-radius: 10px;
            }}
            QLabel#Name {{
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 700;
            }}
            QLabel#Sets {{
                color: {accent};
                font-size: 13px;
                font-weight: 700;
            }}
            QLabel#Badge {{
                background-color: #20232F;
                color: #B8BCD4;
                border-radius: 8px;
                padding: 3px 10px;
                font-size: 11px;
            }}
            QLabel#Note {{
                color: #9AA0C0;
                font-size: 12px;
            }}
        """)
        self.setObjectName("Card")
        self.setFrameShape(QFrame.NoFrame)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 140))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 14, 16, 14)
        outer.setSpacing(8)

        top_row = QHBoxLayout()
        name_label = QLabel(f"#{rank}  {workout['name']}")
        name_label.setObjectName("Name")
        sets_label = QLabel(workout["sets"])
        sets_label.setObjectName("Sets")
        sets_label.setAlignment(Qt.AlignRight)
        top_row.addWidget(name_label)
        top_row.addStretch()
        top_row.addWidget(sets_label)
        outer.addLayout(top_row)

        badge_row = QHBoxLayout()
        badge_row.setSpacing(8)
        for text in (workout["goal"], workout["level"], workout["equipment"], workout["muscle"]):
            badge = QLabel(text)
            badge.setObjectName("Badge")
            badge_row.addWidget(badge)
        badge_row.addStretch()
        outer.addLayout(badge_row)

        note_label = QLabel(f"💡  {workout['note']}")
        note_label.setObjectName("Note")
        note_label.setWordWrap(True)
        outer.addWidget(note_label)


# ---------------------------------------------------------------------------
# 5. MAIN WINDOW
# ---------------------------------------------------------------------------
class GymRecommenderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gym Workout Recommendation Engine")
        self.setMinimumSize(900, 640)
        self.init_ui()

    def init_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # -------------------- Sidebar --------------------
        sidebar = QFrame()
        sidebar.setFixedWidth(320)
        sidebar.setStyleSheet("background-color: #0D0F16; border-right: 1px solid #1F2230;")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(24, 32, 24, 24)
        side_layout.setSpacing(18)

        title = QLabel("🏋️  FitMatch")
        title.setObjectName("AppTitle")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        side_layout.addWidget(title)

        subtitle = QLabel("AI-style rule-based workout matching\nbuilt on your goal, level & gear.")
        subtitle.setObjectName("AppSubtitle")
        subtitle.setWordWrap(True)
        side_layout.addWidget(subtitle)

        input_group = QGroupBox("Your Profile")
        form = QVBoxLayout()
        form.setSpacing(14)

        def field(label_text, combo):
            box = QVBoxLayout()
            box.setSpacing(6)
            lbl = QLabel(label_text)
            lbl.setStyleSheet("color:#8A8FA3; font-size:11px; font-weight:600;")
            box.addWidget(lbl)
            box.addWidget(combo)
            return box

        self.goal_box = QComboBox(); self.goal_box.addItems(GOALS)
        self.level_box = QComboBox(); self.level_box.addItems(LEVELS)
        self.equip_box = QComboBox(); self.equip_box.addItems(EQUIPMENT)
        self.muscle_box = QComboBox(); self.muscle_box.addItems(MUSCLES)

        form.addLayout(field("FITNESS GOAL", self.goal_box))
        form.addLayout(field("EXPERIENCE LEVEL", self.level_box))
        form.addLayout(field("AVAILABLE EQUIPMENT", self.equip_box))
        form.addLayout(field("TARGET MUSCLE GROUP", self.muscle_box))

        input_group.setLayout(form)
        side_layout.addWidget(input_group)

        self.recommend_btn = QPushButton("⚡  Generate My Plan")
        self.recommend_btn.setObjectName("PrimaryButton")
        self.recommend_btn.setCursor(Qt.PointingHandCursor)
        self.recommend_btn.clicked.connect(self.on_recommend)
        side_layout.addWidget(self.recommend_btn)

        side_layout.addStretch()

        footer = QLabel("Rule-based content matching engine\n© Zain Ullah Khan")
        footer.setStyleSheet("color:#4A4F66; font-size:10px;")
        side_layout.addWidget(footer)

        root.addWidget(sidebar)

        # -------------------- Main content --------------------
        content = QFrame()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 32, 32, 32)
        content_layout.setSpacing(16)

        self.result_header = QLabel("Recommended Workouts")
        self.result_header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        content_layout.addWidget(self.result_header)

        self.result_sub = QLabel("Set your profile on the left, then generate a plan.")
        self.result_sub.setStyleSheet("color:#8A8FA3;")
        self.result_sub.setWordWrap(True)
        content_layout.addWidget(self.result_sub)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setSpacing(12)
        self.cards_layout.setContentsMargins(2, 2, 2, 2)
        self.cards_layout.addStretch()
        scroll.setWidget(self.cards_container)
        content_layout.addWidget(scroll, stretch=1)

        root.addWidget(content, stretch=1)

    def clear_cards(self):
        while self.cards_layout.count() > 1:  # keep the trailing stretch
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def on_recommend(self):
        goal = self.goal_box.currentText()
        level = self.level_box.currentText()
        equipment = self.equip_box.currentText()
        muscle = self.muscle_box.currentText()

        results = recommend_workouts(goal, level, equipment, muscle)
        self.clear_cards()

        if not results:
            self.result_sub.setText("No matching workouts found. Try changing your filters.")
            return

        self.result_sub.setText(
            f"Plan for {goal} · {level} · Equipment: {equipment} · Focus: {muscle}"
        )
        for i, w in enumerate(results, 1):
            card = WorkoutCard(i, w)
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = GymRecommenderApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
