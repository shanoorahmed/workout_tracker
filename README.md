# workout_tracker
Steps to set up the project on your local machine:  
For zip downloads, unzip the folder and go to step 4.
1) Make a new folder.  
2) Initialize an empty git repository inside the folder by running the command "git init" in your terminal.  
3) Clone the repository using "git clone https://github.com/shanoorahmed/workout_tracker.git".  
4) Move into the folder, set up a new virtual enviroment and activate it.  
   4.1) For making a new virtual enviroment, paste "python3 -m venv venv" and run it.  
   4.2) For activating it:  
        Windows:  
        i) Set-ExecutionPolicy Unrestricted -scope process  
        ii) .\venv\Scripts\activate  
        Mac OS/Linux:  
        i) source venv/bin/activate  
5) Install all the dependencies using "pip install -r requirements.txt".  
6) Set up the database by entering the below commands one by one sequentially in the terminal:  
   i) python  
   ii) from application import db  
   iii) db.create_all()  
   iv) exit()  
7) Set up the enviroment variables and run the app.  
   Windows:  
   i) $env:FLASK_APP = "main"  
   ii) flask run  
   Mac OS/Linux:  
   i) export FLASK_APP=main  
   ii) flask run  