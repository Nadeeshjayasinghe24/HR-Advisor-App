HR Advisor Web Application

An AI-powered HR advisor designed specifically for the APAC market, providing country-specific compliance guidance and HR management tools for startups and SMEs.

Project Structure

Plain Text


hr_advisor_app/
├── backend/          # Flask backend application
│   ├── src/         # Source code
│   ├── requirements.txt
│   └── init_db.py
├── frontend/        # React frontend application
│   ├── src/         # Source code
│   ├── package.json
│   └── vite.config.js
└── README.md


Features

•
AI-Powered HR Advice: Country-specific HR guidance using OpenAI

•
Multi-Country Support: Singapore, Australia, Malaysia, Hong Kong, and more

•
Template Generation: Automated HR document creation

•
Subscription Management: Tiered pricing with coin-based usage

•
User Authentication: Secure JWT-based authentication

•
Employee Management: Comprehensive employee data management

Technology Stack

Backend

•
Framework: Flask

•
Database: SQLAlchemy with SQLite

•
Authentication: JWT

•
AI Integration: OpenAI API

Frontend

•
Framework: React

•
UI Library: Shadcn UI

•
Build Tool: Vite

•
Package Manager: pnpm

Getting Started

Backend Setup

1.
Navigate to the backend directory:

2.
Create and activate a virtual environment:

3.
Install dependencies:

4.
Initialize the database:

5.
Run the Flask application:

Frontend Setup

1.
Navigate to the frontend directory:

2.
Install dependencies:

3.
Start the development server:

Deployment

The application is designed for easy deployment:

•
Backend: Can be deployed to platforms like Heroku, Render, or AWS

•
Frontend: Can be deployed to Vercel, Netlify, or any static hosting service

Environment Variables

Create a .env file in the backend directory with the following variables:

Plain Text


OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///hr_advisor.db


Contributing

1.
Fork the repository

2.
Create a feature branch

3.
Make your changes

4.
Submit a pull request

License

This project is proprietary software. All rights reserved.

Support

For support and questions, please contact the development team.

