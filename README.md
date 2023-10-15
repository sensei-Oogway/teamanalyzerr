# Team Analyzer

This project combines an Atlassian Connect app and a Django backend to provide team analytics in JIRA.

## Overview

This repository contains an Atlassian Connect app (Teamanalyzer) built using the Express.js framework. This app is designed to extend and integrate with Atlassian products such as Jira, Confluence, and Bitbucket.

## Features

- Easily extend and customize your Atlassian product's functionality.
- Securely authenticate and interact with Atlassian REST APIs.
- Application features:
    Collaborator network
    Workload analyzer
        Heat Map
        Workload distribution
    CategorizePro

## Development Environment Setup

### Atlassian Connect App
Before you begin, make sure you have Node.js installed. You can download it from [nodejs.org](https://nodejs.org/).

#### macOS
```bash
# Install the Atlas Connect command-line tool
sudo npm install -g atlas-connect

# Verify the installation
atlas-connect
```

#### Windows 10
1. Download and install Node.js from [nodejs.org](https://nodejs.org/).
2. Open a command prompt with admin privileges (Run As Administrator).
3. Run the following commands:
   ```bash
   # Install the Atlas Connect command-line tool
   npm install -g atlas-connect

   # Verify the installation
   atlas-connect
   ```

#### Ubuntu Linux
```bash
# Install Node.js and npm
sudo apt-get install nodejs npm

# Install the Atlas Connect command-line tool
sudo npm install -g atlas-connect

# Verify the installation
atlas-connect
```

### Django App (categorizePro)
Make sure you have Django installed. You can install it using pip:
```bash
pip install Django
```

### JIRA Setup
Use the following link to set up an Atlassian developer account: [Getting Started with Connect](https://developer.atlassian.com/cloud/jira/platform/getting-started-with-connect/#step-2--get-a-cloud-development-site).
You will need the email ID and API key for later steps.

## Running the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/sensei-Oogway/teamanalyzerr
   ```

2. Navigate to the repository folder:
   ```bash
   cd teamanalyzerr
   ```

3. Update the `/credentials.json` file with your user email, team ID, and API key.

4. Run the Django backend server:
   ```bash
   cd Teamanalyzer/backend/app
   python manage.py runserver
   ```

5. In another terminal or prompt, navigate to the repository folder:
   ```bash
   cd teamanalyzerr
   ```

6. Start the Node.js server:
   ```bash
   npm start
   ```

7. Follow the steps to give access to the tunnel URL as outlined in [Set Up Your Local Development Environment](https://developer.atlassian.com/cloud/jira/platform/getting-started-with-connect/#step-4--set-up-your-local-development-environment).

8. Open your JIRA project to see the app running.

That's it! You've set up your development environment and can now work on the Team Analyzer project.