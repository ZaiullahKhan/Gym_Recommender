# Gym_Recommender
# Gym Workout Recommendation Engine

A desktop app built with **PyQt5** that recommends personalized gym workouts based on your fitness goal, experience level, available equipment, and target muscle group.

## What It Does

- Takes user input: Fitness Goal (Weight Loss / Muscle Gain / Endurance), Fitness Level (Beginner / Intermediate / Advanced), Available Equipment, and Target Muscle Group.
- Runs a content-based recommendation algorithm that scores each workout in the database against your profile (goal match weighted highest, then level, equipment, and muscle group).
- Displays the top 5 matching workouts with sets/reps and a short form tip for each.

## How to Run

1. Install the dependency:
   ```
   pip install PyQt5
   ```
2. Run the app:
   ```
   python gym_recommender.py
   ```
3. Select your profile from the dropdowns and click **Get My Workout Plan**.

## Project Structure

```
gym_recommender.py   # Full app: workout database, recommendation algorithm, PyQt5 GUI
```

## Screenshots

<img width="960" height="496" alt="week 1" src="https://github.com/user-attachments/assets/20e0815f-0593-4897-b836-81d3bb750e60" />
<img width="960" height="506" alt="week 1 p2" src="https://github.com/user-attachments/assets/4b579a0b-b24f-4d0a-81e8-ba7514f357b2" />
<img width="1920" height="1023" alt="image" src="https://github.com/user-attachments/assets/6201709c-9110-4faa-8793-0ef8a6371ff1" />

## How AI Was Used

I used Claude to help scaffold the initial project structure, generate the sample workout database, and debug the PyQt5 layout. The recommendation logic (scoring rules for goal/level/equipment/muscle matching) and overall design decisions were reviewed and understood by me before finalizing.

## Author

Zain Ullah Khan
