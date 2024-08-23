import openai
import pandas as pd
from collections import defaultdict

# Function to split text into smaller chunks that are within the token limit
def split_text_into_chunks(text, max_tokens=3000):
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(sentence.split())
        if current_tokens + sentence_tokens > max_tokens:
            chunks.append(". ".join(current_chunk) + ".")
            current_chunk = [sentence]
            current_tokens = sentence_tokens
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

    if current_chunk:
        chunks.append(". ".join(current_chunk) + ".")

    return chunks

# Function to perform summarization using the GPT-4 chat model directly
def summarize_speech_directly(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following text: {text}"}
        ]
    )
    summary = response['choices'][0]['message']['content']
    return summary

# Load the CSV file into a pandas DataFrame
csv_file_path = '/Users/dereklee/Desktop/bertscore/data/transcriptions_data.csv'
df = pd.read_csv(csv_file_path)

print("Loaded DataFrame:")
print(df.head())

# Get the unique recording IDs for the 10 shortest meetings
recording_ids = df['recording_id'].unique()[:10]


# List to store summaries
summaries = []

# Summarize the first 10 meetings
for i, recording_id in enumerate(recording_ids):
    if i >= 10:  # Limit to the first 10 meetings
        break
    
    # Aggregate all speech for the current recording_id
    speech = " ".join(df[df['recording_id'] == recording_id]['speech'].dropna().astype(str))
    
    try:
        # Split the speech into manageable chunks
        chunks = split_text_into_chunks(speech)
        print(f"Summarizing recording ID: {recording_id} with {len(chunks)} chunks.")
        
        # Summarize each chunk and then combine the summaries
        chunk_summaries = [summarize_speech_directly(chunk) for chunk in chunks]
        combined_summary = " ".join(chunk_summaries)
        
        print(f"Recording ID: {recording_id}\nSummary: {combined_summary}\n")
        summaries.append([recording_id, combined_summary])
    except Exception as e:
        print(f"Error summarizing recording ID {recording_id}: {e}")

# Check if summaries were generated
if len(summaries) == 0:
    print("No summaries were generated. Exiting without saving.")
else:
    print(f"{len(summaries)} summaries were generated.")

    # Print the generated summaries
    print("Generated Summaries:")
    for s in summaries:
        print(s)

    # Attempt to save the summaries to a CSV file
    try:
        output_df = pd.DataFrame(summaries, columns=['recording_id', 'summary'])
        print("DataFrame to be saved:")
        print(output_df.head())
        
        output_csv_file_path = '/Users/dereklee/Desktop/bertscore/data/multiple_summaries_openai.csv'
        output_df.to_csv(output_csv_file_path, index=False)
        print(f"Summaries saved to {output_csv_file_path}")
    except Exception as e:
        print(f"Failed to save summaries to CSV: {e}")










