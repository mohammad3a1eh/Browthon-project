#
# The project of building a browser with Python language
# Developer: https://github.com/kinite-GP
#


#
# Import Pyqt5 and other library 
#


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys
from getpass import getuser

pwd = os.getcwd().replace('\\','/')



# 
# set search engine default and get user name system (for save pdf site)
#


engine = f"{pwd}/metadata/index.html"
user = getuser()



#
# Main windows class
#


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        
        
        #
        # set icon windows
        #
        

        self.setBaseSize(500,350)
        self.setWindowIcon(QIcon('metadata/ico.png'))


        
        
        #
        # tab builder
        #
        
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)
        
        
        #
        # status bar builder
        #
        
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        

        
        

        
        #
        # nav bar builder (for icons and btn)
        #
        
        
        navtb = QToolBar("Navigation")
        navtb.setFloatable(False)
        navtb.setMovable(False)
        self.addToolBar(navtb)
        
        
        datetb = QToolBar('tools')
        datetb.setFloatable(False)
        datetb.setMovable(False)
        datetb.setGeometry(0,0,100,20)
        self.addToolBar(Qt.LeftToolBarArea,datetb)
        


        #
        # about btn
        #
        
        
        about_btn = QAction('about', self)
        about_btn.setIcon(QIcon('metadata/about.png'))
        about_btn.setStatusTip("about developer")
        about_btn.triggered.connect(self.about)
        
        
        
        #
        # beck btn
        #
        
        
        back_btn = QAction("Back", self)
        back_btn.setIcon(QIcon('metadata/back.png'))
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)
        
        
        #
        # next btn
        #
        
        
        next_btn = QAction("Forward", self)
        next_btn.setIcon(QIcon('metadata/next.png'))
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)
        
        
        #
        # reload_btn
        #
        
        
        reload_btn = QAction("Reload", self)
        reload_btn.setIcon(QIcon('metadata/reload.png'))
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
        
        
        #
        # home btn
        #
        
               
        home_btn = QAction("Home", self)
        home_btn.setIcon(QIcon('metadata/home.png'))
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
 
        
        navtb.addSeparator() # add line to nav bar (seprator)
        
        
        #
        # url bar builder
        #
        
        
        self.urlbar = QLineEdit()
        self.urlbar.setStatusTip('url site')
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        
        
        
        #
        # stop loading btn
        #
        
        
        stop_btn = QAction("Stop", self)
        stop_btn.setIcon(QIcon('metadata/stop.png'))
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
        
        
        #
        # site to pdf creator (print!?)
        #
        
        
        print_btn = QAction('print', self)
        print_btn.setIcon(QIcon('metadata/print.png'))
        print_btn.setStatusTip('site save to pdf')
        print_btn.triggered.connect(self.printer)
        navtb.addAction(print_btn)
        navtb.addAction(about_btn)
        
        
        #
        # create start tab
        #
        
        
        self.add_new_tab(QUrl(engine), 'Homepage')
        self.show()
        self.setWindowTitle("Browthon")
        
        
        
        
        
        
        

        
    
        
    

    #
    # new tab builder
    #    
        

    def add_new_tab(self, qurl = None, label ="Blank"):
 

        if qurl is None:
            qurl = QUrl(engine)
 
        self.browser = QWebEngineView()
        self.browser.setUrl(qurl)
        i = self.tabs.addTab(self.browser, label)
        self.tabs.setCurrentIndex(i)
        self.browser.urlChanged.connect(lambda qurl, browser = self.browser:
                                   self.update_urlbar(qurl, browser))

        self.browser.loadFinished.connect(lambda _, i = i, browser = self.browser:
                                     self.tabs.setTabText(i, browser.page().title()))
 
 
    #
    # new tab builder with double click
    #
    

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()
 

    #
    # switch tab function
    #


    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())
 

    #
    # close tab function
    #


    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)


    #
    # update tab title
    #
    

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
 
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s" % title)
 

    #
    # open home page
    #


    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl(engine))
 

    #
    # open url
    #


    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
 
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)
 

    #
    # update url bar
    #


    def update_urlbar(self, q, browser = None):
        if browser != self.tabs.currentWidget():
            return
 
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
        
        
    #
    # site save to pdf
    #

        
    def printer(self):
        self.browser.page().printToPdf(f"C:/Users/{user}/Downloads/{self.browser.page().title()}.pdf")
        QMessageBox.information(self, 'info', f'exporting file to:\n"C:/Users/{user}/Downloads/{self.browser.page().title()}.pdf"')

        
        
        
    def about(self):
        self.add_new_tab(QUrl("https://github.com/kinite-gp"), 'kinite_gp')
        self.browser.page().runJavaScript("submitted()",self.ready)
        
       
#
# run and loop
#


app = QApplication(sys.argv)
app.setApplicationName("Browthon")
window = MainWindow()
app.exec_()