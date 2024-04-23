import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
    QComboBox
)
from PyQt5.QtGui import QPixmap, QFont

import mysql.connector

class TakeTestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Take Test")
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("background-color: black; color: white;")
        self.setFont(QFont("Arial", 15))
        layout = QVBoxLayout(self)

        # Add labels and entry fields for name, age, and phone number
        self.name_label = QLabel("Name:")
        self.name_label.setStyleSheet("color: white;")
        self.name_entry = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_entry)

        self.age_label = QLabel("Age:")
        self.age_label.setStyleSheet("color: white;")
        self.age_entry = QLineEdit()
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_entry)

        self.phone_label = QLabel("Phone Number:")
        self.phone_label.setStyleSheet("color: white;")
        self.phone_entry = QLineEdit()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_entry)

        # Fetch questions from the database and create question labels and radio buttons
        self.fetch_and_display_questions(layout)

        # Add submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("color: black; background-color: white;")
        self.submit_button.clicked.connect(self.submit_test)
        layout.addWidget(self.submit_button)

    def fetch_and_display_questions(self, layout):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1905",
                database="final_proj"
            )
            cursor = connection.cursor()

            # Fetch questions from the database
            cursor.execute("SELECT * FROM vw_getquestionoption")
            questions = cursor.fetchall()

            # Create question labels and radio buttons
            self.option_groups = []
            for question in questions:
                question_label = QLabel(question[0])
                question_label.setStyleSheet("color: white;")
                layout.addWidget(question_label)

                options = question[1:]
                option_group = QButtonGroup()
                for option in options:
                    radio_button = QRadioButton(option)
                    radio_button.setStyleSheet("color: white;")
                    layout.addWidget(radio_button)
                    option_group.addButton(radio_button)
                self.option_groups.append(option_group)

            connection.close()

        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Database Error", f"Failed to fetch questions: {error}")

    def submit_test(self):
        name = self.name_entry.text()
        age = self.age_entry.text()
        phone = self.phone_entry.text()

        if not name or not age.isdigit() or not phone.isdigit():
            QMessageBox.critical(self, "Input Error", "Please enter valid name, age, and phone number.")
            return

        selected_options = []
        for option_group in self.option_groups:
            selected_option = ""
            for button in option_group.buttons():
                if button.isChecked():
                    selected_option = button.text()
                    break
            selected_options.append(selected_option)

        if len(selected_options) != len(self.option_groups):
            QMessageBox.critical(self, "Input Error", "Please answer all questions.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1905",
                database="final_proj"
            )
            cursor = connection.cursor()

            for index, option in enumerate(selected_options):
                query = "INSERT INTO personqa (person_name, questionoptionid, questionid, age, phone_no) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (name, index + 1, index + 1, int(age), int(phone)))

            connection.commit()
            QMessageBox.information(self, "Test Submitted", "Test submitted successfully.")

        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Database Error", f"Failed to submit test: {error}")

        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

class ViewResultsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Results")
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("background-color: black; color: white;")
        self.setFont(QFont("Arial", 20))

        layout = QVBoxLayout(self)

        # Add dropdown to select criteria
        self.criteria_label = QLabel("Select Person | Phone Number:")
        self.criteria_label.setStyleSheet("color: white;")
        self.criteria_label.setFont(QFont("Arial", 20))
        layout.addWidget(self.criteria_label)

        self.criteria_dropdown = QComboBox()
        self.criteria_dropdown.setFont(QFont("Arial", 15))  # Set font size for dropdown items
        layout.addWidget(self.criteria_dropdown)

        # Add display result button
        self.display_button = QPushButton("Display Result")
        self.display_button.setStyleSheet("color: black; background-color: white;")
        self.display_button.setFont(QFont("Arial", 20))  # Set font size for button
        self.display_button.clicked.connect(self.display_result)
        layout.addWidget(self.display_button)

        # Populate dropdown with data
        self.populate_dropdown()

    def populate_dropdown(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1905",
                database="final_proj"
            )
            cursor = connection.cursor()

            # Fetch distinct names and phone numbers
            cursor.execute("SELECT DISTINCT person_name, phone_no FROM personqa")
            results = cursor.fetchall()

            # Add items to dropdown
            for result in results:
                item_text = f"{result[0]} | {result[1]}"
                self.criteria_dropdown.addItem(item_text)

        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Database Error", f"Failed to fetch data: {error}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def display_result(self):
        selected_criteria = self.criteria_dropdown.currentText()

        # Extract the selected name and phone number from the selected criteria
        selected_name, selected_phone = selected_criteria.split(' | ')
        selected_name = selected_name.strip()
        selected_phone = selected_phone.strip()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1905",
                database="final_proj"
            )
            cursor = connection.cursor()

            # Execute the modified query with the selected name and phone number
            query = f"""SELECT a.person_name, a.age, c.personal_type, SUM(b.optionmarks) AS Totalmarks,  
                        CASE 
                            WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) > 0 THEN 'Extrovert' 
                            WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) <= 0 THEN 'Introvert' 
                            WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) > 0 THEN 'Thinking' 
                            WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) <= 0 THEN 'Feeling' 
                            WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) > 0 THEN 'Sensing' 
                            WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) <= 0 THEN 'Intuitive' 
                            WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) > 0 THEN 'Judging' 
                            WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) <= 0 THEN 'Perceiving' 
                        END AS PersonalityTrait 
                        FROM personqa AS a 
                        LEFT JOIN questionoptions AS b ON a.questionoptionid = b.questionoptionid 
                        LEFT JOIN personality_questions AS c ON a.questionid = c.questionid 
                        WHERE a.person_name = '{selected_name}' AND phone_no = {selected_phone}
                        GROUP BY a.person_name, a.age, c.personal_type"""

            cursor.execute(query)
            result = cursor.fetchall()

            # Create a new window to display the result in a table
            result_window = QMessageBox()
            result_window.setWindowTitle("Result")
            result_window.setStyleSheet("background-color: black; color: white;")
            result_text = ""
            for row in result:
                result_text += (f"Name: {row[0]}, Age: {row[1]}, Personal Type: {row[2]}, Total Marks: {row[3]}, Personality Trait: {row[4]}\n")

            result_window.setText(result_text)
            result_window.exec_()

            connection.close()

        except mysql.connector.Error as error:
            QMessageBox.critical(None, "Database Error", f"Failed to fetch result: {error}")


