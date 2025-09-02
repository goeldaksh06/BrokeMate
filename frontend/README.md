<<<<<<< HEAD
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
=======
 BrokeMate 💸

An AI-powered budget buddy designed to make financial tracking effortless and insightful for students.

## Problem Statement

For students living in hostels on a fixed, tight monthly budget, financial discipline is a major challenge. Manual expense tracking is tedious and often abandoned, leading to overspending, end-of-month stress, and missed savings opportunities. Existing tools are often too complex for a student's simple financial situation.

## Our Solution

BrokeMate is a clean, simple, and intelligent web application that solves this problem. It provides a clear dashboard of a user's financial health and uses AI to automate the most tedious parts of budgeting, making it a tool students will actually use.

(Action:* Take a nice screenshot of your app's dashboard and upload it to your GitHub repo, then replace the text above with the link to the image.)*

✨ Key Features

  * *Secure User Accounts:* Full registration and login functionality to keep each user's financial data private and secure.
  * *Personalized Dashboard:* A clear, visual overview of the monthly budget, total spending, and remaining funds.
  * *AI-Powered Categorization:* Users simply type an expense description (e.g., "Dinner at the cafe"), and the app's AI automatically classifies it, removing the need for manual tagging.
  * *Data Visualization:* A dynamic pie chart provides an instant breakdown of spending habits, helping users see where their money goes.
  * *Editable Budget:* Users can set and update their own monthly budget.
  * *Transaction Management:* Users can log new expenses and delete old ones with ease.

 🛠 Tech Stack

  * *Frontend:*

      * HTML5 & CSS3
      * Vanilla JavaScript (using fetch for API communication)
      * Chart.js (for data visualization)

  * *Backend:*

      * Python 3
      * FastAPI (for high-performance, modern API endpoints)
      * Uvicorn (as the ASGI server)

  * *Database & Authentication:*

      * SQLite (for a simple, file-based, persistent database)
      * SQLAlchemy (as the Python ORM to interact with the database)
      * Simple Session-Based Authentication (using passlib for hashing)

  * *AI / Machine Learning:*

      * Hugging Face transformers library
      * Zero-Shot Text Classification Model (distilbert-base-uncased-mnli)

 🚀 Getting Started

Instructions on how to set up and run this project locally.
nstructions on how to set up and run this project locally.

 *Prerequisites*

  * Python 3.10+
  * pip and venv

 *Installation & Setup*

1.  *Clone the repository:*

    bash
    git clone <YOUR_GITHUB_REPO_URL>
    cd <YOUR_REPO_NAME>
    

2.  **Create a requirements.txt file:**
    *Before you can install the libraries, you need to create this file. Activate your virtual environment (source venv/bin/activate) and run this command in your terminal:*

    bash
    pip freeze > requirements.txt
    

    This saves all the libraries you installed into a file so others can easily install them. Commit this new file to your GitHub repo.

3.  *Create and activate a virtual environment:*

    bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    

4.  *Install the dependencies:*

    bash
      pip install -r requirements.txt
    

5.  *Run the application:*

    bash
    uvicorn main:app --reload
    

6.  *Open your browser* and navigate to http://127.0.0.1:8000.

 🧑‍💻 How to Use

1.  You will be redirected to the login page. Click the link to register a new account.
2.  Create an account with your email and a password.
3.  Log in with your new credentials.
4.  You will be taken to your personal dashboard where you can log expenses, see your spending chart, and manage your budget\!
>>>>>>> 35a73499af29bcc6514f2874a4d8c11231827d7c
