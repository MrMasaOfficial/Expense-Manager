from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox,
                             QPushButton, QMessageBox, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime

class AddExpenseDialog(QDialog):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('➕ إضافة مصروف/دخل جديد')
        self.setGeometry(200, 200, 450, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #333;
                font-weight: bold;
            }
            QLineEdit, QDateEdit, QDoubleSpinBox, QComboBox {
                background-color: white;
                color: #333;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                font-size: 11px;
            }
            QPushButton {
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
                min-height: 35px;
            }
            QPushButton#saveBtn {
                background-color: #4CAF50;
            }
            QPushButton#saveBtn:hover {
                background-color: #45a049;
            }
            QPushButton#cancelBtn {
                background-color: #f44336;
            }
            QPushButton#cancelBtn:hover {
                background-color: #da190b;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel('تفاصيل المصروف/الدخل')
        title.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(title)
        
        amount_layout = QHBoxLayout()
        amount_label = QLabel('💵 المبلغ:')
        amount_label.setMinimumWidth(80)
        amount_layout.addWidget(amount_label)
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(999999)
        self.amount_input.setDecimals(2)
        self.amount_input.setValue(0)
        self.amount_input.setMinimumHeight(30)
        amount_layout.addWidget(self.amount_input)
        layout.addLayout(amount_layout)
        
        type_layout = QHBoxLayout()
        type_label = QLabel('📊 النوع:')
        type_label.setMinimumWidth(80)
        type_layout.addWidget(type_label)
        self.type_group = QButtonGroup()
        self.expense_radio = QRadioButton('🔴 مصروف')
        self.income_radio = QRadioButton('🟢 دخل')
        self.expense_radio.setChecked(True)
        self.type_group.addButton(self.expense_radio, 0)
        self.type_group.addButton(self.income_radio, 1)
        type_layout.addWidget(self.expense_radio)
        type_layout.addWidget(self.income_radio)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        category_layout = QHBoxLayout()
        category_label = QLabel('📂 الفئة:')
        category_label.setMinimumWidth(80)
        category_layout.addWidget(category_label)
        self.category_combo = QComboBox()
        self.category_combo.setMinimumHeight(30)
        self.load_categories()
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        
        date_layout = QHBoxLayout()
        date_label = QLabel('📅 التاريخ:')
        date_label.setMinimumWidth(80)
        date_layout.addWidget(date_label)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMinimumHeight(30)
        date_layout.addWidget(self.date_input)
        layout.addLayout(date_layout)
        
        description_layout = QHBoxLayout()
        description_label = QLabel('📝 الوصف:')
        description_label.setMinimumWidth(80)
        description_layout.addWidget(description_label)
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText('ادخل وصف اختياري...')
        self.description_input.setMinimumHeight(30)
        description_layout.addWidget(self.description_input)
        layout.addLayout(description_layout)
        
        layout.addSpacing(10)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        save_btn = QPushButton('✅ حفظ')
        save_btn.setObjectName('saveBtn')
        save_btn.clicked.connect(self.save_expense)
        
        cancel_btn = QPushButton('❌ إلغاء')
        cancel_btn.setObjectName('cancelBtn')
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_categories(self):
        categories = self.db.get_categories()
        for category in categories:
            self.category_combo.addItem(category['name'], category['id'])
    
    def save_expense(self):
        try:
            amount = self.amount_input.value()
            if amount <= 0:
                QMessageBox.warning(self, 'خطأ', 'المبلغ يجب أن يكون أكبر من صفر')
                return
            
            category_id = self.category_combo.currentData()
            date_str = self.date_input.date().toString('yyyy-MM-dd')
            description = self.description_input.text()
            expense_type = 'income' if self.income_radio.isChecked() else 'expense'
            
            self.db.add_expense(amount, category_id, date_str, description, expense_type)
            
            QMessageBox.information(self, 'نجح', 'تم إضافة المصروف بنجاح')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'خطأ', f'حدث خطأ: {str(e)}')
