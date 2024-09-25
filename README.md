# Myers-Briggs Personality Test

This repository contains the project files for our Database Management Systems (DBMS) course. We have developed a Myers-Briggs Personality Test that determines a user's personality type based on their responses to a series of questions. The project utilizes MySQL for database management, while the backend and frontend are implemented in Python using PyQt for the user interface.

## Project Overview

The Myers-Briggs Personality Test is based on Carl Jung's theory of psychological types, providing insight into an individual's personality preferences. Our project focuses on:
- **Database Design**: Implementing a robust MySQL schema to store user responses and ensure data integrity.
- **Test Administration**: Developing functionalities for users to take the test and receive accurate personality type scores.
- **Profile Generation**: Automatically generating personality profiles based on users' test results.
- **Matching Feature**: An algorithm that suggests users with similar personality types, helping them connect with like-minded individuals.

## Tech Stack
- **Backend**: Python with MySQL connector
- **Frontend**: PyQt
- **Database**: MySQL

## Features
- **Test-taking Interface**: Users can input their details and take the test, with questions dynamically fetched from the database.
- **Result Viewing**: After completing the test, users can view their personality type and corresponding profile.
- **Matching System**: Users can search for other individuals with similar personality traits, making it easier to find compatible friends or peers.

## Database Schema
The project consists of the following key database components:
- **personality_questions**: Stores the questions for the test.
- **questionoptions**: Contains the options for each question.
- **persona**: Records user responses to the questions.
- **Views**: 
  - `vw_getperson`: Retrieves a list of test takers.
  - `vw_getquestionoption`: Displays the available questions and options dynamically for test-taking.

Our database design follows **Boyce-Codd Normal Form (BCNF)** to eliminate redundancy and ensure efficient data storage.

## Application Workflow

### Main Window
- **Take Test**: Users can enter their details and answer personality-related questions.
- **View Results**: Displays the test results for users after they have completed the test.
- **Matching Window**: Allows users to find others who share similar personality traits.

### Scoring Mechanism
Test responses are scored based on the Myers-Briggs Type Indicator (MBTI), which assigns a dominant personality type based on the user's answers. These types fall into one of four categories, and the profile is generated accordingly.

### Error Handling
We implemented error handling for database connections and queries, ensuring that users are notified if any issues arise during interaction.

## Limitations
- **UI Design**: The UI is built with PyQt, which limits its aesthetic appeal. Future improvements can involve a transition to web technologies like HTML/CSS.
- **Matching Algorithm**: Due to time constraints, the matching algorithm is a basic implementation and can be optimized further.

## Learning Outcomes
- **Frontend Development**: Though our front end is functional, there is room for improvement in UI/UX design, which could be achieved with more frontend expertise.
- **Database Optimization**: We could have used more advanced MySQL features like stored procedures and triggers to improve efficiency.

## Contributors
- Arnav Jalan (@arnav-jalan)
- Arnav Aditya (@Arnavadi19)
- Rachit Sen (@GameCorpGG)

## Acknowledgments
We extend our gratitude to our professor, Dr. Sonia Khetarpaul, and our Lab TAs for their support throughout the project.

For an in-depth analysis of the project and to see a working demo, refer to the project report included in this repository.

