  UW PICO 5.09                    File: README.md                     Modified  

# Application-Mini Blog app

# Problem Statement
Build a full stack mini web application that combines frontend and backend.
Here I have made a blog app which-

-Authentication : Sign up /Log in and access your dashboard   
 - create, update, delete your posts.

-View everyone's posts and add your comments.


               
# Tech Stack Used
- Frontend: HTML CSS JS( via Bootstrap templates and the Jinja2 templating)    
- Backend: Flask      
- Database: MySQL
- Auth: werkzeug password hashing, sessions

# Steps to run the code 
- ** Prerequisites **
     - Python 3.10+
     - - pip
- ** Clone and install **
  - git clone https://github.com/<your-username>/<repo>.git
    cd <repo>
    python -m venv .venv
    source .venv/bin/activate    # Windows: .venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt  
- for local dev, create .env file with flask_env as development and a secret_key.
- run locally in terminal of the wsgi.py,  flask --app wsgi:app run --debug.

# Live Deployment Link
https://blog-app-3-i9oy.onrender.com

# A demo of website by me(recommended to watch)
Link: https://youtu.be/5-YXNJdH8Nw

# Roadmap to understanding code structure
- for better understanding,code cleanups are necessary.
- **wsgi.py:** running of the app is because of this.
- **requirements.txt:** every packages ive used in my code.
- **config.json:** just a friendly place for non secretive values, good for non tech people wanting to use the code.
- **.env:** for secrets
- **.gitignore:** so that git doesnt by mistake commit the .env files 
- **__init__.py:** initialisation, configuration


