import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
from datetime import datetime

class ChartsManager:
    
    @staticmethod
    def create_pie_chart(data, title=""):
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        if not data:
            ax.text(0.5, 0.5, 'لا توجد بيانات', ha='center', va='center', fontsize=14)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return fig
        
        categories = [item['name'] for item in data]
        amounts = [item['total'] for item in data]
        colors = [item['color'] for item in data]
        
        wedges, texts, autotexts = ax.pie(amounts, labels=categories, colors=colors,
                                           autopct='%1.1f%%', startangle=90)
        
        for text in texts:
            text.set_fontsize(10)
            text.set_fontfamily('DejaVu Sans')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        fig.tight_layout()
        return fig
    
    @staticmethod
    def create_bar_chart(data, title=""):
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        if not data:
            ax.text(0.5, 0.5, 'لا توجد بيانات', ha='center', va='center', fontsize=14)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return fig
        
        categories = [item['name'] for item in data]
        amounts = [item['total'] for item in data]
        colors = [item['color'] for item in data]
        
        bars = ax.bar(categories, amounts, color=colors, edgecolor='black', linewidth=1.5)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontsize=10)
        
        ax.set_ylabel('المبلغ', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        fig.tight_layout()
        return fig
    
    @staticmethod
    def create_summary_report(expenses_data):
        income = 0
        expenses = 0
        
        for item in expenses_data:
            if item['type'] == 'income':
                income += item['amount']
            else:
                expenses += item['amount']
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': income - expenses
        }
