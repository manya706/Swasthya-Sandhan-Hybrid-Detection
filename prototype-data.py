import csv
import random

# List of predictions
predictions = [
    'Acne, or Rosacea',
    'Actinic Keratosis, or other Malignant Lesions',
    'Alopecia, or other Hair Diseases',
    'Atopic Dermatitis',
    'Bacterial Infections',
    'Benign Tumors',
    'Bullous Disease',
    'Connective Tissue Diseases',
    'Eczema',
    'Exanthems, or Drug Eruptions',
    'Fungal Infections',
    'Healthy or Benign growth',
    'Herpes, HPV, other STDs',
    'Lyme Diseasem, Infestations and Bites',
    'Melanoma Skin Cancer Nevi and Moles',
    'Nail Fungus or other Nail Disease',
    'Poison Ivy or Contact Dermatitis',
    'Psoriasis, Lichen Planus or related diseases',
    'Systemic Disease',
    'Urticaria Hives',
    'Vascular Tumors',
    'Vasculitis Photos',
    'Warts, or other Viral Infections'
]

# List of Indian pin codes
pin_codes = ['110001', '400001', '560001', '600001', '700001', '800001', '110002', '400002', '560002', '600002','201010','201013']

# Generate 60 rows of fake data
rows = []
for _ in range(60):
    total_time = round(random.uniform(10, 500), 2)  # Random total time in milliseconds
    pincode = random.choice(pin_codes)  # Random Indian pin code
    num_diseases = random.randint(1, 10)  # Random number of diseases (up to 5)
    diseases = random.sample(predictions, num_diseases)  # Random diseases from the list
    confidence = random.uniform(93.322, 100) # Random confidence values
    # Append to the rows
    for disease in diseases:
        rows.append([total_time, pincode, disease,confidence])

# Write to CSV
with open('Backend\predictions.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Total Time (ms)', 'Pincode', 'Prediction', 'Confidence'])
    writer.writerows(rows)

# This modified version will randomly assign a variable number of diseases to each pincode, up to a maximum of 5 diseases.