class MatchingWindow(QWidget):
    def __init__(self, personality_traits):
        super().__init__()
        self.setWindowTitle("Matching Results")
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("background-color: black; color: white;")

        layout = QVBoxLayout(self)

        self.trait_label = QLabel("Select The Personality type of the people you want to see:")
        self.trait_label.setStyleSheet("color: white;")
        self.trait_label.setFont(QFont("Arial", 20))
        layout.addWidget(self.trait_label)

        self.trait_dropdown = QComboBox()
        for trait in personality_traits:
            self.trait_dropdown.addItem(trait[0])
        layout.addWidget(self.trait_dropdown)
        self.trait_dropdown.setFont(QFont("Arial", 20))

        self.display_button = QPushButton("Display People")
        self.display_button.setStyleSheet("color: black; background-color: white;")
        self.display_button.clicked.connect(self.display_people)
        layout.addWidget(self.display_button)

    def display_people(self):
        selected_trait = self.trait_dropdown.currentText()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1905",
                database="final_proj"
            )
            cursor = connection.cursor()

            cursor.execute(f"""SELECT person_name, phone_no FROM (
                                SELECT 
                                    a.person_name, 
                                    a.phone_no, 
                                    c.personal_type, 
                                    SUM(b.optionmarks) AS Totalmarks, 
                                    CASE 
                                        WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) > 0 THEN 'Extrovert' 
                                        WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) <= 0 THEN 'Introvert' 
                                        WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) > 0 THEN 'Thinking' 
                                        WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) <= 0 THEN 'Feeling' 
                                        WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) > 0 THEN 'Sensing' 
                                        WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) <= 0 THEN 'Intuitive' 
                                        WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) > 0 THEN 'Judging' 
                                        WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) <= 0 THEN 'Perceiving' 
                                    END AS PersonalityTrait 
                                FROM 
                                    personqa AS a 
                                LEFT JOIN 
                                    questionoptions AS b ON a.questionoptionid = b.questionoptionid 
                                LEFT JOIN 
                                    personality_questions AS c ON a.questionid = c.questionid 
                                GROUP BY 
                                    a.person_name, a.phone_no, c.personal_type
                            ) AS subquery 
                            WHERE 
                                PersonalityTrait = '{selected_trait}'""")
            matching_results = cursor.fetchall()

            # Display the results in a messagebox
            result_window = QMessageBox()
            result_window.setWindowTitle("Matching Results")
            result_window.setStyleSheet("background-color: black; color: white;")
            result_window.setText(f"People with {selected_trait} personality: {matching_results}")
            result_window.exec_()

        except mysql.connector.Error as error:
            QMessageBox.critical(None, "Database Error", f"Failed to fetch matching results: {error}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

class PersonalityTestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MBTI personality test")
        self.setGeometry(100, 100, 1080, 720)
        self.setStyleSheet("background-color: black; color: white;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create buttons with larger font size and increased size
        self.take_test_button = QPushButton("Take Test")
        self.take_test_button.setStyleSheet("color: black; background-color: white; font-size: 18px; padding: 10px;")
        self.take_test_button.clicked.connect(self.take_test)
        self.layout.addWidget(self.take_test_button)

        self.view_results_button = QPushButton("View Results")
        self.view_results_button.setStyleSheet("color: black; background-color: white; font-size: 18px; padding: 10px;")
        self.view_results_button.clicked.connect(self.view_results)
        self.layout.addWidget(self.view_results_button)

        self.matching_window_button = QPushButton("Matching Window")
        self.matching_window_button.setStyleSheet("color: black; background-color: white; font-size: 18px; padding: 10px;")
        self.matching_window_button.clicked.connect(self.open_matching_window)
        self.layout.addWidget(self.matching_window_button)

        # Load and resize the first image
        image_path1 = "C:/Users/Arnav/Desktop/dbms_project/shutterstock_2070009056.jpg"
        pixmap1 = QPixmap(image_path1).scaled(1000, 600)

        # Load and resize the second image
        image_path2 = "C:/Users/Arnav/Desktop/dbms_project/content_myersbriggs-larg-min600.jpg"
        pixmap2 = QPixmap(image_path2).scaled(1000, 600)

        # Display the images
        image_label1 = QLabel()
        image_label1.setPixmap(pixmap1)
        image_label2 = QLabel()
        image_label2.setPixmap(pixmap2)

        image_layout = QHBoxLayout()
        image_layout.addWidget(image_label1)
        image_layout.addWidget(image_label2)
        self.layout.addLayout(image_layout)


    def display_people(self):
        selected_trait = self.trait_dropdown.currentText()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1905",
                database="final_proj"
            )
            cursor = connection.cursor()

            cursor.execute(f"""SELECT person_name, phone_no FROM (
                                SELECT 
                                    a.person_name, 
                                    a.phone_no, 
                                    c.personal_type, 
                                    SUM(b.optionmarks) AS Totalmarks, 
                                    CASE 
                                        WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) > 0 THEN 'Extrovert' 
                                        WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) <= 0 THEN 'Introvert' 
                                        WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) > 0 THEN 'Thinking' 
                                        WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) <= 0 THEN 'Feeling' 
                                        WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) > 0 THEN 'Sensing' 
                                        WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) <= 0 THEN 'Intuitive' 
                                        WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) > 0 THEN 'Judging' 
                                        WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) <= 0 THEN 'Perceiving' 
                                    END AS PersonalityTrait 
                                FROM 
                                    personqa AS a 
                                LEFT JOIN 
                                    questionoptions AS b ON a.questionoptionid = b.questionoptionid 
                                LEFT JOIN 
                                    personality_questions AS c ON a.questionid = c.questionid 
                                GROUP BY 
                                    a.person_name, a.phone_no, c.personal_type
                            ) AS subquery 
                            WHERE 
                                PersonalityTrait = '{selected_trait}'""")
            matching_results = cursor.fetchall()

            # Display the results in a messagebox
            result_window = QMessageBox()
            result_window.setWindowTitle("Matching Results")
            result_window.setStyleSheet("background-color: black; color: white;")
            result_window.setText(f"People with {selected_trait} personality: {matching_results}")
            result_window.exec_()

        except mysql.connector.Error as error:
            QMessageBox.critical(None, "Database Error", f"Failed to fetch matching results: {error}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

class PersonalityTestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MBTI personality test")
        self.setGeometry(100, 100, 1080, 720)
        self.setStyleSheet("background-color: black; color: white;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Create buttons
        self.take_test_button = QPushButton("Take Test")
        self.take_test_button.setStyleSheet("color: black; background-color: white;")
        self.take_test_button.clicked.connect(self.take_test)
        button_layout.addWidget(self.take_test_button)

        self.view_results_button = QPushButton("View Results")
        self.view_results_button.setStyleSheet("color: black; background-color: white;")
        self.view_results_button.clicked.connect(self.view_results)
        button_layout.addWidget(self.view_results_button)

        self.matching_window_button = QPushButton("Matching Window")
        self.matching_window_button.setStyleSheet("color: black; background-color: white;")
        self.matching_window_button.clicked.connect(self.open_matching_window)
        button_layout.addWidget(self.matching_window_button)

        # Add button layout to the main layout
        self.layout.addLayout(button_layout)

        # Load and resize the first image
        image_path1 = "C:/Users/Arnav/Desktop/dbms_project/shutterstock_2070009056.jpg"
        pixmap1 = QPixmap(image_path1).scaled(800, 600)

        # Load and resize the second image
        image_path2 = "C:/Users/Arnav/Desktop/dbms_project/content_myersbriggs-larg-min600.jpg"
        pixmap2 = QPixmap(image_path2).scaled(800, 600)

        # Display the images
        image_label1 = QLabel()
        image_label1.setPixmap(pixmap1)
        image_label2 = QLabel()
        image_label2.setPixmap(pixmap2)

        # Create horizontal layout for images
        image_layout = QHBoxLayout()
        image_layout.addWidget(image_label1)
        image_layout.addWidget(image_label2)

        # Add image layout to the main layout
        self.layout.addLayout(image_layout)

    def take_test(self):
        # Create the take test window
        self.take_test_window = TakeTestWindow()
        self.take_test_window.show()

    def view_results(self):
        # Create the view results window
        self.view_results_window = ViewResultsWindow()
        self.view_results_window.show()

    def open_matching_window(self):
        # Run the matching query and display matching window
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1905",
                database="final_proj"
            )
            cursor = connection.cursor()

            # Run the matching query to fetch all personality traits
            cursor.execute("""SELECT DISTINCT PersonalityTrait FROM (
                                SELECT 
                                    a.person_name, 
                                    a.phone_no, 
                                    c.personal_type, 
                                    SUM(b.optionmarks) AS Totalmarks, 
                                    CASE 
                                        WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) > 0 THEN 'Extrovert' 
                                        WHEN c.personal_type = 'E-I' AND SUM(b.optionmarks) <= 0 THEN 'Introvert' 
                                        WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) > 0 THEN 'Thinking' 
                                        WHEN c.personal_type = 'T-F' AND SUM(b.optionmarks) <= 0 THEN 'Feeling' 
                                        WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) > 0 THEN 'Sensing' 
                                        WHEN c.personal_type = 'S-N' AND SUM(b.optionmarks) <= 0 THEN 'Intuitive' 
                                        WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) > 0 THEN 'Judging' 
                                        WHEN c.personal_type = 'J-P' AND SUM(b.optionmarks) <= 0 THEN 'Perceiving' 
                                    END AS PersonalityTrait 
                                FROM 
                                    personqa AS a 
                                LEFT JOIN 
                                    questionoptions AS b ON a.questionoptionid = b.questionoptionid 
                                LEFT JOIN 
                                    personality_questions AS c ON a.questionid = c.questionid 
                                GROUP BY 
                                    a.person_name, a.phone_no, c.personal_type
                            ) AS subquery""")
            personality_traits = cursor.fetchall()

            # Create the matching window
            self.matching_window = MatchingWindow(personality_traits)
            self.matching_window.show()

        except mysql.connector.Error as error:
            QMessageBox.critical(None, "Database Error", f"Failed to fetch personality traits: {error}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonalityTestApp()
    window.show()
    sys.exit(app.exec_())
