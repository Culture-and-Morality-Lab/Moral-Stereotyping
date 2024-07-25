# -*- coding: utf-8 -*-
"""moral_foundations-Gemini.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DLIAAqyRyuo90WFKuHwpdIShaD1lWgwv
"""

!pip install openai anthropic requests

google_api_key = 'AIzaSyDc2xTSyN-dFPbzGFiojqeTAkBrImDbkO4'

client = OpenAI(
    api_key=openai_api_key
)

# Configure Google Gemini Pro
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-pro')

# List of countries and statements
countries = ["Argentina", "Belgium", "Chile", "Colombia", "Egypt", "France", "Ireland", "Japan", "Kenya", "Mexico", "Morocco", "New Zealand", "Nigeria", "Peru", "Russia", "Saudi Arabia", "South Africa", "Switzerland", "UAE", "Ghana", "Germany", "Italy", "Netherlands", "Spain", "UK", "Australia", "Canada", "USA", "Brazil", "South Korea", "Norway", "Sweden", "Iran", "India", "China", "Namibia", "Congo", "Turkey", "Poland"]


statements = {
    "Caring": [
        "Caring for people who have suffered is an important virtue.",
        "I believe that compassion for those who are suffering is one of the most crucial virtues.",
        "We should all care for people who are in emotional pain.",
        "I am empathetic toward those people who have suffered in their lives.",
        "Everyone should try to comfort people who are going through something hard.",
        "It pains me when I see someone ignoring the needs of another human being."
    ],
    "Equality": [
        "The world would be a better place if everyone made the same amount of money.",
        "Our society would have fewer problems if people had the same income.",
        "I believe that everyone should be given the same quantity of resources in life.",
        "I believe it would be ideal if everyone in society wound up with roughly the same amount of money.",
        "When people work together toward a common goal, they should share the rewards equally, even if some worked harder on it.",
        "I get upset when some people have a lot more money than others in my country."
    ],
    "Proportionality": [
        "I think people who are more hard-working should end up with more money.",
        "I think people should be rewarded in proportion to what they contribute.",
        "The effort a worker puts into a job ought to be reflected in the size of a raise they receive.",
        "It makes me happy when people are recognized on their merits.",
        "In a fair society, those who work hard should live with higher standards of living.",
        "I feel good when I see cheaters get caught and punished."
    ],
    "Loyalty": [
        "I think children should be taught to be loyal to their country.",
        "It upsets me when people have no loyalty to their country.",
        "Everyone should love their own community.",
        "Everyone should defend their country, if called upon.",
        "Everyone should feel proud when a person in their community wins in an international competition.",
        "I believe the strength of a sports team comes from the loyalty of its members to each other."
    ],
    "Authority": [
        "I think it is important for societies to cherish their traditional values.",
        "I feel that most traditions serve a valuable function in keeping society orderly.",
        "I think obedience to parents is an important virtue.",
        "We all need to learn from our elders.",
        "I believe that one of the most important values to teach children is to have respect for authority.",
        "I think having a strong leader is good for society."
    ],
    "Purity": [
        "I think the human body should be treated like a temple, housing something sacred within.",
        "I believe chastity is an important virtue.",
        "It upsets me when people use foul language like it is nothing.",
        "If I found out that an acquaintance had an unusual but harmless sexual fetish I would feel uneasy about them.",
        "People should try to use natural medicines rather than chemically identical human-made ones.",
        "I admire people who keep their virginity until marriage."
    ]
}

# Collecting responses for each country and statement
results = []

from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir("/content/drive/MyDrive/moral_foundations")
print("Current Directory:", os.getcwd())

#itembyitem

def ask_google(statement, country):
    prompt = f'For the statement below, please indicate how well the statement describes the average person from {country}. Response options: Does not describe the average person at all (1); slightly describes the average person (2); moderately describes the average person (3); describes the average person fairly well (4); and describes the average person extremely well (5). Please answer only using a single number, with no words.\n\n'
    prompt += f" {statement}\n"
    # print(prompt)

    response = model.generate_content(prompt,
        generation_config=genai.types.GenerationConfig(
        temperature=2.0))
    extracted_response = response.text.lower().strip()

    return extracted_response

import os
import csv
import time

csv_filename = 'responses_openapi10.csv'
csv_exists = os.path.exists(csv_filename)
csv_path = os.path.abspath(csv_filename)

if csv_exists:
    print(f"File {csv_filename} exists at {csv_path}")
else:
    print(f"File {csv_filename} does not exist.")

processed_set = set()  # Initialize an empty set to store processed statement-country pairs

if os.path.exists('processed_responses.txt'):
    with open('processed_responses.txt', 'r') as f:
        for line in f:
            statement_country = line.strip()
            processed_set.add(statement_country)

