# from fbs_runtime.application_context import ApplicationContext
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import interface
from PyQt5 import *
import os
import sys
import webbrowser
import pickle
import preprocess




if PYQT_VERSION_STR !='5.9.2':
    print('\n')
    print('Dear User:')
    print('pyqt5 version is not satisfied, please reinstall version 5.9.2')
    print('\n')
    exit(1)
    


lst = [u"External Risk Estimate",u"Months Since Oldest Trade Open", u"Months Since Most Recent Trade Open", 
u"Average Months in File", u"Number Satisfactory Trades", u"Number Trades 60+ Ever",
 u"Number Trades 90+ Ever", u"Percent Trades Never Delinquent", u"Months Since Most Recent Delinquency",
  u"last year Max Public Records", u"Max Delinquency Ever", u"Number of Total Trades", u"Number of Trades Open in Last 12 Months", u"Percent Installment Trades",
   u"Months Since Most Recent Inq excl 7days",u'Num Inq Last 6Months',u'Num Inq Last 6M excl 7days', u"Net Fraction Revolving Burden.", u"Net Fraction Installment Burden", u"Number Revolving Trades with Balance", 
   u"Number Installment Trades with Balance", u"Number Bank Trades w high utilization ratio", u"Percent Trades with Balance"]
parameters=[]
values=[]
printImage=True

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')   
        


