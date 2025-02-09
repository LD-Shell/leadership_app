# Leadership Assessment App

A web-based leadership assessment application built with Flask and Bootstrap that lets you evaluate your leadership qualities using a modern, responsive interface. The app provides instant scoring, detailed category breakdowns, a dynamic results graph, an option to email your results, and even a counter showing how many users have taken the assessment.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Locally](#running-locally)
- [Deployment](#deployment)
  - [Deploying to Heroku](#deploying-to-heroku)
  - [Updating the Online Version](#updating-the-online-version)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## Features

- **Modern UI & Responsive Design:**  
  Uses Bootstrap 5 for a sleek, mobile-friendly interface with flexbox-based cards and a modern, compact gradient navbar.

- **Leadership Assessment:**  
  A set of 21 questions covering various leadership categories:
  - **Charisma**
  - **Character**
  - **Compassion**
  - **Courage**
  - **Competency**
  - **Conviction**
  - **Commitment**

- **Dynamic Graphs:**  
  Visualize your results with a dynamic bar chart generated using Matplotlib, where each category is displayed with a unique color.

- **Email Results:**  
  Option to send your assessment results directly to your email.

- **Usage Counter:**  
  The home page displays a counter showing how many people have used the assessment.

- **About Page & Contact Link:**  
  An About page provides more information about the app and its creator, and the Contact link directs users to the creator’s GitHub profile.

---

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/LD-Shell/leadership_app.git
   cd leadership-app
   
2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt

4. **Set Environment Variables (Optional for Development):**

   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development

5. **Running Locally:**

   ```bash
   python app.py