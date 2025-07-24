# gitHub API

A concise Python-based flask API solution for interacting with the public GitHub Gists for a given user. This project is containerized for easy setup using Docker.

## Features

- Simple Python interface for GitHub API operations
- Dockerized environment for consistent deployment

## Requirements

Ensure you have the following installed:

* Python 3.9+
* pip
* Docker
* Git

## Quick Start 

1. **Clone the repository:**

    `git clone https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git`
   
    `cd <YOUR_REPO_NAME>`
   
2. **Setup with Docker**

   **2.1  Build the Docker image:**

    `docker build -t github-api .`

   **2.2  Run the container:**
   
    `docker run -p 8080:8080 github-api`
    
    The API will now be accessible at http://127.0.0.1:8080

3. **Setup locally(without Docker)**
   
    Set Up Virtual Environment & Install Dependencies
   
     **3.1 Create a virtual environment**

      `python3.12 -m venv venv`

     **3.2 Activate the virtual environment**

      `source venv/bin/activate`  # On Windows: `.\venv\Scripts\activate`

     **3.3 Install the required Python packages**

      `pip install -r requirements.txt`

     **3.4  Running the Application with Gunicorn**

      Gunicorn is a production-grade WSGI server that offers better performance and stability than Flask's built-in                 development server.

      Ensure your virtual environment is active and you are in the `<YOUR-REPO>` directory

      `gunicorn --bind 0.0.0.0:8080 app:app`

      The API will be available at `http://127.0.0.1:8080`.

4. **Test the API**

   Send a curl request to the API (e.g., for user octocat):

   `curl http://127.0.0.1:8080/octocat`

   You should receive a JSON array of octocat's public Gists.

5. **Run Automated Tests**

   To ensure everything is working correctly and to verify the code quality:  

   Ensure your virtual environment is active and you are in the `<YOUR-REPO>` directory
   
   `pytest`

## License
MIT License
