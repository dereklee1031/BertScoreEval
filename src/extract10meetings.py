import pandas as pd

# List of recording IDs you want to extract transcripts from
recording_ids = [
    
    '9b658e90-8bcd-489b-8cad-d16bfcfc908d',
    'febc3387-bb94-41d1-bed0-0abd1403da0e',
    'a7fe10ea-ef3c-40ec-a8a2-e4107c49d65f',
    'aa3c8df4-a868-4785-ac4e-6681cff60a21',
    'dbfe2a55-0a46-4536-8fbe-14fe4f5e6777',
    '5a9b192a-cd2f-433c-8ad0-ba50ccb6346a',
    '0841b18e-fd73-4c67-8947-04ec1bb3f5d1',
    'bad92662-7853-413b-8238-3c0cdcb80553',
    'f9c5e4d7-e4e8-411f-9b42-404c6960f006',
    'f0327d39-77f4-476a-a854-8db2b5969f6d'
]

# Load the CSV file
csv_file_path = '/Users/dereklee/Desktop/bertscore/data/transcriptions_data.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Filter the DataFrame for the specified recording IDs
filtered_df = df[df['recording_id'].isin(recording_ids)]

# Ensure the data is sorted by recording ID and time
filtered_df = filtered_df.sort_values(by=['recording_id', 'time'])

# Group transcripts by recording ID and combine them into paragraphs
paragraphs = []

for recording_id in recording_ids:
    meeting_transcripts = filtered_df[filtered_df['recording_id'] == recording_id]
    paragraph = " ".join(meeting_transcripts['speech'])
    paragraphs.append([recording_id, paragraph])

# Save the paragraphs to a CSV file
output_csv_file_path = '/Users/dereklee/Desktop/bertscore/data/10meeting.csv'  # Replace with the actual path to save the output
output_df = pd.DataFrame(paragraphs, columns=['recording_id', 'paragraph'])
output_df.to_csv(output_csv_file_path, index=False)

print(f"Paragraphs saved to {output_csv_file_path}")
