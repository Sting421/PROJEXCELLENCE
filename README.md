# PROJEXCELLENCE

<h1 align="center">
  <img src="./PROJEXCELLENCE/static/res/logoWBg.jpg" alt="Project Logo" width="200" /><br />
  <span style="font-size: 2em; font-weight: bold;">PROJECT MANAGEMENT SYSTEM</span>
</h1>

## About PROJEXCELLENCE

PROJEXCELLENCE is a comprehensive project management system designed to streamline team collaboration, task management, and project tracking. The system provides a centralized platform for teams to manage projects, assign and track tasks, communicate through blog posts, organize team structures, and visualize project timelines.

### Key Features

- **User Authentication & Profile Management**: Secure email-based login and registration with customizable user profiles
- **Project Management**: Create, edit, and delete projects with detailed descriptions and tracking capabilities
- **Task Management**: Comprehensive task tracking with status updates (Pending, On-going, Done), due dates, and assignment capabilities
- **Team Collaboration**: Create teams within projects with different role assignments (Member, Manager, Head)
- **Timeline Visualization**: Calendar-based view of tasks and deadlines with filtering options
- **Resource Library**: Central repository for project resources
- **Blog Posts & Comments**: In-project communication through blog posts and comments
- **Responsive Design**: Bootstrap-based UI for seamless experience across devices

## System Architecture

- **Backend**: Django web framework with custom user authentication
- **Database**: SQLite database with relational models for users, projects, tasks, teams, and communications
- **Frontend**: HTML, CSS, JavaScript with Bootstrap and Django Templates
- **Media Handling**: Profile image upload and processing with Pillow
- **Form Processing**: Django forms with Crispy Forms for enhanced UI
- **Data Filtering**: Django-filter for advanced search and filtering capabilities

## Project Resources

- [Entity Relationship Diagram (ERD)](https://lucid.app/lucidchart/948151db-f69a-4aa7-a3af-692bc680f76f/edit?page=0_0&invitationId=inv_b185c4d6-ca9b-4c1d-a990-9edcf7c5f1c4#)
- [Figma Prototype](https://www.figma.com/design/Ejn0kA6AoDekfoNpKFUWXq/IM2?node-id=0-1&t=wTeiojp3ZGKXDLTL-1)
- [Gantt Chart](https://docs.google.com/spreadsheets/d/1QTl-HRuxibmfoPrlHXM7rtjF6_c43Y9-kxwVyI9Ik6k/edit?usp=sharing)
- [Project Requirements](https://docs.google.com/document/d/1nWzAiBxbicxQGC9QtIwUru9vspHINHGE5XID0jx5WNI/edit?usp=sharing)

## Team Members

- **zincaid (Lanz Roy Sumalpong)** - Project Manager / Designer / Front-end / Tester
- **Sting421 (Aldrin John Vitorillo)** - Full-stack Developer
- **Raveneko (Mary Apple Ramos)** - Designer & Front-end / Tester

## Installation Guide

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Sting421/PROJEXCELLENCE.git
   ```

2. **Go to the project directory**  
   ```bash
   cd PROJEXCELLENCE
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the application**
   ```bash
   python manage.py runserver
   ```
   The application will be available at http://127.0.0.1:8000/

## Core Models

- **User**: Extended Django user model with email authentication and profile management
- **Project**: Central entity for organizing work with descriptions and ownership
- **Task**: Work items with status tracking, assignments, and due dates
- **Team**: Group structure within projects with role-based memberships
- **BlogPost**: Communication tool for project updates and discussions
- **Comments**: Feedback mechanism for blog posts

## Key Features Explained

### Task Management
- Create and assign tasks to team members
- Track task status (Pending, On-going, Done)
- Set due dates and monitor progress
- Filter tasks by various criteria

### Timeline View
- Calendar-based visualization of tasks and deadlines
- Month and day navigation
- Task filtering by date

### Team Collaboration
- Create teams within projects
- Assign different roles to team members
- Manage team composition and responsibilities

## Technologies Used
- **Frontend**: HTML, CSS, Bootstrap, JavaScript, Django Templates
- **Backend**: Django
- **Database**: SQLite
- **Additional Tools**: 
  - Crispy Forms (enhanced form rendering)
  - Django Filter (advanced data filtering)
  - Pillow (image processing)
  - Ruff (code linting)
  - PyTZ (timezone handling)
  - Python-dotenv (environment variable management)
