Jewelry Inventory Management System
Overview
This project provides a simple inventory management system for a jewelry shop. It includes:

A console-based application for basic CRUD operations and summaries using an in-memory data store.
A web-based application built with Flask, using SQLite for persistence, served via Apache and mod_wsgi.
Docker containerization for the web app.
Deployment script to AWS Elastic Beanstalk via ECR and S3.

The system supports adding items (rings, bracelets, necklaces in silver/gold), viewing inventory, marking items as sold, updating items, calculating profit summaries, and getting inventory summaries.
Features

Item Management: Add, update, mark as sold.
Inventory Views: List all items or get summarized counts by type/category/status.
Profit Calculation: Total costs, revenue, profit, and per-item profits for sold items.
Web Interface: Responsive UI with sidebar navigation, dark mode, and form validation.
Deployment: Automated script for building Docker image, pushing to ECR, and deploying to Elastic Beanstalk.

Requirements
Console App

Python 3.8+

Web App

Python 3.8+
Flask
Docker (for containerization)
AWS CLI (for deployment)
AWS account with ECR, S3, Elastic Beanstalk permissions

Directory Structure
text.
├── main.py                  # Console application entry point
├── functions.py             # Shared functions (adapted for console in-memory or web SQLite)
├── app.py                   # Flask web application
├── app.wsgi                 # WSGI config for Apache
├── apache.conf              # Apache VirtualHost config
├── Dockerfile               # Docker build for web app
├── deploy.sh                # Deployment script to AWS
├── Dockerrun.aws.json       # Elastic Beanstalk Docker config
├── templates/               # Jinja2 templates for web UI
│   ├── add.html
│   ├── menu.html
│   ├── profit.html
│   ├── show.html
│   ├── sold.html
│   └── update.html
└── static/                  # CSS and JS for web UI
    ├── styles.css
    └── scripts.js
Setup and Installation
Console App

Ensure Python is installed.
Run python main.py to start the interactive menu.

Web App (Local)

Install dependencies: pip install flask.
Run python app.py to start the server at http://localhost:5000.
Access the dashboard and navigate via the sidebar.

Web App (Docker Local)

Build the image: docker build -t jewelry-app .
Run the container: docker run -p 80:80 jewelry-app
Access at http://localhost/.

Note: The Docker setup creates /var/www/flask_app/inventory.db on first run if missing.
Usage
Console App

Run python main.py.
Follow the menu:

Add item: Input type, category, cost.
Show inventory: Lists all items.
Mark sold: Input ID and selling price.
Update: Input ID and optional fields.
Profit summary: Displays costs, revenue, profit.
Inventory summary: Counts total/available/sold, by type/category.
Quit.



Web App

Navigate to / for the dashboard.
Use sidebar links for actions.
Forms include validation (e.g., positive prices, valid types).
Dark mode toggle and mobile-responsive menu.

Deployment to AWS Elastic Beanstalk

Configure AWS CLI with credentials.
Update deploy.sh variables (e.g., APP_NAME, REGION, S3_BUCKET).
Ensure zip is available (script handles Windows fallback).
Run ./deploy.sh (make executable if needed: chmod +x deploy.sh).

The script:

Logs into ECR, creates repo if needed.
Builds and pushes Docker image.
Creates Dockerrun.aws.json and zips it.
Uploads to S3.
Creates/updates Elastic Beanstalk app/environment.

Solution Stack: Uses "64bit Amazon Linux 2023 v4.6.3 running Docker" (latest as of August 2025). Verify with aws elasticbeanstalk list-available-solution-stacks.
Environment settings:

Load-balanced with min 2, max 4 instances.
IAM Instance Profile: "LabInstanceProfile" (update if needed).
Health check at "/".

After deployment, the script outputs the environment CNAME (e.g., jewelry-env.elasticbeanstalk.com).
