from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtNetwork import QNetworkProxy
import os
import sys
from getpass import getuser
import darkdetect
from style import stylesheet
from setting import load_setting
import image

engine = "https://google.com"
user = getuser()

class MyWindow(QMainWindow):
    def __init__(self, *args, **kwargs):

        super(QMainWindow, self).__init__(*args, **kwargs)

        self.setBaseSize(500, 350)
        self.setWindowIcon(QIcon(':/image/meta/ico.png'))

        browser_setting = QWebEngineSettings.defaultSettings()
        browser_setting.setAttribute(QWebEngineSettings.SpatialNavigationEnabled, True)
        browser_setting.setAttribute(QWebEngineSettings.ShowScrollBars, False)


        self.proxy = QNetworkProxy()
        self.set_setting()


        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(stylesheet[theme]["central_widget"])
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.status.setStyleSheet(stylesheet[theme]["body"])
        self.setStatusBar(self.status)

        navtb = QToolBar("")
        navtb.setStyleSheet(stylesheet[theme]["body"])
        navtb.setFloatable(False)
        navtb.setMovable(False)
        self.addToolBar(navtb)

        about_btn = QAction('', self)
        about_btn.setIcon(QIcon(':/image/meta/github.png'))
        about_btn.setStatusTip("GitHub project")
        about_btn.triggered.connect(
            lambda: self.add_new_tab(qurl=QUrl("https://github.com/kinite-gp"), label="kinite-gp"))

        back_btn = QAction("", self)
        back_btn.setIcon(QIcon(':/image/meta/back.png'))
        back_btn.setStatusTip("Go to the previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction("", self)
        next_btn.setIcon(QIcon(':/image/meta/forward.png'))
        next_btn.setStatusTip("Go to the next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        self.reload_btn = QAction("", self)
        self.reload_btn.setIcon(QIcon(':/image/meta/reload.png'))
        self.reload_btn.setStatusTip("Reload the page")
        self.reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(self.reload_btn)

        home_btn = QAction("", self)
        home_btn.setIcon(QIcon(':/image/meta/home.png'))
        home_btn.setStatusTip("Going home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.setStyleSheet(stylesheet[theme]["body"])
        font = QFont()
        font.setPointSize(11)
        self.urlbar.setFont(font)
        self.urlbar.setStatusTip('To enter and see the URL of the site')
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        print_btn = QAction('', self)
        print_btn.setIcon(QIcon(':/image/meta/pdf.png'))
        print_btn.setStatusTip('Save the site as PDF')
        print_btn.triggered.connect(self.printer)

        new_tab = QAction('', self)
        new_tab.setIcon(QIcon(":/image/meta/new.png"))
        new_tab.setStatusTip("Open a new tab")
        new_tab.triggered.connect(self.tab_open_doubleclick)

        reload_setting = QAction('', self)
        reload_setting.setIcon(QIcon(":/image/meta/setting.png"))
        reload_setting.setStatusTip("Reload the settings from the settings file")
        reload_setting.triggered.connect(self.set_setting)


        navtb.addAction(new_tab)
        navtb.addAction(reload_setting)
        navtb.addAction(print_btn)
        navtb.addAction(about_btn)

        self.add_new_tab(QUrl(engine), 'Homepage')
        self.show()
        self.setWindowTitle("Browthon")


    def set_setting(self):
        global engine
        setting = load_setting()
        engine = setting["home_url"]
        if setting["proxy"]["status"]:
            self.proxy.setType(QNetworkProxy.HttpProxy)
            self.proxy.setHostName(f'{setting["proxy"]["host"]}')
            self.proxy.setPort(setting["proxy"]["port"])
            if setting["proxy"]["login"]["status"]:
                self.proxy.setUser(setting["proxy"]["login"]["user"])
                self.proxy.setPassword((setting["proxy"]["login"]["pass"]))
        else:
            self.proxy.setType(QNetworkProxy.DefaultProxy)
        QNetworkProxy.setApplicationProxy(self.proxy)


    def on_load_started(self, i, b):
        self.tabs.setTabText(i, b)
        self.reload_btn.setIcon(QIcon(':/image/meta/stop.png'))
        self.reload_btn.setStatusTip("Stop loading the page")
        self.reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())


    def on_load_finished(self, i, b):
        self.tabs.setTabText(i,b)
        self.reload_btn.setIcon(QIcon(':/image/meta/reload.png'))
        self.reload_btn.setStatusTip("Reload the page")
        self.reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())



    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl(engine)

        self.browser = QWebEngineView()
        self.browser.setStyleSheet(stylesheet[theme]["body"])
        self.browser.setUrl(qurl)
        i = self.tabs.addTab(self.browser, label)
        self.tabs.setCurrentIndex(i)
        self.browser.urlChanged.connect(lambda qurl, browser=self.browser:
                                        self.update_urlbar(qurl, browser))


        self.browser.loadFinished.connect(lambda: self.on_load_finished(i, self.browser.page().title()))
        self.browser.loadProgress.connect(lambda: self.on_load_started(i, self.browser.page().title()))

    def tab_open_doubleclick(self):
        self.add_new_tab()


    def current_tab_changed(self):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())


    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)


    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s" % title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl(engine))


    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())

        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)


    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def printer(self):
        self.browser.page().printToPdf(f"C:/Users/{user}/Downloads/{self.browser.page().title().replace('|','')}.pdf")
        QMessageBox.information(self, 'info',
                                f'exporting file to:\n"C:/Users/{user}/Downloads/{self.browser.page().title()}.pdf"')


if __name__ == "__main__":
    if darkdetect.isDark():
        theme = "dark"
        os.environ[
            "QTWEBENGINE_CHROMIUM_FLAGS"
        ] = "--blink-settings=darkMode=4,darkModeImagePolicy=2"
        app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
        app.setStyleSheet(stylesheet[theme]["tooltip"])
    else:
        theme = "light"
        app = QApplication(sys.argv)


    QToolTip.hideText()
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
