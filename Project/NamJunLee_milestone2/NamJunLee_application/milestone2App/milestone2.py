import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone2App.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def executeQuery(sql_str):
    try:
        conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='leeilgoo12'")
    except:
        print("Unable to connect to the database!")
    cur = conn.cursor()
    cur.execute(sql_str)
    conn.commit()
    result = cur.fetchall()
    conn.close()
    return result


class milestone2(QMainWindow):
    def __init__(self):
        super(milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.bzipLine.textChanged.connect(self.zipChanged)
        self.ui.bnameLine.textChanged.connect(self.searchBusiness)

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT DISTINCT state FROM business ORDER BY state;"
        try:
            results = executeQuery(sql_str)
            for row in results:
                # add state list into item state
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed!")
        # not selected then empty first
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if self.ui.stateList.currentIndex() >= 0:
            sql_str = "SELECT DISTINCT city FROM business WHERE state = '" + state + "' ORDER BY city;"
            try:
                results = executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed!")

    def cityChanged(self):
        self.ui.zipList.clear()
        self.ui.bzipLine.clear()
        self.ui.bnameLine.clear()
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0):
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT DISTINCT zip FROM business WHERE city = '" + city + "' ORDER BY zip;"
            try:
                results = executeQuery(sql_str)
                for row in results:
                    self.ui.zipList.addItem(row[0])
            except:
                print("Query failed!")

    def zipChanged(self):
        self.ui.categoriesList.clear()
        self.ui.businessTable.clear()
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0) and \
                (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT DISTINCT ct.cname FROM categories as ct \
            WHERE ct.bid = (SELECT bid FROM business WHERE bid = ct.bid AND \
             zip = '" + zip + "') ORDER BY ct.cname;"
            try:
                results = executeQuery(sql_str)
                for row in results:
                    self.ui.categoriesList.addItem(row[0])
                self.ui.bzipLine.setText(zip)
            except:
                print("Query failed!")

    def searchBusiness(self):
        self.ui.businessTable.clear()
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0) and \
                (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            businessName = self.ui.bnameLine.text()
            sql_str = "SELECT bname, address, stars, reviewcount, numcheckins, reviewrating FROM business \
            WHERE zip = '" + zip + "' AND bname LIKE '%" + businessName + "%' ORDER BY bname;"
            try:
                results = executeQuery(sql_str)
                # set style of businessTable header
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                # set row, column
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                # set header name
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'Stars',
                                                                 'Review Count', '# of Checkins', 'Review Rating'])
                # better view
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec_())
