import sys
import joblib
import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog


class HormonePredictor(QWidget):
    def __init__(self):
        super().__init__()
        self.button = None
        self.cortisol_label = None
        self.melatonin_label = None
        self.initUI()

    def initUI(self):
        # Set up the window properties
        self.setWindowTitle('Hormone Predictor')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")

        layout = QVBoxLayout()

        # Create and add the "Choose file" button
        self.button = self.create_button('Choose file', 14, self.open_file)
        layout.addWidget(self.button)

        # Create and add the labels for cortisol and melatonin predictions
        self.cortisol_label = self.create_label('')
        layout.addWidget(self.cortisol_label)

        self.melatonin_label = self.create_label('')
        layout.addWidget(self.melatonin_label)

        self.setLayout(layout)

    @staticmethod
    def create_button(text, font_size, callback):
        # Create a button with specified text, font size, and callback function
        button = QPushButton(text)
        button.setFont(QFont('Arial', font_size))
        button.setStyleSheet(
            "background-color: #2196F3; color: #ffffff; padding: 10px; border-radius: 5px;")
        button.clicked.connect(callback)
        return button

    @staticmethod
    def create_label(text):
        # Create a label with specified text and default styles
        label = QLabel(text)
        label.setFont(QFont('Arial', 12))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            "color: #ffffff; padding: 10px; border: 1px solid white; border-radius: 10px;")
        label.setWordWrap(True)
        return label

    def open_file(self):
        # Open a file dialog to choose an Excel file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file", "",
                                                   "Excel Files (*.xlsx *.xls);;", options=options)
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        try:
            # Read and process the Excel file
            data = self.read_excel(file_path)
            data, cols_in_abnormal_format, col_indexes_in_abnormal_format = self.clean_data(data)
            if len(cols_in_abnormal_format) > 5:
                raise Exception("The number of missing values is more than 5. The data is considered incomplete!")
            data = self.replace_missing_values(data, cols_in_abnormal_format, col_indexes_in_abnormal_format)
            data_to_process = data.iloc[0]

            # Scale the data and make predictions
            data_scaled = self.scale_data(data_to_process)
            cortisol_prediction, melatonin_prediction = self.make_predictions(data_scaled)
            self.display_predictions(cortisol_prediction, melatonin_prediction)
        except Exception as e:
            self.display_error(e)

    @staticmethod
    def read_excel(file_path):
        # Read the Excel file and return the DataFrame
        return pd.read_excel(file_path)

    @staticmethod
    def clean_data(data):
        # Clean the data by dropping unnecessary columns and handling non-numeric columns
        data = data.drop(columns=['Gender'], axis=1).dropna(axis=1, how='all')
        cols_in_abnormal_format = data.select_dtypes(exclude=[np.number]).columns
        col_indexes_in_abnormal_format = {col: data.columns.get_loc(col) for col in cols_in_abnormal_format}
        numeric_data = data.drop(columns=cols_in_abnormal_format)
        return numeric_data, cols_in_abnormal_format, col_indexes_in_abnormal_format

    @staticmethod
    def replace_missing_values(data, cols_in_abnormal_format, col_indexes_in_abnormal_format):
        # Replace missing values in non-numeric columns with mean values from an external file
        mean_values_dict = pd.read_excel('Auxiliary files/mean_values.xlsx').set_index('Unnamed: 0')['Mean'].to_dict()
        offset = 0
        for column in cols_in_abnormal_format:
            if column in mean_values_dict:
                data.insert(col_indexes_in_abnormal_format[column] - offset, column, mean_values_dict[column])
            else:
                offset += 1
        return data

    @staticmethod
    def scale_data(row):
        # Scale the data using a pre-trained scaler
        scaler = joblib.load('Auxiliary files/scaler.joblib')
        return scaler.transform(row.to_frame().T)

    @staticmethod
    def make_predictions(data):
        # Load pre-trained models and make predictions
        cortisol_model = joblib.load("Auxiliary files/Cortisol (before sleep) class_model.joblib")
        melatonin_model = joblib.load("Auxiliary files/Melatonin (before sleep) class_model.joblib")
        cortisol_prediction = cortisol_model.predict(data)
        melatonin_prediction = melatonin_model.predict(data)
        return cortisol_prediction, melatonin_prediction

    def display_predictions(self, cortisol_prediction, melatonin_prediction):
        # Display the predictions for cortisol and melatonin
        self.update_label(self.cortisol_label, "cortisol", cortisol_prediction)
        self.update_label(self.melatonin_label, "melatonin", melatonin_prediction)

    @staticmethod
    def update_label(label, hormone, prediction):
        # Update the label with the prediction results
        if prediction == 1:
            label.setText(f"Your {hormone} levels are good!")
            label.setStyleSheet(
                "background-color: #4caf50; color: #ffffff; padding: 10px; border: 1px solid white; border-radius: 10px;")
        else:
            label.setText(f"You have {hormone} deficiency!")
            label.setStyleSheet(
                "background-color: #f44336; color: #ffffff; padding: 10px; border: 1px solid white; border-radius: 10px;")

    def display_error(self, exception):
        # Display an error message if something goes wrong
        error_message = "An error occurred while processing your data! Please check that all required fields are present, in order, and have valid values."
        detailed_error_message = f"Error details: {str(exception)}"
        self.cortisol_label.setText(error_message)
        self.cortisol_label.setStyleSheet(
            "background-color: #f44336; color: #ffffff; padding: 10px; border: 1px solid white; border-radius: 10px;")
        self.melatonin_label.setText(detailed_error_message)
        self.melatonin_label.setStyleSheet(
            "background-color: #f44336; color: #ffffff; padding: 10px; border: 1px solid white; border-radius: 10px;")


if __name__ == '__main__':
    # Run the application
    app = QApplication(sys.argv)
    ex = HormonePredictor()
    ex.show()
    sys.exit(app.exec_())
