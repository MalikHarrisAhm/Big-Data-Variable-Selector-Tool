import csv
from openai import OpenAI

#Ensure to update the prompt according to your specific research question and subsequent variable-domains of interest:
def variable_selection(text, client):
    prompt = f"""Reference Variables: {text}

    Task:
    - Decide if any variable is relevant to answering the following research question: [INSERT RESEARCH QUESTION HERE]?
     - If more than zero variables are selected, determine its category out of the following: [INSERT YOUR CATEGORIES E.G.: Demographic, Biomarkers, etc.].
    - Write a very short justification for the inclusion or exclusion of a variable.

    Formatting Criteria:
    - Construct a table with five columns: "Variable", "Path", "Decision", "Category" and "Reason".
    - Each row of the "Variable" column should contain verbatim the variable name provided.
    - Each row of the "Path" column should contain verbatim the path name provided.
    - Each row of the "Decision" column should state either "Include" or "Exclude".
    - Each row of the "Category" column should state "N/A" if the decision is "Exclude". If the decision is "Include", it should state the category verbatim as one of the following: [INSERT YOUR CATEGORIES E.G.: Demographic, Biomarkers, etc.].
    - Each row of the "Reason" column should state very short justification statement for the choice of either "Include" or "Exclude".
    - Only write out the requested, not any other words or sentence.
    - The last variable curly-bracket should have a comma at the end.

    Example output:
    {{"Variable":"Sex", "Path":"Population characteristics > Baseline characteristics", "Decision":"Include", "Category":"Demographic", "Reason”:”Sex has a significant impact on biological responses and the modulation of internal metabolic and hormonal pathways.”}},
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(model="gpt-4",  # Replace with appropriate GPT-4 engine ID
    messages=messages,
    max_tokens=5000)

    # Parse the GPT-4 output into Anki cards
    cards_text = response.choices[0].message.content
    return cards_text
  
def read_csv_and_split_into_chunks(file_path, chunk_size=20):
    """
    Reads a CSV file, converts each row (first four columns only) into a string,
    and groups these strings into chunks. Each chunk is a single string where rows are separated by newlines.

    :param file_path: Path to the CSV file.
    :param chunk_size: Number of rows in each chunk.
    :return: A list of strings, each string represents a chunk of rows.
    """
    chunks = []  # List to hold all chunks
    current_chunk = []  # Temporary list to hold rows of the current chunk

    # Open the CSV file
    with open(file_path, mode='r', encoding='utf-8') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Iterate over rows in the CSV file
        for row in csv_reader:
            # Slice the row to include only the first four columns
            row_slice = row[:4]
            # Convert the sliced row to a string
            row_string = ','.join(row_slice)
            # Append the row string to the current chunk
            current_chunk.append(row_string)

            # Check if the current chunk is full
            if len(current_chunk) == chunk_size:
                # Join the rows in the current chunk with a newline character
                chunk_string = '\n'.join(current_chunk)
                # Append the chunk string to the list of chunks
                chunks.append(chunk_string)
                # Start a new chunk
                current_chunk = []

    # Add any remaining rows as the last chunk
    if current_chunk:
        chunk_string = '\n'.join(current_chunk)
        chunks.append(chunk_string)

    return chunks
def append_string_to_file(filename: str, data_string: str):
    """
    Appends a string to the end of a text file.

    :param filename: Path to the text file.
    :param data_string: The string to append.
    """
    with open(filename, 'a') as file:
        file.write(data_string + '\n')

def variable_selection_to_txt(chunk, api_key):


    # Initialize OpenAI client with the current API key
    client = OpenAI(api_key=api_key)

    try:
        # Process the chunk
        variable_selection_string = variable_selection(chunk, client)
    except Exception as e:
        print(f"An error occurred while processing the chunk: {e}")
        raise

    return variable_selection_string

data_path = "Data_Dictionary_Showcase.csv"
txt_filename = "variable_selection_output.txt"
api_key = "YOUR_API_KEY"
chunks = read_csv_and_split_into_chunks(data_path)
# print(chunks[4])
# Iterate over each chunk and process it
print("Total Chunks: " + str(len(chunks)))
current_chunk = 0
for chunk in chunks:
    print("Current Chunk: " + str(current_chunk))
    try:
        variable_selection_string = variable_selection_to_txt(chunk, api_key)
        # print(variable_selection_string)
        append_string_to_file(txt_filename, variable_selection_string)
        current_chunk += 1
    except Exception as e:
        print(f"An error occurred: {e}")
        # break
