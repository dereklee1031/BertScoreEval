import csv
from google.cloud import firestore
import google.auth

credentials, project_id = google.auth.load_credentials_from_file('configs/gcloud_service_credentials.json') 

# Initialize Firestore client
db = firestore.Client(credentials=credentials, project=project_id)

# Reference to the 'transcriptions' collection
collection_ref = db.collection('transcriptions')

# Get 5 documents from the collection
docs = collection_ref.stream()

# Convert documents to a list of dictionaries
data = []
for doc in docs:
    doc_data = doc.to_dict()
    doc_data['id'] = doc.id  # Optionally include document ID
    data.append(doc_data)

# Function to write data to CSV
def write_to_csv(data, csv_file_name):
    if not data:
        print("No data to write.")
        return

    # Extract fieldnames from the first document
    fieldnames = data[0].keys()

    # Write to CSV
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write the header
        writer.writerows(data)  # Write the data

    print(f"Data has been written to {csv_file_name}")

# Specify the CSV file name
csv_file_name = 'transcriptions_data.csv'

# Write data to CSV
write_to_csv(data, csv_file_name)
