from PyQt5.QtWidgets import *
import sys, pickle
from PyQt5 import uic , QtWidgets
import pandas as pd
import table_display
from sklearn.preprocessing import LabelEncoder ,StandardScaler , MinMaxScaler , PowerTransformer
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.Browse = self.findChild(QPushButton , "Browse")
        self.columns = self.findChild(QListWidget,"column_list")
        self.Submit_btn = self.findChild(QPushButton , "Submit")
        self.target_col = self.findChild(QLabel,"target_col")
        self.shape = self.findChild(QLabel , "shape")
        self.scale_btn = self.findChild(QPushButton , "scale_btn")
        self.tableView = self.findChild(QTableView , "tableView")

        self.cat_column = self.findChild(QComboBox , "cat_column")
        self.drop_column = self.findChild(QComboBox , "drop_column")
        self.empty_column = self.findChild(QComboBox , "empty_column")
        self.convert_btn = self.findChild(QPushButton , "convert_btn")
        self.drop_btn = self.findChild(QPushButton , "drop_btn")
        self.fiil_mean = self.findChild(QPushButton , "fiil_mean")
        self.fill_na = self.findChild(QPushButton , "fill_na")

        #scater plot 등록
        self.scater_x = self.findChild(QComboBox , "scater_x")
        self.scater_y = self.findChild(QComboBox , "scater_y")
        self.scater_c = self.findChild(QComboBox , "scater_c")
        self.scater_mark = self.findChild(QComboBox , "scater_mark")
        self.scater_plot = self.findChild(QPushButton , "scater_plot")

        #line plot 등록
        self.line_x = self.findChild(QComboBox , "line_x")
        self.line_y = self.findChild(QComboBox , "line_y")
        self.line_c = self.findChild(QComboBox , "line_c")
        self.line_mark = self.findChild(QComboBox , "line_mark")
        self.line_plot = self.findChild(QPushButton , "line_plot")
        
        #히스토그램 등록
        self.hist_column = self.findChild(QComboBox , "hist_column")
        self.hist_column_add = self.findChild(QComboBox , "hist_column_add")
        self.hist_add_btn = self.findChild(QPushButton , "hist_add_btn")
        self.hist_remove_btn = self.findChild(QPushButton , "hist_remove_btn")
        self.histogram = self.findChild(QPushButton , "histogram")

        self.hist_add_btn.clicked.connect(self.hist_add_column)
        self.hist_remove_btn.clicked.connect(self.hist_remove_column)
        self.histogram.clicked.connect(self.histogram_plot)
        
        #히트맵 등록
        self.hitmap = self.findChild(QPushButton , "hitmap")
        self.hitmap.clicked.connect(self.plot_heatmap)

        self.Browse.clicked.connect(self.get_csv)
        self.columns.clicked.connect(self.target)
        self.Submit_btn.clicked.connect(self.set_target)
        
        # fillna 처리 
        self.fiil_mean.clicked.connect(self.fillmean)
        self.fill_na.clicked.connect(self.fillna_func)

        # tocategorical 처리
        self.convert_btn.clicked.connect(self.convert_category)

        # column drop
        self.drop_btn.clicked.connect(self.dropc)

        #정규화
        self.scaler = self.findChild(QComboBox , "scaler")
        self.scale_btn = self.findChild(QPushButton , "scale_btn")

        self.scale_btn.clicked.connect(self.scale_value)

        # 산점도그래프
        self.scater_plot.clicked.connect(self.scatter_plot)


        # 꺽은선 그래프
        self.line_plot.clicked.connect(self.lineplot)

    def plot_heatmap(self):
        plt.figure()
        x = self.df[self.get_numeric()].corr()
        mask = np.triu(np.ones_like(x , dtype=np.bool))
        sns.heatmap(x , annot=True , mask=mask, vmin=1 , vmax=1)
        plt.show()

    def hist_add_column(self):
        print(self.hist_column.findText(self.hist_column.currentText()))
        self.hist_column_add.addItem(self.hist_column.currentText())
        self.hist_column.removeItem(self.hist_column.findText(self.hist_column.currentText()))
        

    def hist_remove_column(self):
        self.hist_column.addItem(self.hist_column_add.currentText())
        self.hist_column_add.removeItem(self.hist_column_add.findText(self.hist_column_add.currentText()))
        
    def histogram_plot(self):
        Allitems = [self.hist_column_add.itemText(i) for i in range(self.hist_column_add.count())]
        for i in Allitems:
            self.df.hist(column=i)
            plt.show()

    def scatter_plot(self):
        self.x = self.scater_x.currentText()
        self.y = self.scater_y.currentText()
        self.c = self.scater_c.currentText()
        self.marker = self.scater_mark.currentText()
        plt.figure()
        plt.scatter(self.df[self.x], self.df[self.y], c=self.c ,marker=self.marker)
        plt.xlabel(self.x)
        plt.ylabel(self.y)
        plt.title(f'{self.y} vs {self.x}')
        plt.show()
    
    def lineplot(self):
        self.x = self.line_x.currentText()
        self.y = self.line_y.currentText()
        self.c = self.line_c.currentText()
        self.marker = self.line_mark.currentText()
        plt.figure()
        plt.plot(self.df[self.x], self.df[self.y], c=self.c ,marker=self.marker)
        plt.xlabel(self.x)
        plt.ylabel(self.y)
        plt.title(f'{self.y} vs {self.x}')
        plt.show()

    def get_empty_list(self , df):
        empty_list= []
        for i in df.columns:
            if (df[i].isnull().values.any() == True):
                empty_list.append(i)
        return empty_list
    def get_numeric(self):
        numeric_col = []
        for i in self.df:
            if(self.df[i].dtype != 'object'):
                numeric_col.append(i)
        return numeric_col

    def filldetails(self, flag = 1):
        if (flag == 0):
            self.df = pd.read_csv(self.filepath,index_col=0, encoding='utf-8')
        
        self.columns.clear()
        self.column_list = []
        for i in self.df.columns:
            self.column_list.append(i)
        
        for i , j in enumerate(self.column_list):
            stri = f'{j} ------- {self.df[j].dtype}'
            self.columns.insertItem(i, stri)
        
        # print(self.column_list)

        self.cat_column.clear()
        self.cat_column.addItems(self.column_list)
        self.drop_column.clear()
        self.drop_column.addItems(self.column_list)
        self.empty_column.clear()
        self.empty_column.addItems(self.get_empty_list(self.df))
        self.scater_x.clear()
        self.scater_x.addItems(self.column_list)
        self.scater_y.clear()
        self.scater_y.addItems(self.column_list)
        self.line_x.clear()
        self.line_x.addItems(self.column_list)
        self.line_y.clear()
        self.line_y.addItems(self.column_list)
        self.hist_column.clear()
        self.hist_column.addItems(self.get_numeric())
        self.hist_column.addItem('All')
        
        


        x = table_display.DataFrameModel(self.df)
        self.tableView.setModel(x)
    
    def scale_value(self):
        x = self.df.drop(self.target_value, axis=1)
        scaler = self.scaler.currentText()
        if scaler == "StandardScale":
            scaled_features = StandardScaler().fit_transform(x)
            scaled_features_df = pd.DataFrame(scaled_features, index=x.index, columns=x.columns )
            scaled_features_df[self.target_value] = self.df[self.target_value]
            self.df = scaled_features_df
            self.filldetails()
        elif scaler == "MinMaxScale":
            scaled_features = MinMaxScaler().fit_transform(x)
            scaled_features_df = pd.DataFrame(scaled_features, index=x.index, columns=x.columns )
            scaled_features_df[self.target_value] = self.df[self.target_value]
            self.df = scaled_features_df
            self.filldetails()
        else :
            scaled_features = PowerTransformer().fit_transform(x)
            scaled_features_df = pd.DataFrame(scaled_features, index=x.index, columns=x.columns )
            scaled_features_df[self.target_value] = self.df[self.target_value]
            self.df = scaled_features_df
            self.filldetails()

    def dropc(self):
        if (self.drop_column.currentText() == self.target_value):
            self.target_value =""
            self.target_col.setText("")
        current_column = self.drop_column.currentText()
        self.df.drop(current_column, axis=1, inplace=True)
        self.filldetails()

    def convert_category(self):
        current_column = self.cat_column.currentText()
        self.df[current_column] = LabelEncoder().fit_transform(self.df[current_column])
        self.filldetails()

    def fillmean(self):
        current_column = self.empty_column.currentText()
        self.df[current_column] = self.df[current_column].fillna(self.df[current_column].mean())
        self.filldetails()

    def fillna_func(self):
        current_column = self.empty_column.currentText()
        self.df[current_column] = self.df[current_column].fillna(0)
        self.filldetails()

    def target(self):
        self.item = self.columns.currentItem().text().split()[0]
        print(self.item)

    def set_target(self):
        self.target_value = self.item
        self.target_col.setText(self.target_value)

    def get_csv(self):
        self.filepath , _ = QFileDialog.getOpenFileName(self, 'Open Csv File', '',"csv(*.csv)")
        # print(self.data)
        
        # print(df.info())
        self.filldetails(flag=0)
        # self.show()

   
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()

    sys.exit(app.exec_())