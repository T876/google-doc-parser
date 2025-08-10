# Google Docs API Setup Instructions

To use this program with the Google Docs API, you need to set up authentication. Follow these steps:

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select an existing project
3. Give your project a name (e.g., "Google Doc Parser")

## Step 2: Enable the Google Docs API

1. In your project, go to "APIs & Services" > "Library"
2. Search for "Google Docs API"
3. Click on it and press "Enable"

## Step 3: Create Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields (App name, User support email, Developer contact)
   - Add your email to "Test users" section
4. For Application type, choose "Desktop application"
5. Give it a name (e.g., "Google Doc Parser")
6. Click "Create"

## Step 4: Download Credentials

1. After creating the OAuth client, click the download button (⬇️)
2. Save the downloaded file as `credentials.json` in the same directory as `main.py`

## Step 5: Install Dependencies

```bash
pip3 install -r requirements.txt
```

## Step 6: Run the Program

```bash
python3 main.py
```

## First Run Authentication

The first time you run the program:

1. It will open a web browser for authentication
2. Sign in with your Google account
3. Grant permission to read Google Docs
4. The program will save a `token.json` file for future runs

## File Structure

After setup, your directory should look like:
```
google-doc-parser/
├── main.py
├── requirements.txt
├── credentials.json  (your downloaded OAuth credentials)
├── token.json        (created after first authentication)
└── setup_instructions.md
```

## Troubleshooting

- **"credentials.json not found"**: Make sure you downloaded the OAuth credentials and named the file exactly `credentials.json`
- **Permission errors**: Make sure the Google Doc is accessible to your Google account
- **API not enabled**: Double-check that the Google Docs API is enabled in your project

## Security Note

- Keep `credentials.json` and `token.json` private
- Don't commit these files to version control
- The OAuth credentials are tied to your Google Cloud project
