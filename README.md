  UW PICO 5.09                    File: README.md                     Modified  

# Application-Mini Blog app

# Problem Statement
Build a full stack mini web application that combines frontend and backend.
Here I have made a blog app which-

-Authentication : Sign up /Log in and access your dashboard   
 - create, update, delete your posts and also upload your images for your blog.

-View everyone's posts and add your comments

-Use my curated contact form to get in touch with me! (emails sent via SMTP)
               
# Tech Stack Used
- Frontend: HTML CSS JS( via Bootstrap templates and the Jinja2 templating)    
- Backend: Flask      
- Database: MySQL
- Auth: werkzeug password hashing, sessions

# Roadmap to understanding code structure
- for better understanding,code cleanups are necessary.
- **wsgi.py:** running of the app is because of this.
- **requirements.txt:** every packages ive used in my code.
- **config.json:** just a friendly place for non secretive values, good for non tech people wanting to use the code.
- **.env:** for secrets
- **.gitignore:** so that git doesnt by mistake commit the .env files 
- **__init__.py:** initialisation, configuration

