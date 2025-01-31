# Extract information from articles downloaded directly from Nexus Uni database
# Store in form of JSON
# Change directory under tag: "SUBJECT TO CHANGE"

import json
import os
import glob
# library to read in DOCX, library full name: python-docx
import docx

# code to extract word files
def get_word_files(directory):
    # Change the directory to the specified path
    os.chdir(directory)
    # Use glob to find all .docx files in the directory
    word_files = glob.glob("*.DOCX")
    return word_files

# code to read the content of a word (.DOCX) file
def read_word_file(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

# code to extract structured data from content
def extract_article_info(content):
    # Split the content by newline characters
    parts = content.split('\n')
    
    # Filter out empty parts
    parts = [part for part in parts if part.strip()]

    # could be two formats:
    # format 1: title -> source -> date
    # format 2: title -> "Newstex Blogs" -> source -> date
    # Extract title, source, and date based on the structure
    article_info = {
        # title must be on the first line
        "title": parts[0] if len(parts) > 0 else "Unknown",
        "source": "Unknown",
        "date": "Unknown",
        "byline": "Unknown", # Specific Author
        "content": "None",
    }

    # Determine the format and extract source and date
    if len(parts) > 2 and "Newstex Blogs" in parts[1]:
        article_info["source"] = parts[2] if len(parts) > 2 else "Unknown"
        article_info["date"] = parts[3] if len(parts) > 3 else "Unknown"
    else:
        article_info["source"] = parts[1] if len(parts) > 1 else "Unknown"
        article_info["date"] = parts[2] if len(parts) > 2 else "Unknown"

    # Extract byline and body content
    for i, part in enumerate(parts):
        # Some articles may not have a Byline
        if part.startswith("Byline:"):
            article_info["byline"] = part.replace("Byline:", "").strip()
        # All articles have a article body
        elif part == "Body":
            body_content = "\n".join(parts[i + 1:])
            # Find the "Load-Date" line and trim the content behind it
            load_date_index = body_content.find("\nLoad-Date:")
            if load_date_index != -1:
                body_content = body_content[:load_date_index]
            # Remove leading and ending spaces
            article_info["content"] = body_content.strip()

    return article_info

# Specify the directory path
# This is where the articles/data are physically saved
directory_path = '../Data/pre-analyze/nexus_uni/Test' # SUBJECT TO CHANGE

# list used to store all post-process information
articles_info = []

# Get the list of Word files
word_files = get_word_files(directory_path)

# Process each word document, accessed by file name
for file_name in word_files:
    # read the content of the word file given file name
    content = read_word_file(file_name)

    # remove the .DOCX extension, not needed anymore
    #if file_name.endswith(".DOCX"):
    #    file_name = file_name[:-5]

    # construct Json data point
    # extract information from parsed DOCX text
    article_info = extract_article_info(content)

    articles_info.append(article_info)
    print("finished processing through article:", file_name)

# Change directory back to root
# We are currently in the parser code directory
os.chdir('../../../../') # SUBJECT TO CHANGE
# store the JSON data to the JSON file
# Define the directory and file path
# This is where the JSON file will be saved
data_dir = "Data/pre-analyze/newspaper" # SUBJECT TO CHANGE
file_path = os.path.join(data_dir, "DataPool.json")

# format json data
json_data = {
    "status": "ok",
    "totalResults": len(articles_info),
    "articles": articles_info
}

# Format the JSON data with indentation for better readability
formatted_json = json.dumps(json_data, indent=4)
# Save data to a JSON file in the specified directory
with open(file_path, 'w') as json_file:
    json_file.write(formatted_json)

print(f"Data saved to {file_path}")