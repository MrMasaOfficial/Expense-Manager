import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    try:
        from gui.main_window import MainWindow
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        QMessageBox.critical(None, "Error", f"Failed to start application:\n{str(e)}")
        sys.exit(1)
