import numpy as np
import joblib


svm_model = joblib.load("svm_heart_disease_model.pkl")
scaler = joblib.load("scaler.pkl")


feature_names = [
    "Age", "Sex", "Chest pain type", "Cholesterol", "EKG results",
    "Max HR", "Exercise angina", "ST depression", "Slope of ST",
    "Number of vessels fluro", "Thallium"
]

feature_ranges = {
    "Age": (0, 120),
    "Sex": (0, 1),
    "Chest pain type": (0, 4),
    "Cholesterol": (0, 400),
    "EKG results": (0, 2),
    "Max HR": (0, 250),
    "Exercise angina": (0, 1),
    "ST depression": (0, 10),
    "Slope of ST": (0, 3),
    "Number of vessels fluro": (0, 3),
    "Thallium": (0, 7)
}

print("=" * 70)
print("HEART DISEASE PREDICTION SYSTEM")
print("=" * 70)
print("\nFeature Information:")
print("-" * 70)
for feature, (min_val, max_val) in feature_ranges.items():
    print(f"{feature:25s} | Range: {min_val:6.1f} - {max_val:6.1f}")

print("\n" + "=" * 70)
print("Please enter patient information:")
print("=" * 70)

user_input = {}


feature_guidance = {
    "Age": "Patient age in years",
    "Sex": "Sex (0=Female, 1=Male)",
    "Chest pain type": "Type of chest pain (0-4)",
    "Cholesterol": "Serum cholesterol in mg/dl",
    "EKG results": "EKG results (0-2)",
    "Max HR": "Maximum heart rate achieved",
    "Exercise angina": "Exercise induced angina (0=No, 1=Yes)",
    "ST depression": "ST depression induced by exercise",
    "Slope of ST": "Slope of ST segment (0-2)",
    "Number of vessels fluro": "Number of major vessels (0-3)",
    "Thallium": "Thallium test result (0-7)"
}

# Get user inputs
for feature in feature_names:
    while True:
        min_val, max_val = feature_ranges[feature]
        
        print(f"\n{feature}")
        print(f"  Description: {feature_guidance.get(feature, '')}")
        
        try:
            value = float(input(f"  Enter value: "))
            
            # Validate input
            if value < min_val or value > max_val:
                print(f"  ⚠️  Value out of range! Please enter a value between {min_val:.1f} and {max_val:.1f}")
                continue
            
            user_input[feature] = value
            break
        except ValueError:
            print(f"  ⚠️  Invalid input! Please enter a numeric value.")


input_data = np.array([user_input[feature] for feature in feature_names]).reshape(1, -1)
input_data_scaled = scaler.transform(input_data)


prediction = svm_model.predict(input_data_scaled)[0]
prediction_prob = svm_model.decision_function(input_data_scaled)[0]

print("\n" + "=" * 70)
print("PREDICTION RESULT")
print("=" * 70)

if prediction == 1:
    result_text = "⚠️  HEART DISEASE DETECTED"
else:
    result_text = "✓ NO HEART DISEASE DETECTED"

print(f"\n{result_text}")
print(f"\nConfidence Score: {abs(prediction_prob):.4f}")
print("\n" + "=" * 70)
print("Note: This prediction is based on the SVM model trained on the dataset.")
print("Please consult a medical professional for accurate diagnosis.")
print("=" * 70)
