Hormone Predictor Application. 
This application is designed to predict cortisol and melatonin levels from an Excel file containing hormone data. It uses pre-trained machine learning models to make these predictions.

Requirements
- Python 3.6+
- Required Python packages: sys, joblib, numpy, pandas, PyQt5

Installation
1. Clone the repository or download the script file.
2. Install the required packages using pip: pip install joblib numpy pandas pyqt5
3. Ensure you have the following files in an "Auxiliary files" folder:
- scaler.joblib: Pre-trained scaler for data normalization.
- Cortisol (before sleep) class_model.joblib: Pre-trained model for cortisol prediction.
- Melatonin (before sleep) class_model.joblib: Pre-trained model for melatonin prediction.
- mean_values.xlsx: Excel file containing mean values for missing data replacement.

Usage
1. Open a terminal or command prompt and navigate to the directory containing the script.
2. Run the script:
3. The application window will open. Follow these steps to use it:
- Click the "Choose file" button to open a file dialog.
- Select an Excel file containing the hormone data.
- The application will process the file and display the prediction results for cortisol and melatonin.
By following these steps, you can easily predict your hormone levels using the Hormone Predictor application.

Code Explanation
- HormonePredictor class inherits from QWidget and initializes the UI components in initUI().
- create_button() and create_label() are utility methods to create styled buttons and labels.
- open_file() method opens a file dialog to select an Excel file.
- process_file() method reads the file, cleans the data, scales it, and makes predictions.
- display_predictions() method displays the prediction results.
- display_error() method displays error messages in case of any issues during file processing.
