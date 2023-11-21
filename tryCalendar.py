import sys
from PyQt5.QtCore import Qt, QRectF, QDate
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QCalendarWidget, QApplication
import pymysql


class CalendarWidget(QCalendarWidget):

    def __init__(self, parent=None):
        super(CalendarWidget, self).__init__(parent)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)  # Hide week numbers

        # Establish a database connection
        self.db_connection = pymysql.connect(
            host='localhost',
            user='root',
            password='mysql',
            database='hci',
            charset='utf8'
        )
        self.cursor = self.db_connection.cursor()

    def paintCell(self, painter, rect, date):
        painter.setRenderHint(QPainter.Antialiasing, True)

        painter.save()
        painter.drawRect(rect)

        # Set different colors for weekends and weekdays
        if date.dayOfWeek() == Qt.Saturday or date.dayOfWeek() == Qt.Sunday:
            painter.setPen(QColor(255, 0, 0))  # Red for weekends
        else:
            painter.setPen(QColor(0, 0, 0))  # Black for weekdays

        # Calculate font size and offsets based on cell dimensions
        font_size = min(rect.width(), rect.height()) // 5
        painter.setFont(QFont('Decorative', font_size))

        # Fetch the score from the database for the current date
        current_date = date.toString("yyyy-MM-dd")
        self.cursor.execute(f"SELECT score FROM score WHERE createdAt = '{current_date}'")
        result = self.cursor.fetchone()

        if result is not None:
            score = result[0]
            # Draw the score below the date number with proportional offset
            text_rect = QRectF(rect.left(), rect.top() + 3 * font_size, rect.width(), rect.height() - 3 * font_size)
            painter.setPen(QColor(0, 0, 255))  # Blue for the score
            painter.drawText(text_rect, Qt.AlignCenter, f'{score}점')
        else:
            # Draw "None" below the date number with proportional offset
            text_rect = QRectF(rect.left(), rect.top() + 3 * font_size, rect.width(), rect.height() - 3 * font_size)
            painter.setPen(QColor(0, 0, 255))  # Blue for "None"
            painter.drawText(text_rect, Qt.AlignCenter, 'None')

        painter.restore()



try:

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        w = CalendarWidget()
        w.show()
        sys.exit(app.exec_())

except Exception as e:
    print(f"An error occurred: {e}")