class MyApp(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setWindowTitle("House Loan Pro 1.0")
        self.setupUi(self)
        self.show_img.clicked.connect(self.print_img)
        self.hid_img.clicked.connect(self.hidd)
        self.model_box.activated.connect(self.handleActivated)
        self.clear.clicked.connect(self.clear_line)
        self.help.clicked.connect(self.on_pushButton_clicked)
        self.predict_button.clicked.connect(self.prediction)
        self.save.clicked.connect(self.save_file)
        init_image_path='../important_image/heatmap.png'
        # print(init_image_path)
            # 'img.png' #path to your image file
        image = QtGui.QImage(QtGui.QImageReader(init_image_path).read()).scaled(330,221, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.img_label.setPixmap(QtGui.QPixmap(image))
        self.initUI()





    def save_file(self):
        try:
            if self.filename.text()=='':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Please enter a file name")
                msg.setWindowTitle("Error")
                msg.exec_()            
            else:
                path=get_download_path()
                text=self.notebook.toPlainText()
                fname=self.filename.text()
                with open(path+'/'+fname+'.txt', 'w') as f:
                    f.write(text)
                self.filename.clear()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("text file "+fname+".txt saved")
                msg.setWindowTitle("Reminder")
                msg.exec_() 
                print('pass')
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Unknow Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()



    def on_pushButton_clicked(self):
        msg = QMessageBox()
        msg.setWindowTitle("Help")
        result=msg.information(self,'Information',"detailed information please visite the website",QMessageBox.Open|QMessageBox.Cancel)
        # replay=msg.Information(self,)
        if  result==QMessageBox.Open:
            
            webbrowser.open('https://community.fico.com/s/explainable-machine-learning-challenge')
        else:
            msg.close()

            
    def clear_line(self):
        # print('connect')
        for x in parameters:
            x.clear()

    def handleActivated(self, index):
        print(self.model_box.itemText(index))
    def print_img(self):
        self.img_label.clear()
        if self.model_box.currentText()=='None':
            image_path='../important_image/heatmap.png'
            print(image_path)
            image = QtGui.QImage(QtGui.QImageReader(image_path).read()).scaled(330,221, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            print(image)
            self.img_label.setPixmap(QtGui.QPixmap(image))

        elif self.model_box.currentText()=='SVM':
            image_path='../important_image/SVM_.png'
            image = QtGui.QImage(QtGui.QImageReader(image_path).read()).scaled(330,221, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.img_label.setPixmap(QtGui.QPixmap(image))

        elif self.model_box.currentText()=='LR':
            image_path='../important_image/LR_.png'
            image = QtGui.QImage(QtGui.QImageReader(image_path).read()).scaled(330,221, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.img_label.setPixmap(QtGui.QPixmap(image))

        elif self.model_box.currentText()=='KNN':
            image_path='../important_image/heatmap.png'
            image = QtGui.QImage(QtGui.QImageReader(image_path).read()).scaled(330,221, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.img_label.setPixmap(QtGui.QPixmap(image))

        elif self.model_box.currentText()=='NB':
            image_path='../important_image/heatmap.png'
            image = QtGui.QImage(QtGui.QImageReader(image_path).read()).scaled(330,221, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.img_label.setPixmap(QtGui.QPixmap(image))

        elif self.model_box.currentText()=='Tree':
            image_path='../important_image/Tree_.png'
            image = QtGui.QImage(QtGui.QImageReader(image_path).read()).scaled(330,221, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.img_label.setPixmap(QtGui.QPixmap(image))

        elif self.model_box.currentText()=='RF':
            image_path='../important_image/RF_.png'
            image = QtGui.QImage(QtGui.QImageReader(image_path).read()).scaled(330,221, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.img_label.setPixmap(QtGui.QPixmap(image))

        elif self.model_box.currentText()=='Boosting':
            image_path='../important_image/Boosting_.png'
            image = QtGui.QImage(QtGui.QImageReader(image_path).read()).scaled(330,221, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.img_label.setPixmap(QtGui.QPixmap(image))


        # print(os.getcwd())

        # image_path='heatmap.png'
        # # 'img.png' #path to your image file
        # image = QtGui.QImage(QtGui.QImageReader(image_path).read()).scaled(330,221, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        # self.img_label.setPixmap(QtGui.QPixmap(image))

        # self.show_frame_in_display(image_path)
    def hidd(self):
        self.img_label.clear()

    def error_message(self,place):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("There is an Error in "+ place)
        msg.setInformativeText('More information')
        msg.setWindowTitle("Error")
        msg.exec_()


    def createLayout_group(self, number):
        sgroupbox = QGroupBox("Input Values", self)
        layout_groupbox = QVBoxLayout(sgroupbox)
        for i in range(len(lst)):
            item = QLineEdit( sgroupbox)
            item.setPlaceholderText(lst[i]) 
            # item.setObjectName("input"+str(i))
            item.setValidator(QtGui.QDoubleValidator())
            parameters.append(item)

            # print(item.getObjectName)
            layout_groupbox.addWidget(item)
        layout_groupbox.addStretch(2)
        return sgroupbox

    def createLayout_Container(self):
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setFixedWidth(310)
        self.scrollarea.setFixedHeight(150)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget()
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)

        # for i in range(5):
        self.layout_SArea.addWidget(self.createLayout_group(0))
        self.layout_SArea.addStretch(1)
    def initUI(self):
        self.createLayout_Container()
        # self.layout_All = QVBoxLayout(self)
        # self.layout_All.addWidget(self.scrollarea)
        self.scrollarea.move(70,100)
        self.setWindowTitle("House Loan Pro 1.0")
        # print(self.input1)
        self.show()
    def prediction(self):

        next=False

                
        text_value=[x.text()for x in parameters]
        for i in range(len(text_value)):
            if text_value[i]=='' :
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Empty Input Value")
                msg.setInformativeText('please enter all input values')
                msg.setWindowTitle("Error")
                msg.exec_()
                break
            elif text_value[i]=='e':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Invalid Input")
                msg.setInformativeText('Input must be number!!')
                msg.setWindowTitle("Error")
                msg.exec_()
                break
            elif i == len(text_value)-1:
                next=True



        if next:
            predict_next=True
            try:
                values=[float(x.text()) for x in parameters]
            except Exception as e:
                predict_next=False
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Unknow Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()

            if predict_next:
                print(str(self.model_box.currentText()))  
                if self.model_box.currentText()=='None':
                    self.output.setText('')
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Please Select a Model")
                    msg.setInformativeText('Assign model before each prediction')
                    msg.setWindowTitle("Error")
                    msg.exec_()

                elif self.model_box.currentText()=='SVM':
                    self.output.clear()
                    self.comment.clear()
                    text1,text2=preprocess.preprocess(values,'SVM')
                    self.output.setText(text1)
                    self.comment.setText(text2)
                    print(text2)
                elif self.model_box.currentText()=='LR':
                    text1,text2=preprocess.preprocess(values,'LR')
                    self.output.setText(text1)
                    self.comment.setText(text2)
                elif self.model_box.currentText()=='KNN':
                    text1,text2=preprocess.preprocess(values,'KNN')
                    self.output.setText(text1)
                    self.comment.setText(text2)
                elif self.model_box.currentText()=='NB':
                    text1,text2=preprocess.preprocess(values,'NB')
                    self.output.setText(text1)
                    self.comment.setText(text2)
                elif self.model_box.currentText()=='Tree':
                    text1,text2=preprocess.preprocess(values,'Tree')
                    self.output.setText(text1)
                    self.comment.setText(text2)
                elif self.model_box.currentText()=='RF':
                    text1,text2=preprocess.preprocess(values,'RF')
                    self.output.setText(text1)
                    self.comment.setText(text2)
                elif self.model_box.currentText()=='Boosting':
                    text1,text2=preprocess.preprocess(values,'Boosting')
                    self.output.setText(text1)
                    self.comment.setText(text2)

                print('finished')
     

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    # window.
    window.show()
    sys.exit(app.exec_())