with open('responses_openapi10.csv', 'r', newline='') as csvfile, open('processed_responses.txt', 'a') as processed_file:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames

    with open('newgemini_responses10.csv', 'a', newline='') as newcsvfile:
        writer = csv.DictWriter(newcsvfile, fieldnames=fieldnames)

        # Write the header if the file is empty
        if os.path.getsize('newgemini_responses10.csv') == 0:
            writer.writeheader()

        for row in reader:
            country = row['country']
            category = row['category']
            statement = row['statement']

            statement_country = f"{statement}-{country}"
            if statement_country in processed_set:
                print(f"Skipping already processed statement: {statement}, country: {country}")
                continue

            try:
                gemini_responses = []
                for i in range(10):
                    time.sleep(4)  # Delay between API calls
                    gemini_response = ask_google(statement, country)
                    gemini_responses.append(gemini_response)

                # Record the processed statement-country pair
                processed_file.write(statement_country + '\n')
                processed_set.add(statement_country)  # Update the set

            except Exception as e:
                print(f"Error with Gemini API for statement: {statement}, country: {country} - {e}")
                gemini_responses = ["na"] * 10
                processed_file.write(statement_country + '\n')  # Record the processed statement-country pair
                processed_set.add(statement_country)  # Update the set

            # Write the row with the Gemini responses
            row.update({f'openai_{i+1}': response for i, response in enumerate(gemini_responses)})
            writer.writerow(row)

print("New responses collected and saved to newgemini_responses10.csv")

#Together

def ask_google(statements, country):
    prompt = f'For each of the statements below, please indicate how well each statement describes the average person from {country}. Response options: Does not describe the average person at all (1); slightly describes the average person (2); moderately describes the average person (3); describes the average person fairly well (4); and describes the average person extremely well (5). Please answer only using a single number, with no words.\n\n'
    for category, statement_list in statements.items():
      for i, statement in enumerate(statement_list, start=1):
          prompt += f"{i}. {statement}\n"
    all_responses = []
    print(prompt)
    while len(all_responses) < 2:
      try:
          time.sleep(6)
          response = model.generate_content(prompt,
        generation_config=genai.types.GenerationConfig(
        temperature=2.0))
          extracted_response = [
              resp.split('.')[1].strip()
              for resp in response.text.strip().split('\n')
              if len(resp.split('.')) > 1 and resp.split('.')[1].strip().isdigit()
          ]

          if len(extracted_response) == 3:
              all_responses.append(extracted_response)
              print(f"Collected {len(all_responses)} out of 10 responses")
          else:
              print(f"Incomplete response received: {extracted_response}, retrying...")

      except Exception as e:
          print(f"Error occurred: {e}, retrying...")

    return all_responses

csv_filename = 'testinggemini.csv'

# Function to check if CSV file exists
def csv_file_exists(filename):
    return os.path.exists(filename)

# Check if CSV file exists
csv_exists = csv_file_exists(csv_filename)
csv_path = os.path.abspath(csv_filename)

if csv_exists:
    print(f"File {csv_filename} exists at {csv_path}")
else:
    print(f"File {csv_filename} does not exist.")

# Initialize set for existing results
existing_results = set()

# If CSV file exists, read existing results
if csv_exists:
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            existing_results.add((row['country'], row['category'], row['statement']))

# Open the CSV file in read mode and create a list of dictionaries for existing rows
existing_rows = []
if csv_exists:
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            existing_rows.append(dict(row))

# Open the CSV file in append mode
with open(csv_filename, 'a', newline='') as csvfile:
    fieldnames = ['country', 'category', 'statement'] + [f'gemini_{i}' for i in range(1, 11)]  # Adjust for 10 OpenAI responses
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header if the file is empty
    if not csv_exists:
        writer.writeheader()

    # Loop through each country and process statements
    for country in countries:
        to_process = [
            (country, category, statement)
            for category, statements_list in statements.items()
            for statement in statements_list
            if (country, category, statement) not in existing_results
        ]

        # Skip processing if no statements to process
        if not to_process:
            continue


        # Get 10 lists of responses for the country
        google_responses = ask_google(statements, country)
        print(google_responses)
        print(country)
        if len(google_responses) != len(to_process) or any(len(resp) != 10 for resp in google_responses):
            raise ValueError("Unexpected response format from Google API")

        # Prepare results to write to CSV
        for (country, category, statement), google_response in zip(to_process, google_responses):
            # Check if the row exists in existing_rows
            existing_row_index = next((index for index, row in enumerate(existing_rows) if row['country'] == country and row['category'] == category and row['statement'] == statement), None)

            if existing_row_index is not None:
                # Update existing row with new google_response
                for i in range(10):
                    existing_rows[existing_row_index][f'gemini_{i+1}'] = google_response[i]
            else:
                # Create a new result dictionary
                result = {
                    'country': country,
                    'category': category,
                    'statement': statement,
                }
                for i in range(10):
                    result[f'gemini_{i+1}'] = google_response[i]

                existing_rows.append(result)
        writer.writerows(existing_rows)
        csvfile.flush()  # Ensure data is written to the file immediately
        existing_rows = []  # Clear existing_rows after writing


print("Responses collected and saved to testinggemini.csv")