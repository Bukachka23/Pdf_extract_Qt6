from PyQt6 import QtCore
from pdfquery import PDFQuery


# Worker class
class PDFWorker(QtCore.QObject):
    progress = QtCore.pyqtSignal(int)                                                                # Signal for the progress bar
    total_pages = QtCore.pyqtSignal(int)                                                             # Signal for the total number of pages
    current_page = QtCore.pyqtSignal(int)                                                            # Signal for the current page
    time_remaining = QtCore.pyqtSignal(int)                                                          # Signal for the time remaining
    result = QtCore.pyqtSignal(str)                                                                  # Signal for the extracted text
    error = QtCore.pyqtSignal(str)                                                                   # Signal for the error message

    # Constructor
    def __init__(self, pdf_path):
        super().__init__()                                                                           # Call the parent class constructor
        self.pdf_path = pdf_path                                                                     # PDF file path

    # Process the PDF file
    @QtCore.pyqtSlot()                                                                               # Slot for the process_pdf method
    def process_pdf(self):
        try:
            pdf = PDFQuery(self.pdf_path)                                                            # Create a PDFQuery object
            pdf.load()
            text = pdf.pq('LTTextLineHorizontal:in_bbox("0, 0, 612, 792")').text()                   # Extract the text from the PDF file
            pages = text.split('\x0c')                                                               # Split the text into pages
            total_pages = len(pages)                                                                 # Get the total number of pages
            self.total_pages.emit(total_pages)                                                       # Emit the total number of pages signal

            # Simulate processing
            for i, page in enumerate(pages):                                                         # Loop through the pages
                self.current_page.emit(i + 1)                                                        # Emit the current page signal
                self.progress.emit(int(100 * (i + 1) / total_pages))                                 # Emit the progress signal
                QtCore.QThread.msleep(100)                                                           # Sleep for 100 milliseconds
                self.time_remaining.emit(0)                                                          # Emit the time remaining signal
                self.result.emit(text)                                                               # Emit the extracted text signal

        except Exception as e:
            self.error.emit(str(e))                                                                  # Emit the error message signal




