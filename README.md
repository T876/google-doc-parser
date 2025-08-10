# Google Doc Parser

A Python program that solves the technical interview challenge of parsing Google Docs containing Unicode characters and their 2D grid positions to reveal secret messages.

## Problem Description

This program retrieves and parses data from a published Google Doc that contains a list of Unicode characters and their positions in a 2D grid. When the characters are arranged according to their coordinates and printed in a fixed-width font, they form a graphic showing uppercase letters that represent a secret message.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Command Line Argument
```bash
python main.py "https://docs.google.com/document/d/YOUR_DOCUMENT_ID/edit"
```

### Method 2: Interactive Input
```bash
python main.py
# Then enter the URL when prompted
```

## How It Works

1. **Document Retrieval**: Converts the Google Doc URL to a plain text export URL and fetches the content
2. **Data Parsing**: Extracts character and coordinate information from the document text
3. **Grid Creation**: Creates a 2D grid and places characters at their specified positions
4. **Display**: Prints the resulting character grid to reveal the secret message

## Key Features

- No authentication required (works with published Google Docs)
- Automatic URL conversion to plain text export format
- Flexible parsing that can be adjusted for different document formats
- Clear step-by-step output showing the process
- Error handling for network issues and invalid URLs

## Notes

- The parsing pattern in `parse_character_data()` may need to be adjusted based on the specific format of your Google Doc
- The coordinate system assumes (0,0) is at the top-left corner
- Empty positions in the grid are filled with space characters
- The program displays the first 500 characters of the retrieved document to help with debugging format issues

## Example Output

```
Google Doc Puzzle Solver
==================================================
Step 1: Retrieving Google Doc content...
Document retrieved successfully. Length: 1234 characters

Step 2: Parsing character data...
Found character '█' at position (0, 0)
Found character '▀' at position (1, 0)
...
Found 15 characters

Step 3: Creating character grid...
Grid dimensions: 4 x 3

Secret Message:
----
█▀▀▀
█▀▀ 
█   
----
```


