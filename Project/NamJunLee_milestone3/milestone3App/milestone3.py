import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone3App.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class milestone3(QMainWindow):
    def __init__(self):
        super(milestone3, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.zipList.itemSelectionChanged.connect(self.totalBusinesses)
        self.ui.zipList.itemSelectionChanged.connect(self.totalPopulation)
        self.ui.zipList.itemSelectionChanged.connect(self.averageIncome)
        self.ui.zipList.itemSelectionChanged.connect(self.topCategories)
        self.ui.searchButton.clicked.connect(self.searchBusiness)
        self.ui.clearButton.clicked.connect(self.clearBusiness)
        self.ui.refreshButton.clicked.connect(self.popularSuccess)

    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='milestone3db' user='postgres' host='localhost' password='leeilgoo12'")
        except:
            print("Unable to connect to the database!")
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT DISTINCT state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
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
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed!")

    def cityChanged(self):
        self.ui.zipList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0):
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT DISTINCT zip FROM business WHERE city = '" + city + "' ORDER BY zip;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipList.addItem(row[0])
            except:
                print("Query failed!")

    def zipChanged(self):
        self.ui.categoriesList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0) and \
                (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT DISTINCT ct.cname FROM categories as ct \
            WHERE ct.bid = (SELECT bid FROM business WHERE bid = ct.bid AND \
             zip = '" + zip + "') ORDER BY ct.cname;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.categoriesList.addItem(row[0])
            except:
                print("Query failed!")

    def totalBusinesses(self):
        self.ui.businessesLine.clear()
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0) and \
                (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT COUNT(cs.cname) FROM categories as cs, business as bs \
            WHERE cs.bid = bs.bid AND bs.zip = '" + zip + "';"
            try:
                results = self.executeQuery(sql_str)
                self.ui.businessesLine.setText(str(results[0][0]))
            except:
                print("Query failed!")

    def totalPopulation(self):
        self.ui.populationLine.clear()
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0) and \
                (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT DISTINCT totalpopulation FROM business WHERE zip = '" + zip + "';"
            try:
                results = self.executeQuery(sql_str)
                self.ui.populationLine.setText(str(results[0][0]))
            except:
                print("Query failed!")

    def averageIncome(self):
        self.ui.incomeLine.clear()
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0) and \
                (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT DISTINCT avgincome FROM business WHERE zip = '" + zip + "';"
            try:
                results = self.executeQuery(sql_str)
                self.ui.incomeLine.setText(str(results[0][0]))
            except:
                print("Query failed!")

    def searchBusiness(self):
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0) and \
                (len(self.ui.zipList.selectedItems()) > 0) and \
                (len(self.ui.categoriesList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            categories = self.ui.categoriesList.selectedItems()[0].text()
            sql_str = "SELECT bname, address, city, ROUND(stars,1), reviewcount, reviewrating, numcheckins \
            FROM business \
            WHERE business.bid = (SELECT ct.bid FROM categories as ct \
            WHERE ct.bid = business.bid AND ct.cname = '" + categories + "') AND \
            business.zip = '" + zip + "' ORDER BY business.bname;"
            try:
                results = self.executeQuery(sql_str)
                # set style of businessTable header
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                # set row, column
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                # set header name
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name',
                                                                 'Address', 'City', 'Stars',
                                                                 'Review Count', 'Review Rating', '# of Checkins'])
                # better view
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 250)
                self.ui.businessTable.setColumnWidth(2, 150)
                self.ui.businessTable.setColumnWidth(3, 60)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed!")

    def topCategories(self):
        # set row, column
        self.ui.categoriesTable.setColumnCount(0)
        self.ui.categoriesTable.setRowCount(0)
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0) and \
                (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT COUNT(ct.cname) as numBusiness, ct.cname \
                      FROM categories as ct, business as bs \
                      WHERE ct.bid = bs.bid AND bs.zip = '" + zip + "' GROUP BY ct.cname ORDER BY numBusiness DESC;"
            try:
                results = self.executeQuery(sql_str)
                # set style of categoriesTable header
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.categoriesTable.horizontalHeader().setStyleSheet(style)
                # set row, column
                self.ui.categoriesTable.setColumnCount(len(results[0]))
                self.ui.categoriesTable.setRowCount(len(results))
                # set header name
                self.ui.categoriesTable.setHorizontalHeaderLabels(['# of Business', 'Category'])
                # better view
                self.ui.categoriesTable.resizeColumnsToContents()
                self.ui.categoriesTable.setColumnWidth(0, 150)
                self.ui.categoriesTable.setColumnWidth(1, 220)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.categoriesTable.setItem(currentRowCount, colCount,
                                                        QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print("Query failed!")

    def clearBusiness(self):
        self.ui.businessTable.clear()
        # set row, column
        self.ui.businessTable.setColumnCount(0)
        self.ui.businessTable.setRowCount(0)

    def popularSuccess(self):
        if (self.ui.stateList.currentIndex() >= 0) and \
                (len(self.ui.cityList.selectedItems()) > 0) and \
                (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            sql_str1 = "SELECT cs.cname, bs.bname, ROUND(bs.stars,1), bs.numcheckins, bs.reviewrating, bs.reviewcount \
                        FROM business as bs, categories as cs \
                       WHERE cs.bid = bs.bid AND bs.zip = '" + zip + "' AND \
                       (cs.cname, bs.numcheckins) IN (SELECT cname, MAX(numcheckins) FROM business, categories \
                        WHERE business.bid = categories.bid AND business.zip = '" + zip + "' GROUP BY cname) \
                        ORDER BY cs.cname;"
            sql_str2 = "SELECT bs.bname, bs.address, ROUND(bs.stars,1), bs.reviewcount, bs.numcheckins \
                        FROM business as bs, categories as cs \
                        WHERE cs.bid = bs.bid AND bs.zip = '" + zip + "' AND \
                        (bs.numcheckins) > (SELECT AVG(numcheckins) \
				        FROM business, categories WHERE business.bid = categories.bid AND \
                       business.zip = '" + zip + "' AND categories.cname = cs.cname GROUP BY cname) \
                        GROUP BY bs.bname, bs.address, bs.stars, bs.reviewcount, bs.numcheckins\
                        ORDER BY bs.numcheckins DESC;"
            try:
                # popular
                results1 = self.executeQuery(sql_str1)
                # set style of businessTable header
                style1 = "::section {""background-color: #f3f3f3; }"
                self.ui.popularTable.horizontalHeader().setStyleSheet(style1)
                # set row, column
                self.ui.popularTable.setColumnCount(len(results1[0]))
                self.ui.popularTable.setRowCount(len(results1))
                # set header name
                self.ui.popularTable.setHorizontalHeaderLabels(['Category',
                                                                'Business Names', 'Stars', '# of Checkins',
                                                                'Review Rating', '# of Reviews'])
                # better view
                self.ui.popularTable.resizeColumnsToContents()
                self.ui.popularTable.setColumnWidth(0, 300)
                self.ui.popularTable.setColumnWidth(1, 200)
                self.ui.popularTable.setColumnWidth(2, 70)
                currentRowCount1 = 0
                for row1 in results1:
                    for colCount1 in range(0, len(results1[0])):
                        self.ui.popularTable.setItem(currentRowCount1, colCount1,
                                                     QTableWidgetItem(str(row1[colCount1])))
                    currentRowCount1 += 1

                # successful
                results2 = self.executeQuery(sql_str2)
                # set style of businessTable header
                style2 = "::section {""background-color: #f3f3f3; }"
                self.ui.successfulTable.horizontalHeader().setStyleSheet(style2)
                # set row, column
                self.ui.successfulTable.setColumnCount(len(results2[0]))
                self.ui.successfulTable.setRowCount(len(results2))
                # set header name
                self.ui.successfulTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'Stars',
                                                                   '# of Reviews', '# of Checkins'])
                # better view
                self.ui.successfulTable.resizeColumnsToContents()
                self.ui.successfulTable.setColumnWidth(0, 280)
                self.ui.successfulTable.setColumnWidth(1, 280)
                self.ui.successfulTable.setColumnWidth(2, 110)
                currentRowCount2 = 0
                for row2 in results2:
                    for colCount2 in range(0, len(results2[0])):
                        self.ui.successfulTable.setItem(currentRowCount2, colCount2,
                                                        QTableWidgetItem(str(row2[colCount2])))
                    currentRowCount2 += 1
            except:
                print("Query failed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone3()
    window.show()
    sys.exit(app.exec_())
