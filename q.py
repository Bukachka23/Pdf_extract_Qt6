import os
from PyQt6 import QtWidgets, QtCore
from main import PDFWorker



class PDFExtractor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()                                                                          # Call the constructor of the parent class
        self.start_time = QtCore.QTime.currentTime()                                                # Get the current time
        self.worker_thread = None                                                                   # Create a worker thread
        self.destroyed.connect(self.stop_worker_thread)                                             # Stop the worker thread when the window is destroyed

        self.pdf_path_label = QtWidgets.QLabel("PDF file:")                                         # Create a label for the PDF file path
        self.pdf_path_input = QtWidgets.QLineEdit()                                                 # Create a text field for the PDF file path
        self.pdf_path_button = QtWidgets.QPushButton("Browse")                                      # Create a browse button
        self.pdf_path_button.setToolTip("Browse for a PDF file")                                    # Set the browse button tooltip
        self.pdf_path_button.clicked.connect(self.browse_file)                                      # Browse for a PDF file

        self.process_button = QtWidgets.QPushButton("Process PDF")                                  # Create a process button
        self.process_button.setToolTip("Process the PDF file")                                      # Set the process button tooltip
        self.process_button.clicked.connect(self.process_pdf)                                       # Process the PDF file

        self.clear_button = QtWidgets.QPushButton("Clear")                                          # Create a clear button
        self.clear_button.setToolTip("Clear the extracted text")                                    # Set the clear button tooltip
        self.clear_button.clicked.connect(self.clear)                                               # Clear the extracted text

        self.exit_button = QtWidgets.QPushButton("Exit")                                            # Create an exit button
        self.exit_button.clicked.connect(self.close)                                                # Close the application
        self.exit_button.setToolTip("Exit the application")                                         # Set the exit button tooltip

        self.text_label = QtWidgets.QLabel("Extracted Text:")                                       # Create a text label
        self.text_box = QtWidgets.QPlainTextEdit()                                                  # Create a text box
        self.text_box.setReadOnly(True)                                                             # Set the text box to read only

        self.progressbar = QtWidgets.QProgressBar()                                                 # Create a progress bar
        self.progressbar.setMinimum(0)                                                              # Set the progress bar minimum value
        self.progressbar.setMaximum(100)                                                            # Set the progress bar maximum value
        self.progressbar.setToolTip("Progress: 0%")                                                 # Set the progress bar tooltip

        self.progressbar_label = QtWidgets.QLabel("Progress:")                                      # Create a progress bar label
        self.progressbar_label.setAlignment \
            (QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)              # Align the progress bar label to the left
        self.progressbar_label.setToolTip("Progress bar")                                           # Set the progress bar label tooltip

        self.page_label = QtWidgets.QLabel("Pages processed:")                                      # Create a page label
        self.page_count_label = QtWidgets.QLabel()                                                  # Create a page count label
        self.percent_label = QtWidgets.QLabel()                                                     # Create a percent label
        self.time_label = QtWidgets.QLabel()                                                        # Create a time label

        grid_layout = QtWidgets.QGridLayout()                                                       # Create a grid layout
        grid_layout.addWidget(self.pdf_path_label, 0, 0)                                            # Add the PDF path label
        grid_layout.addWidget(self.pdf_path_input, 0, 1)                                            # Add the PDF path input
        grid_layout.addWidget(self.pdf_path_button, 0, 2)                                           # Add the browse button
        grid_layout.addWidget(self.process_button, 1, 0)                                            # Add the process button
        grid_layout.addWidget(self.clear_button, 1, 1)                                              # Add the clear button
        grid_layout.addWidget(self.exit_button, 1, 2)                                               # Add the exit button
        grid_layout.addWidget(self.text_label, 2, 0)                                                # Add the text label
        grid_layout.addWidget(self.text_box, 3, 0, 1, 3)                                            # Add the text box
        grid_layout.addWidget(self.progressbar, 4, 0, 1, 3)                                         # Add the progress bar
        grid_layout.addWidget(self.page_label, 5, 0)                                                # Add the page label
        grid_layout.addWidget(self.page_count_label, 5, 1)                                          # Add the page count label
        grid_layout.addWidget(self.percent_label, 5, 2)                                             # Add the percent label
        grid_layout.addWidget(self.time_label, 5, 3)                                                # Add the time label
        grid_layout.addWidget(self.progressbar_label, 4, 0)                                         # Add the progress bar label

        self.setLayout(grid_layout)                                                                 # Set the layout
        self.setWindowTitle("PDF Text Extractor")                                                   # Set the window title
        self.worker = None                                                                          # Create a worker


    # Clear the extracted text
    def stop_worker_thread(self):
        if self.worker_thread is not None:                                                          # If the worker thread exists
            self.worker_thread.quit()                                                               # Quit the worker thread
            self.worker_thread.wait()                                                               # Wait for the worker thread to finish


    # Browse for a PDF file
    def browse_file(self):
        file_dialog = QtWidgets.QFileDialog()                                                       # Create a file dialog
        file_dialog.setNameFilter("PDF Files (*.pdf)")                                              # Set the file filter
        file_dialog.setDefaultSuffix("pdf")                                                         # Set the default suffix
        file_path, _ = file_dialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")  # Get the path to the PDF file
        if file_path:
            self.pdf_path_input.setText(file_path)                                                  # Set the path to the PDF file


    # Clear the text box and reset the progress bar
    def clear(self):
        self.pdf_path_input.clear()                                                                  # Clear the file path input
        self.text_box.clear()                                                                        # Clear the text box
        self.progressbar.setValue(0)                                                                 # Reset the progress bar


    # Clear the extracted text
    def process_pdf(self):
        pdf_path = self.pdf_path_input.text()                                                        # Get the path to the PDF file
        if not os.path.exists(pdf_path):
            QtWidgets.QMessageBox.critical(self, "Error", f"File '{pdf_path}' not found")            # Display an error message
        else:
            self.process_button.setDisabled(True)                                                    # Disable the process button
            self.worker = PDFWorker(pdf_path)                                                        # Create a worker
            self.worker.total_pages.connect(self.set_total_pages)                                    # Connect the total_pages signal to the set_total_pages slot
            self.worker.current_page.connect(self.set_current_page)                                  # Connect the current_page signal to the set_current_page slot
            self.worker.progress.connect(self.set_progress)                                          # Connect the progress signal to the set_progress slot
            self.worker.time_remaining.connect(self.set_time_remaining)                              # Connect the time_remaining signal to the set_time_remaining slot
            self.worker.result.connect(self.display_text)                                            # Connect the result signal to the display_text slot
            self.worker.error.connect(self.display_error)                                            # Connect the error signal to the display_error slot
            self.start_time = QtCore.QTime.currentTime()                                             # Get the current time
            self.process_button.setDisabled(True)                                                    # Disable the process button
            self.worker_thread = QtCore.QThread()                                                    # Create a worker thread
            self.worker.moveToThread(self.worker_thread)                                             # Move the worker to the worker thread
            self.worker_thread.started.connect(self.worker.process_pdf)                              # Start the worker
            self.worker_thread.start()                                                               # Start the worker thread


    # Display the extracted text
    def set_total_pages(self, total_pages):
        self.page_count_label.setText(f"{total_pages}")                                              # Update the total number of pages


    # Update the progress bar
    def set_current_page(self, current_page):
        total_pages = int(self.page_count_label.text())                                              # Get the total number of pages
        if current_page == total_pages:                                                              # If the current page is the last page
            self.percent_label.setText(f"{100}%")                                                    # Update the percentage
            self.progressbar.setValue(100)                                                           # Update the progress bar
            self.progressbar.setToolTip(f"Progress: 100%")                                           # Update the progress bar tooltip

        # Calculate the progress
        else:
            self.percent_label.setText(f"{int(current_page / total_pages * 100)}%")                  # Update the percentage
            self.progressbar.setValue(int(current_page / total_pages * 100))                         # Update the progress bar
            self.progressbar.setToolTip(f"Progress: {int(current_page / total_pages * 100)}%")       # Update the progress bar tooltip
            self.time_label.setText("")
            self.page_count_label.setText(f"{current_page}")                                         # Update the page count

        # Calculate the time remaining
        if self.start_time.isValid():
            elapsed_time = self.start_time.msecsTo(QtCore.QTime.currentTime())                       # Time elapsed in milliseconds
            pages_left = total_pages - current_page                                                  # Pages left to process
            seconds_left = int(elapsed_time / current_page * pages_left / 1000)                      # Time remaining in seconds
            self.time_label.setText(f"{seconds_left // 60:02d}:{seconds_left % 60:02d}")             # Display the time remaining


    # Display the error message
    def set_progress(self, value):
        self.progressbar.setValue(value)                                                             # Update the progress bar


    # Display the error message
    def set_time_remaining(self, seconds):
        if seconds > 0:
            minutes, seconds = divmod(seconds, 60)
            self.time_label.setText(f"{minutes:02d}:{seconds:02d}")
        else:
            self.time_label.setText("")


    # Clear the text box
    def update_progressbar(self, value):
        self.progressbar.setValue(value)                                                             # Update the progress bar
        self.progressbar.setToolTip(f"Progress: {value}%")                                           # Update the progress bar tooltip


    # Display the extracted text
    def display_text(self, text):
        self.text_box.setPlainText(text)                                                             # Display the extracted text
        self.clear_button.setDisabled(self.text_box.toPlainText() == "")                             # Enable the clear button if the text box is not empty
        self.process_button.setDisabled(False)                                                       # Enable the process button
        self.progressbar.reset()                                                                     # Reset the progress bar
        self.progressbar.setToolTip("Progress: 0%")                                                  # Reset the progress bar tooltip


    # Display an error message
    def display_error(self, error):
        QtWidgets.QMessageBox.critical(self, "Error", error)                                         # Display the error message
        self.process_button.setDisabled(False)                                                       # Enable the process button
        self.progressbar.reset()                                                                     # Reset the progress bar
        self.progressbar.setToolTip("Progress: 0%")                                                  # Reset the progress bar tooltip




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = PDFExtractor()
    window.show()
    app.exec()














