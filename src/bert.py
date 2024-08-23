import pandas as pd
from bert_score import score

# Load the CSV files containing GPT-generated summaries and human-written summaries
gpt_summaries_file = '/Users/dereklee/Desktop/bertscore/data/multiple_summaries_openai.csv'  # Replace with your actual file path
human_summaries_file = '/Users/dereklee/Desktop/bertscore/data/human-written_summaries.csv'  # Replace with your actual file path

# Load the GPT-generated summaries
gpt_df = pd.read_csv(gpt_summaries_file)
gpt_summaries = gpt_df['summary'].tolist()

# Load the human-written summaries
human_df = pd.read_csv(human_summaries_file)
human_summaries = human_df['Summary'].tolist()

# Ensure that the lists of summaries are aligned and have the same length
if len(gpt_summaries) != len(human_summaries):
    raise ValueError("The number of GPT summaries and human summaries must be the same.")

# Compute BERTScore for each pair of summaries
P, R, F1 = score(gpt_summaries, human_summaries, lang="en", verbose=True)

# Create a DataFrame to store the BERTScore results
results_df = pd.DataFrame({
    'recording_id': gpt_df['recording_id'],  # Assuming the 'recording_id' is present in the GPT summaries file
    'gpt_summary': gpt_summaries,
    'human_summary': human_summaries,
    'precision': P.tolist(),
    'recall': R.tolist(),
    'f1': F1.tolist(),
})
# Calculate the mean of each metric
mean_precision = results_df['precision'].mean()
mean_recall = results_df['recall'].mean()
mean_f1 = results_df['f1'].mean()

# Create a row with the mean values
mean_row = pd.DataFrame({
    'recording_id': [''],
    'gpt_summary': [''],
    'human_summary': [''],
    'precision': [mean_precision],
    'recall': [mean_recall],
    'f1': [mean_f1],
})
results_df = pd.concat([results_df, mean_row], ignore_index=True)

# Save the results to a CSV file
output_file_path = '/Users/dereklee/Desktop/bertscore/data/bert_score_results.csv'  # Replace with your desired output path
results_df.to_csv(output_file_path, index=False)

print(f"BERTScore results saved to {output_file_path}")
