# 💰 Expense Manager

**A Professional Personal Expense Tracking Application**

A modern, user-friendly desktop application built with Python and PyQt5 for managing personal finances, tracking expenses and income, and generating detailed financial reports.

---

## ✨ Features

### 📊 Expense Management
- ✅ Add and delete expenses and income entries with ease
- ✅ Categorize transactions for better organization
- ✅ Record transaction dates and descriptions
- ✅ Support for both expense and income tracking
- ✅ Real-time data validation

### 💾 SQLite Database
- ✅ Secure local data storage
- ✅ Organized table structure (Expenses & Categories)
- ✅ Persistent data storage across sessions
- ✅ Efficient query performance

### 📈 Statistics & Analytics
- ✅ Detailed breakdown of expenses by category
- ✅ Percentage distribution calculations
- ✅ Monthly expense analysis
- ✅ Color-coded category identification

### 📋 Comprehensive Reports
- ✅ Monthly income and expense summaries
- ✅ Net balance calculations
- ✅ Category-wise financial breakdown
- ✅ Comparative analysis tools

### 🎨 User Interface
- ✅ Modern, professional design with Material Design principles
- ✅ Intuitive tabbed interface
- ✅ Dark-themed color scheme with blue gradients
- ✅ Responsive layout
- ✅ Emoji-enhanced navigation for better UX

---

## 📋 Available Categories

1. **Food** (طعام) 🍔
2. **Transportation** (مواصلات) 🚗
3. **Entertainment** (ترفيه) 🎮
4. **Health** (صحة) 🏥
5. **Education** (تعليم) 📚
6. **Housing** (مسكن) 🏠
7. **Other** (أخرى) 📦
8. **Income** (دخل) 💰

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd expense_manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

---

## 📖 Usage Guide

### Main Window

The application features a professional header with three main tabs:

#### 📊 **Expenses Tab**
- **View all transactions** in a comprehensive table
- **Add New Expense** ➕ - Opens a dialog to input new transaction details
- **Delete Expense** 🗑️ - Remove selected transaction (with confirmation)
- **Refresh** 🔄 - Update the display to show latest data

**Columns:**
- ID: Unique transaction identifier
- Amount: Transaction value in SAR
- Category: Expense category
- Date: Transaction date
- Description: Additional notes
- Type: Expense or Income
- Color: Visual category indicator

#### 📈 **Statistics Tab**
- **Filter by Year and Month** using dropdown menus
- **View category distribution** in a detailed table
- **Percentage calculation** for each category
- **Real-time updates** with the refresh button

**Displays:**
- Category name
- Transaction amount
- Percentage of total spending
- Transaction type (expense/income)

#### 📋 **Reports Tab**
- **Monthly financial summary** with key metrics
- **Income Display** 💰 - Total income in green
- **Expense Display** 💸 - Total expenses in red
- **Balance Display** 💎 - Net balance in blue
- **Detailed breakdown** by category

**Metrics:**
- Total Income
- Total Expenses
- Net Balance (Income - Expenses)
- Category-wise breakdown with income, expenses, and net values

### Adding a New Entry

1. Click **➕ Add New Expense** button
2. Enter the transaction details:
   - **Amount**: Transaction value (up to 999,999.99)
   - **Type**: Select either Expense (🔴) or Income (🟢)
   - **Category**: Choose from 8 predefined categories
   - **Date**: Transaction date (auto-filled with today)
   - **Description**: Optional notes for reference
3. Click **✅ Save** to add the transaction
4. Click **❌ Cancel** to close without saving

---

## 🏗️ Project Structure

```
expense_manager/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py           # Database manager class
│   └── expenses.db             # SQLite database (auto-created)
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py          # Main application window
│   ├── dialogs.py              # Dialog windows
│   └── __pycache__/            # Compiled Python files
│
└── utils/
    ├── __init__.py
    ├── charts.py               # Chart generation utilities
    └── __pycache__/            # Compiled Python files
```

---

## 🔧 Technical Details

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt5 | 5.15.7 | GUI framework |

### Database Schema

