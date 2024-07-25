# -*- coding: utf-8 -*-
"""moral_foundations-Llama.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_Qz7kcEptJECJH0tzcP7VMEs9_7UgRXW
"""

!pip install openai anthropic requests

!pip install transformers

!huggingface-cli login

meta_api_key = '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'

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

import requests
import re
import time

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def ask_meta(statements, country):
    # Helper function to create a prompt from a list of statements
    def create_prompt(statements_chunk):
        prompt = f''' <s>[INST] <<SYS>>
For the statement below, please indicate how well each statement describes the average person from {country}. Response options: Option 1. Does not describe the average person at all ; Option 2. slightly describes the average person; Option 3. moderately describes the average person; Option 4. describes the average person fairly well; Option 5. describes the average person extremely well. Please select the options that best describes the country {country} and answer only using a single whole number from the given options, answer the question with no words.

example:
User:
1. Statement 1
2. Statement 2


Assistant:

1. 5
2. 2

<</SYS>>

User:
'''
        statement_count = 1
        for statement in statements_chunk:
            prompt += f"{statement_count}. {statement}\n"
        prompt += "Assistant: \n [/INST]"
        return prompt

    # Flatten the statements dictionary into a list
    all_statements = [statement for statement_list in statements.values() for statement in statement_list]

    # Process statements in chunks of 12
    chunk_size = 1
    def get_responses():
      all_responses = []

      for i in range(0, len(all_statements), chunk_size):
          chunk = all_statements[i:i + chunk_size]
          chunk_responses = []
          while len(chunk_responses) != chunk_size:
            time.sleep(3)

            prompt = create_prompt(chunk)
            # print(prompt)
            try:
              response = query({"inputs": prompt, "temperature": 100.0})
              print(response)
              generated_text = response[0]["generated_text"]

              # Extract the responses
              pattern = re.compile(r'\[\/INST\]\s*(.*)', re.DOTALL)
              match = pattern.search(generated_text)
              if match:
                  digits_section = match.group(1).strip()
                  if digits_section.isdigit():
                    chunk_responses = [int(digits_section)]
                  elif re.findall(r'\d+\.\s*(\d+)', digits_section):
                    chunk_responses = re.findall(r'\d+\.\s*(\d+)', digits_section)
                  else:
                    chunk_responses = re.findall(r'Assistant:\s*(\d+)', digits_section)
                  chunk_responses = [int(response) for response in chunk_responses]
              if len(chunk_responses) != chunk_size:
                  print(f"Expected {chunk_size} responses, but got {len(chunk_responses)}. Retrying...")
                  chunk_responses = ['na']
                  time.sleep(5)
            except:
              chunk_responses = ['na']

          all_responses.extend(chunk_responses)

      return all_responses

    all_results = []
    for _ in range(10):
        responses = get_responses()
        if len(responses) == 36:
            all_results.append(responses)
            print(all_results)
        else:
            print(f"Expected 36 responses, but got {len(responses)}. Retrying...")

    return all_results

import csv
import os

def csv_file_exists(filename):
    return os.path.exists(filename)

def save_responses_to_csv(statements, country, all_responses, csv_filename):
    # Flatten the statements dictionary into a list
    flat_statements = [(category, statement) for category, statement_list in statements.items() for statement in statement_list]

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

    # Open the CSV file in append mode
    with open(csv_filename, 'a', newline='') as csvfile:
        fieldnames = ['country', 'category', 'statement'] + [f'llama_{i}' for i in range(1, 11)]  # Adjust for 10 OpenAI responses
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if the file is empty
        if not csv_exists:
            writer.writeheader()

        # Write new responses to the CSV file
        for i, (category, statement) in enumerate(flat_statements):
            # Create a dictionary for each row
            row = {
                'country': country,
                'category': category,
                'statement': statement
            }
            for j in range(10):  # 10 sets of responses
                row[f'llama_{j + 1}'] = all_responses[j][i]

            # Check if the row already exists
            if (country, category, statement) not in existing_results:
                writer.writerow(row)

# country = "Congo"
# responses  # This should be the list of lists with 10 sets of responses
csv_filename = "llama_singleitem1.csv"

for i in countries:
  responses = ask_meta(statements, i)
  save_responses_to_csv(statements, i, responses, csv_filename)