from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QTabWidget,
                             QLabel, QDialog, QLineEdit, QComboBox, QDateEdit,
                             QSpinBox, QDoubleSpinBox, QMessageBox, QHeaderView, QScrollArea)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon, QBrush
from datetime import datetime, date
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import DatabaseManager
from gui.dialogs import AddExpenseDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle('💰 Expense Manager - إدارة المصاريف الشخصية')
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet(self.get_stylesheet())
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        header = self.create_header()
        main_layout.addWidget(header)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #bbb;
                background-color: #f0f4f8;
            }
            QTabBar::tab { 
                background-color: #e0e0e0; 
                color: #333;
                padding: 8px 20px;
                border: 1px solid #bbb;
                margin-right: 2px;
            }
            QTabBar::tab:selected { 
                background-color: #2196F3;
                color: white;
                border: 1px solid #2196F3;
            }
            QTabBar::tab:hover { 
                background-color: #64B5F6;
                color: white;
            }
        """)
        
        self.tab_expenses = QWidget()
        self.tab_charts = QWidget()
        self.tab_reports = QWidget()
        
        self.tab_widget.addTab(self.tab_expenses, '📊 المصاريف')
        self.tab_widget.addTab(self.tab_charts, '📈 الإحصائيات')
        self.tab_widget.addTab(self.tab_reports, '📋 التقارير')
        
        self.setup_expenses_tab()
        self.setup_charts_tab()
        self.setup_reports_tab()
        
        main_layout.addWidget(self.tab_widget)
        central_widget.setLayout(main_layout)
    
    def create_header(self):
        header = QWidget()
        header.setStyleSheet("""
            background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
            color: white;
            padding: 15px;
        """)
        layout = QHBoxLayout()
        
        title = QLabel('💰 Expense Manager')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setStyleSheet("color: #1A1A1A; background: transparent;")
        
        subtitle = QLabel('Professional Expense Tracking Application')
        subtitle.setFont(QFont('Arial', 10))
        subtitle.setStyleSheet("color: #E3F2FD; background: transparent;")
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(title)
        left_layout.addWidget(subtitle)
        
        layout.addLayout(left_layout)
        layout.addStretch()
        
        header.setLayout(layout)
        return header
    
    def get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #f0f4f8;
            }
            QWidget {
                background-color: #f0f4f8;
                color: #333;
            }
            QLabel {
                color: #333;
                background: transparent;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f5f5f5;
                gridline-color: #ddd;
                border: 1px solid #ddd;
                border-radius: 4px;
                color: #333;
            }
            QTableWidget::item {
                padding: 5px;
                color: #333;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QComboBox {
                background-color: white;
                color: #333;
                border: 1px solid #bbb;
                border-radius: 4px;
                padding: 5px;
                selection-background-color: #2196F3;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(noimg);
            }
            QComboBox:hover {
                border: 1px solid #2196F3;
            }
        """
    
    def setup_expenses_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        add_btn = QPushButton('➕ إضافة مصروف جديد')
        add_btn.clicked.connect(self.add_expense)
        add_btn.setMinimumHeight(40)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        button_layout.addWidget(add_btn)
        
        delete_btn = QPushButton('🗑️ حذف المصروف')
        delete_btn.clicked.connect(self.delete_expense)
        delete_btn.setMinimumHeight(40)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #da190b; }
        """)
        button_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton('🔄 تحديث')
        refresh_btn.clicked.connect(self.load_data)
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #e68900; }
        """)
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels([
            'ID', 'المبلغ', 'الفئة', 'التاريخ', 'الوصف', 'النوع', 'اللون'
        ])
        
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSelectionBehavior(1)
        self.table_widget.setSelectionMode(1)
        
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.table_widget)
        self.tab_expenses.setLayout(layout)
    
    def setup_charts_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        year_label = QLabel('📅 السنة:')
        year_label.setFont(QFont('Arial', 11, QFont.Bold))
        year_label.setStyleSheet("color: #333; background: transparent;")
        filter_layout.addWidget(year_label)
        
        self.year_combo = QComboBox()
        self.year_combo.setMinimumWidth(100)
        current_year = datetime.now().year
        for year in range(current_year - 5, current_year + 2):
            self.year_combo.addItem(str(year))
        self.year_combo.setCurrentText(str(current_year))
        filter_layout.addWidget(self.year_combo)
        
        month_label = QLabel('📆 الشهر:')
        month_label.setFont(QFont('Arial', 11, QFont.Bold))
        month_label.setStyleSheet("color: #333; background: transparent;")
        filter_layout.addWidget(month_label)
        
        self.month_combo = QComboBox()
        self.month_combo.setMinimumWidth(120)
        months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
        self.month_combo.addItems(months)
        self.month_combo.setCurrentIndex(datetime.now().month - 1)
        filter_layout.addWidget(self.month_combo)
        
        update_chart_btn = QPushButton('📊 تحديث الإحصائيات')
        update_chart_btn.clicked.connect(self.update_charts)
        update_chart_btn.setMinimumHeight(35)
        filter_layout.addWidget(update_chart_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        self.charts_table = QTableWidget()
        self.charts_table.setColumnCount(4)
        self.charts_table.setHorizontalHeaderLabels(['الفئة', 'المبلغ (ريال)', 'النسبة المئوية', 'النوع'])
        self.charts_table.setAlternatingRowColors(True)
        self.charts_table.setSelectionBehavior(1)
        
        header = self.charts_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.charts_table)
        self.tab_charts.setLayout(layout)
    
    def setup_reports_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        year_label = QLabel('📅 السنة:')
        year_label.setFont(QFont('Arial', 11, QFont.Bold))
        year_label.setStyleSheet("color: #333; background: transparent;")
        filter_layout.addWidget(year_label)
        
        self.report_year_combo = QComboBox()
        self.report_year_combo.setMinimumWidth(100)
        current_year = datetime.now().year
        for year in range(current_year - 5, current_year + 2):
            self.report_year_combo.addItem(str(year))
        self.report_year_combo.setCurrentText(str(current_year))
        filter_layout.addWidget(self.report_year_combo)
        
        month_label = QLabel('📆 الشهر:')
        month_label.setFont(QFont('Arial', 11, QFont.Bold))
        month_label.setStyleSheet("color: #333; background: transparent;")
        filter_layout.addWidget(month_label)
        
        self.report_month_combo = QComboBox()
        self.report_month_combo.setMinimumWidth(120)
        months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
        self.report_month_combo.addItems(months)
        self.report_month_combo.setCurrentIndex(datetime.now().month - 1)
        filter_layout.addWidget(self.report_month_combo)
        
        update_report_btn = QPushButton('📋 تحديث التقرير')
        update_report_btn.clicked.connect(self.update_reports)
        update_report_btn.setMinimumHeight(35)
        filter_layout.addWidget(update_report_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(20)
        
        self.income_label = QLabel('💰 الدخل: 0.00 SAR')
        self.income_label.setFont(QFont('Arial', 13, QFont.Bold))
        self.income_label.setStyleSheet("""
            color: #4CAF50;
            padding: 10px;
            background-color: rgba(76, 175, 80, 0.1);
            border-radius: 4px;
            border-left: 4px solid #4CAF50;
        """)
        summary_layout.addWidget(self.income_label)
        
        self.expenses_label = QLabel('💸 المصاريف: 0.00 SAR')
        self.expenses_label.setFont(QFont('Arial', 13, QFont.Bold))
        self.expenses_label.setStyleSheet("""
            color: #f44336;
            padding: 10px;
            background-color: rgba(244, 67, 54, 0.1);
            border-radius: 4px;
            border-left: 4px solid #f44336;
        """)
        summary_layout.addWidget(self.expenses_label)
        
        self.balance_label = QLabel('💎 الرصيد: 0.00 SAR')
        self.balance_label.setFont(QFont('Arial', 13, QFont.Bold))
        self.balance_label.setStyleSheet("""
            color: #2196F3;
            padding: 10px;
            background-color: rgba(33, 150, 243, 0.1);
            border-radius: 4px;
            border-left: 4px solid #2196F3;
        """)
        summary_layout.addWidget(self.balance_label)
        
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(4)
        self.report_table.setHorizontalHeaderLabels(['الفئة', 'الدخل (ريال)', 'المصاريف (ريال)', 'الصافي (ريال)'])
        self.report_table.setAlternatingRowColors(True)
        self.report_table.setSelectionBehavior(1)
        
        header = self.report_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.report_table)
        self.tab_reports.setLayout(layout)
    
    def add_expense(self):
        dialog = AddExpenseDialog(self, self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
            self.update_charts()
            self.update_reports()
    
    def delete_expense(self):
        current_row = self.table_widget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'تنبيه', 'الرجاء اختيار مصروف للحذف')
            return
        
        expense_id = int(self.table_widget.item(current_row, 0).text())
        reply = QMessageBox.question(self, 'تأكيد', 'هل تريد حذف هذا المصروف؟')
        
        if reply == QMessageBox.Yes:
            self.db.delete_expense(expense_id)
            self.load_data()
            self.update_charts()
            self.update_reports()
    
    def load_data(self):
        expenses = self.db.get_all_expenses()
        self.table_widget.setRowCount(len(expenses))
        
        for row, expense in enumerate(expenses):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(expense['id'])))
            self.table_widget.setItem(row, 1, QTableWidgetItem(f"{expense['amount']:.2f}"))
            self.table_widget.setItem(row, 2, QTableWidgetItem(expense['category']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(expense['date']))
            self.table_widget.setItem(row, 4, QTableWidgetItem(expense['description'] or ''))
            self.table_widget.setItem(row, 5, QTableWidgetItem(expense['type']))
            
            color_item = QTableWidgetItem()
            color = QColor(expense['color'])
            color_item.setBackground(color)
            self.table_widget.setItem(row, 6, color_item)
    
    def update_charts(self):
        year = self.year_combo.currentText()
        month = self.month_combo.currentIndex() + 1
        
        category_data = self.db.get_category_summary(year, month)
        
        total_expenses = sum(item['total'] for item in category_data if item['type'] == 'expense')
        
        self.charts_table.setRowCount(len(category_data))
        
        for row, item in enumerate(category_data):
            self.charts_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.charts_table.setItem(row, 1, QTableWidgetItem(f"{item['total']:.2f}"))
            
            percentage = (item['total'] / total_expenses * 100) if total_expenses > 0 else 0
            self.charts_table.setItem(row, 2, QTableWidgetItem(f"{percentage:.1f}%"))
            self.charts_table.setItem(row, 3, QTableWidgetItem(item['type']))
            
            color_item = QTableWidgetItem()
            color = QColor(item['color'])
            color_item.setBackground(color)
            self.charts_table.setItem(row, 0, color_item)
            self.charts_table.item(row, 0).setText(item['name'])
    
    def update_reports(self):
        year = self.report_year_combo.currentText()
        month = self.report_month_combo.currentIndex() + 1
        
        expenses_data = self.db.get_expenses_by_month(year, month)
        
        income = sum(item['amount'] for item in expenses_data if item['type'] == 'income')
        expenses = sum(item['amount'] for item in expenses_data if item['type'] == 'expense')
        balance = income - expenses
        
        self.income_label.setText(f'الدخل: {income:.2f}')
        self.expenses_label.setText(f'المصاريف: {expenses:.2f}')
        self.balance_label.setText(f'الرصيد: {balance:.2f}')
        
        category_data = self.db.get_category_summary(year, month)
        
        category_summary = {}
        for item in category_data:
            if item['name'] not in category_summary:
                category_summary[item['name']] = {'income': 0, 'expenses': 0}
            if item['type'] == 'income':
                category_summary[item['name']]['income'] = item['total']
            else:
                category_summary[item['name']]['expenses'] = item['total']
        
        self.report_table.setRowCount(len(category_summary))
        
        for row, (category, data) in enumerate(category_summary.items()):
            self.report_table.setItem(row, 0, QTableWidgetItem(category))
            self.report_table.setItem(row, 1, QTableWidgetItem(f"{data['income']:.2f}"))
            self.report_table.setItem(row, 2, QTableWidgetItem(f"{data['expenses']:.2f}"))
            self.report_table.setItem(row, 3, QTableWidgetItem(f"{data['income'] - data['expenses']:.2f}"))
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()
