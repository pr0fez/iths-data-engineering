#!/bin/bash

# yolo
# bert
# midjourney
# alphago
# alexnet

# Define variables
EXISTING_REPO="OlofHarrysson/iths-data-engineering"
EXISTING_BRANCH="13-prepare-repo-for-students"
NEW_REPO="OlofHarrysson/iths-data-engineering-group-test1"
NEW_BRANCH="main"

# Clone the existing repository and checkout the specific branch
git clone --branch $EXISTING_BRANCH "https://github.com/$EXISTING_REPO.git"
cd "iths-data-engineering"

# Remove the existing Git repository
rm -rf .git

# Create a new repository on GitHub
gh repo create $NEW_REPO --private

# Initialize a new Git repository
git init

# Add all the files to the new repository
git add .

# Commit the changes
git commit -m "Initial commit"

# Set the new repository as the remote
git remote add origin "https://github.com/$NEW_REPO.git"

# Push the code to the new repository's remote and set the branch as main
git push -u origin main:refs/heads/$NEW_BRANCH

# Cleanup
cd ..
rm -rf "iths-data-engineering"
