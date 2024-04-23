PLEASE REFER TO THE REPORT FOR INDEPTH ANALYSIS

In the Python Script, we created different functions for the different windows which are displayed and can be accessed from the front end. The functions are connected to the main database, which has been created through the MySQL script. The Different functions consist of different MySQL query which is run on the connector to populate data in the table or fetch records from the already populated tables. 

For the Take Test Window:
We created a view of the table containing the questions, and used the view for displaying the questions and their key for keeping a track of the response given by the user. We also used an insert statement to add the Name, Age and Phone Numbers and the options into the transaction table created in the database.

For the View Result Window: 
We used different sets of queries for splitting the details of the users and then used cases to calculate the personality type based on the responses fed into the Take Test Window. the personality of all the users in the database can be accessed through this window.

For the Matching Window:
We used a Query to group all the users into a particular personality type. We then created a dropdown list containing the personality types, which can be accessed to find all the users possessing the same personality, which will help in matching same personality users.

INSTRUCTIONS FOR EXECUTION:
- In your python environment execute this line: "pip install mysql-connector-python"
- In your python environment execute this line: "pip install "
- In your MySql workbbench upload the provided .sql file and execute the code
- In your environment run the python script using the command:"python main.py"
- Take the test and evaluate yourself !!