#### Categories Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    color TEXT DEFAULT '#FF6B6B'
);
```

#### Expenses Table
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    type TEXT CHECK(type IN ('expense', 'income')) DEFAULT 'expense',
    FOREIGN KEY(category_id) REFERENCES categories(id)
);
```

---

## 🎯 Core Classes

### DatabaseManager (`database/db_manager.py`)
- **`__init__(db_name)`** - Initialize database connection
- **`init_database()`** - Create tables if they don't exist
- **`add_expense(amount, category_id, date, description, type)`** - Add new transaction
- **`get_all_expenses()`** - Retrieve all transactions
- **`get_expenses_by_month(year, month)`** - Get transactions for specific month
- **`get_category_summary(year, month)`** - Get category-wise breakdown
- **`get_categories()`** - Retrieve all available categories
- **`delete_expense(id)`** - Remove transaction by ID
- **`close()`** - Close database connection

### MainWindow (`gui/main_window.py`)
- **`setup_expenses_tab()`** - Configure expenses view
- **`setup_charts_tab()`** - Configure statistics view
- **`setup_reports_tab()`** - Configure reports view
- **`load_data()`** - Load and display all expenses
- **`add_expense()`** - Open add expense dialog
- **`delete_expense()`** - Delete selected expense
- **`update_charts()`** - Refresh statistics display
- **`update_reports()`** - Refresh reports display

### AddExpenseDialog (`gui/dialogs.py`)
- **`init_ui()`** - Build dialog interface
- **`load_categories()`** - Load categories from database
- **`save_expense()`** - Validate and save new transaction

---

## 🎨 Design Features

### Color Scheme
- **Primary Blue**: #2196F3 (Headers, buttons)
- **Success Green**: #4CAF50 (Add/Income)
- **Error Red**: #f44336 (Delete/Expense)
- **Warning Orange**: #FF9800 (Refresh)
- **Background**: #f8f9fa (Light gray)

### User Experience
- Emoji indicators for quick visual recognition
- Consistent button styling with hover effects
- Alternating row colors in tables for readability
- Responsive layout that adapts to window size
- Tooltips and placeholder text for guidance

---

## 💡 Usage Tips

1. **Organize Categories**: Properly categorize expenses for better analysis
2. **Add Descriptions**: Use descriptions for future reference and analysis
3. **Regular Updates**: Keep data current for accurate reporting
4. **Monthly Review**: Check monthly reports to identify spending patterns
5. **Backup Data**: Periodically back up your database file

---

## 🔒 Data Privacy

- All data is stored locally on your computer
- No internet connection required
- No cloud synchronization
- Database file: `database/expenses.db`
- Backup by copying this file to a safe location

---

## 🛠️ Troubleshooting

### Application Won't Start
- Verify Python 3.7+ is installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`
- Check for permission issues in the project folder

### Database Issues
- Delete `database/expenses.db` to reset and start fresh
- Database will be automatically recreated on next launch
- Ensure write permissions for the database folder

### Display Issues
- Update PyQt5: `pip install --upgrade PyQt5`
- Try restarting the application
- Check your display scaling settings

---

## 🚀 Future Enhancements

Potential features for future versions:

- 📊 Advanced charts (pie charts, bar graphs)
- 📁 Data export (CSV, PDF, Excel)
- 📱 Mobile companion app
- 💾 Automatic backup system
- 📈 Budget forecasting
- 🌍 Multi-currency support
- 🔐 Password protection
- 📊 Financial insights and analytics
- 💬 Multi-language support

---

## 📄 License

This project is open-source and free to use for personal purposes.

---

## 👨‍💻 Developer Notes

### Code Style
- Uses Python PEP 8 conventions
- Object-oriented programming design
- Modular architecture for easy maintenance
- Clear separation of concerns (UI, Database, Utils)

### Adding New Features
1. Create new methods in appropriate modules
2. Update UI components in `gui/main_window.py`
3. Ensure database compatibility
4. Test thoroughly before deploying

---

## 📞 Support

For issues or questions:
1. Check the Usage Guide above
2. Review the Troubleshooting section
3. Examine the source code documentation

---

## 🙏 Acknowledgments

Built with Python, PyQt5, and SQLite3

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Status**: Production Ready ✅

---

**Happy Expense Tracking! 💰**
