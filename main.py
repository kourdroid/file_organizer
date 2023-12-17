import os
import shutil
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QPixmap
import qdarkstyle

class FileOptimizerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Optimizer")
        self.setGeometry(200,200, 400, 100)
        
        # Logo
        self.logo_label = QLabel()
        logo_path = os.path.abspath("logo.png")  # Replace with the actual path to your logo
        logo_pixmap = QPixmap(logo_path)
        logo_pixmap = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio)

        if not logo_pixmap.isNull():
            self.logo_label.setPixmap(logo_pixmap)
            self.logo_label.setAlignment(Qt.AlignCenter)
        else:
            print(f"Error: Unable to load the logo from {logo_path}")

        # Title


        # UI elements
        self.source_label = QLabel("Source Directory:")
        self.source_entry = QLineEdit()
        self.browse_source_button = QPushButton("Browse")
        self.browse_source_button.clicked.connect(self.browse_source)
        self.browse_source_button.setStyleSheet("background-color: #3498db; color: white; border: 1px solid #2980b9;")

        self.destination_label = QLabel("Destination Directory:")
        self.destination_entry = QLineEdit()
        self.browse_destination_button = QPushButton("Browse")
        self.browse_destination_button.clicked.connect(self.browse_destination)
        self.browse_destination_button.setStyleSheet("background-color: #3498db; color: white; border: 1px solid #2980b9;")

        self.start_optimization_button = QPushButton("Start Optimization")
        self.start_optimization_button.clicked.connect(self.start_optimization)
        self.start_optimization_button.setStyleSheet("background-color: #e74c3c; color: white; border: 1px solid #c0392b;")

        self.delete_empty_folders_button = QPushButton("Delete Empty Folders")
        self.delete_empty_folders_button.clicked.connect(self.delete_empty_folders)
        self.delete_empty_folders_button.setStyleSheet("background-color: #e74c3c; color: white; border: 1px solid #c0392b;")

        self.clear_temp_button = QPushButton("Clear Temp")
        self.clear_temp_button.clicked.connect(self.clear_temp)
        self.clear_temp_button.setStyleSheet("background-color: #e74c3c; color: white; border: 1px solid #c0392b;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_entry)
        layout.addWidget(self.browse_source_button)
        layout.addWidget(self.destination_label)
        layout.addWidget(self.destination_entry)
        layout.addWidget(self.browse_destination_button)
        layout.addWidget(self.start_optimization_button)
        layout.addWidget(self.delete_empty_folders_button)
        layout.addWidget(self.clear_temp_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Apply the dark theme using QDarkStyle
        dark_stylesheet = qdarkstyle.load_stylesheet_pyside6()
        self.setStyleSheet(dark_stylesheet)

        # Set a dark color palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(70, 70, 70))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(100, 149, 237))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Highlight, QColor(255, 69, 0))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(dark_palette)


    def browse_source(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if folder_selected:
            self.source_entry.setText(folder_selected)

    def browse_destination(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if folder_selected:
            self.destination_entry.setText(folder_selected)

    def start_optimization(self):
        source_directory = self.source_entry.text()
        destination_directory = self.destination_entry.text()
        optimize_files(source_directory, destination_directory)

    def delete_empty_folders(self):
        destination_directory = self.destination_entry.text()
        delete_empty_folders(destination_directory)
        
    def clear_temp(self):
        temp_directory = "C:\Windows\Temp"
        clear_temp_directory(temp_directory)    


def optimize_files(source_dir, destination_dir):
    file_types = {
        'Fonts': ('.ttf', '.otf', '.woff', '.woff2'),
        'Images': ('.jpg', '.jpeg', '.png', '.gif','.webp', '.bmp', '.svg'),
        'Videos': ('.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'),
        'Documents': ('.docx', '.doc', '.xlsx'),
        'Archives': ('.zip',),
        'Music': ('.mp3',),
        'Illustrations': ('.ai',),
        'PhotoshopFiles': ('.psd',),
        'InDesignFiles': ('.indd',),
        'AfterEffectsFiles': ('.ae',),
        'PremiereProFiles': ('.prproj',),
        'BlenderFiles': ('.blend',),
        '3DObjects': ('.obj', '.fbx', '.stl'),
        'PythonScripts': ('.py',),
        'JavaScriptFiles': ('.js',),
        'HTMLFiles': ('.html',),
        'CSSFiles': ('.css',),
        'JSONFiles': ('.json',),
        'XMLFiles': ('.xml',),
        'MarkdownFiles': ('.md',),
        'C++Files': ('.cpp',),
        'JavaFiles': ('.java',),
    }

    for folder, extensions in file_types.items():
        folder_path = os.path.join(destination_dir, folder)
        os.makedirs(folder_path, exist_ok=True)

        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)

            if os.path.isfile(file_path):
                _, file_extension = os.path.splitext(filename)
                file_extension = file_extension.lower()

                if file_extension in extensions:
                    suggested_folder = folder
                    destination_path = os.path.join(destination_dir, suggested_folder, filename)
                    shutil.move(file_path, destination_path)
                    print(f"Moved '{filename}' to '{suggested_folder}' folder.")

    print("Optimization completed.")

def delete_empty_folders(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                print(f"Deleted empty folder: {folder_path}")

    print("Deletion of empty folders completed.")
    
    
def clear_temp_directory(directory):
    try:
        shutil.rmtree(directory)
        print(f"Temp directory '{directory}' cleared.")
    except Exception as e:
        print(f"Error clearing temp directory: {e}")
        QMessageBox.critical(None, "Error", f"Error clearing temp directory: {e}", QMessageBox.Ok)

# Main application loop
app = QApplication([])
window = FileOptimizerGUI()
window.show()
app.exec()







