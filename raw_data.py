import pandas as pd
import numpy as np

# ==========================================
# STEP 1: GENERATE RAW & MESSY DATASET
# ==========================================
np.random.seed(42)

students = ['STU001', 'STU002', 'STU003', 'STU004', 'STU005']
date_range = pd.date_range(start='2026-01-01', end='2026-12-31')

data = []
record_num = 1

for student in students:
    for date in date_range:
        if student in ['STU001', 'STU004']:
            attended = np.random.randint(40, 49)
            study_hrs = round(np.random.uniform(4.5, 6.0), 1)
            screen_hrs = round(np.random.uniform(3.0, 4.5), 1)
            sleep_hrs = round(np.random.uniform(7.0, 8.5), 1)
            pattern = 'Stable Routine'
        elif student in ['STU003', 'STU005']:
            attended = np.random.randint(20, 32)
            study_hrs = round(np.random.uniform(2.5, 4.0), 1)
            screen_hrs = round(np.random.uniform(5.5, 7.5), 1)
            sleep_hrs = round(np.random.uniform(5.5, 6.8), 1)
            pattern = 'Moderate Stress'
        else:
            attended = np.random.randint(2, 9)
            study_hrs = round(np.random.uniform(1.0, 2.0), 1)
            screen_hrs = round(np.random.uniform(8.0, 10.0), 1)
            sleep_hrs = round(np.random.uniform(4.0, 5.2), 1)
            pattern = 'Risky / Unusual Routine'

        scheduled = 50
        attendance_pct = round((attended / scheduled) * 100, 1)
        assignments = np.random.randint(0, 3) if pattern != 'Risky / Unusual Routine' else 0
        exercise = np.random.choice([30, 45, 60, 90]) if pattern == 'Stable Routine' else np.random.choice([5, 10, 15])
        late_night = round(np.random.uniform(0.2, 0.8), 1) if pattern == 'Stable Routine' else (round(np.random.uniform(1.2, 2.2), 1) if pattern == 'Moderate Stress' else round(np.random.uniform(2.8, 4.0), 1))
        routine_score = round(np.random.uniform(0.05, 0.3), 2) if pattern == 'Stable Routine' else (round(np.random.uniform(0.4, 0.7), 2) if pattern == 'Moderate Stress' else round(np.random.uniform(0.75, 0.98), 2))

        if np.random.rand() < 0.08:
            study_hrs = np.nan
        if np.random.rand() < 0.07:
            sleep_hrs = np.nan
        if np.random.rand() < 0.06:
            screen_hrs = np.nan

        data.append({
            'Record_ID': f"R{record_num:05d}",
            'Student_ID': student,
            'Date': date.strftime('%d-%m-%Y'),
            'Study_Hours': study_hrs,
            'Screen_Time_Hours': screen_hrs,
            'Sleep_Hours': sleep_hrs,
            'Assignment_Count': assignments,
            'Exercise_Minutes': exercise,
            'Classes_Attended': attended,
            'Classes_Scheduled': scheduled,
            'Attendance_Percent': attendance_pct,
            'Late_Night_Screen_Hours': late_night,
            'Routine_Change_Score': routine_score,
            'Behavior_Pattern': pattern
        })
        record_num += 1

df_raw = pd.DataFrame(data)
df_raw.to_csv('Silent_Signals_Raw_Messy.csv', index=False)


# ==========================================
# STEP 2: LOAD & EXECUTE STEP-BY-STEP PIPELINE
# ==========================================

df = pd.read_csv('Silent_Signals_Raw_Messy.csv')

# --- Step 1: Initial Dataset Info ---
print("--- Step 1: Initial Dataset Info ---")
print(f"Total Rows & Columns: {df.shape}\n")


# --- Step 2: Missing Values Check ---
print("--- Step 2: Missing Values Check ---")
print(df.isnull().sum())
print()


# --- Step 3: Missing Values Correction (Imputation) ---
df['Study_Hours'] = df['Study_Hours'].fillna(df['Study_Hours'].median())
df['Screen_Time_Hours'] = df['Screen_Time_Hours'].fillna(df['Screen_Time_Hours'].median())
df['Sleep_Hours'] = df['Sleep_Hours'].fillna(df['Sleep_Hours'].median())

print("--- Step 3: Missing Values Corrected ---")
print("Missing values after median imputation:")
print(df[['Study_Hours', 'Screen_Time_Hours', 'Sleep_Hours']].isnull().sum())
print()


# --- Step 4: Custom Encoding (Stable: 0, Moderate: 1, Risky: 2) ---
encoding_mapping = {
    'Stable Routine': 0,
    'Moderate Stress': 1,
    'Risky / Unusual Routine': 2
}
df['Behavior_Pattern_Encoded'] = df['Behavior_Pattern'].map(encoding_mapping)

print("--- Step 4: Encoding Performed ---")
# Har category ka ek sample dikhane ke liye drop_duplicates use kiya hai
print(df[['Behavior_Pattern', 'Behavior_Pattern_Encoded']].drop_duplicates().reset_index(drop=True))
print()


# --- Step 5: Decoding Verification ---
decoding_mapping = {v: k for k, v in encoding_mapping.items()}
df['Behavior_Pattern_Decoded'] = df['Behavior_Pattern_Encoded'].map(decoding_mapping)

print("--- Step 5: Decoding Performed ---")
print(df[['Behavior_Pattern_Encoded', 'Behavior_Pattern_Decoded']].drop_duplicates().reset_index(drop=True))
print()

# --- Step 6: Filtration Operations ---
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
reference_date = df['Date'].max()

risky_filtered = df[df['Behavior_Pattern_Decoded'] == 'Risky / Unusual Routine']
stu001_filtered = df[df['Student_ID'] == 'STU001']

print("--- Step 6: Filtration Performed ---")
print(f"Total records matching 'Risky / Unusual Routine': {len(risky_filtered)}")
print(f"Total records for 'STU001': {len(stu001_filtered)}")
print()


# --- Step 7: Time-based Range Filtration ---
last_3_days = df[df['Date'] >= (reference_date - pd.Timedelta(days=3))]
last_1_week = df[df['Date'] >= (reference_date - pd.Timedelta(weeks=1))]
last_1_month = df[df['Date'] >= (reference_date - pd.DateOffset(months=1))]
last_6_months = df[df['Date'] >= (reference_date - pd.DateOffset(months=6))]

print("--- Step 7: Time-based Filtration (Days / Weeks / Months) ---")
print(f"Records in Last 3 Days: {len(last_3_days)}")
print(f"Records in Last 1 Week: {len(last_1_week)}")
print(f"Records in Last 1 Month: {len(last_1_month)}")
print(f"Records in Last 6 Months: {len(last_6_months)}")

df.to_csv('Silent_Signals_Cleaned_Processed.csv', index=False)