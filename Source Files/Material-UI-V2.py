import re
import os
import sys
import asyncio
import datetime
import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets

import aiohttp
import aiofiles

from database_manager import Manager

release = True
def exc_logger(exc_type,value,tb):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    directory = os.path.join(__location__, "log.txt")
    tme = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")  
    if not os.path.exists(directory):
        with open("log.txt","w") as f:
            f.write("%s\n"%(tme))
            f.write("Type: %s\nValue: %s\nTraceback: %s\n"%(exc_type,value,tb))
    else:
        with open("log.txt","a") as f:
            f.write("%s\n"%(tme))
            f.write("Type: %s\nValue: %s\nTraceback: %s\n"%(exc_type,value,tb))
if release == True:
    sys.excepthook = exc_logger

class Ui_w_MainWindow(object):
    def setupUi(self, w_MainWindow):
        w_MainWindow.setObjectName("w_MainWindow")
        w_MainWindow.setEnabled(True)
        w_MainWindow.resize(1024, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(w_MainWindow.sizePolicy().hasHeightForWidth())
        w_MainWindow.setSizePolicy(sizePolicy)
        w_MainWindow.setMinimumSize(QtCore.QSize(1024, 800))
        w_MainWindow.setMaximumSize(QtCore.QSize(1024, 800))
        w_MainWindow.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Data/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        w_MainWindow.setWindowIcon(icon)
        w_MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        w_MainWindow.setStyleSheet("background-color: rgb(98, 98, 98);")
        w_MainWindow.setDocumentMode(False)
        w_MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.wg_Central = QtWidgets.QWidget(w_MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_Central.sizePolicy().hasHeightForWidth())
        self.wg_Central.setSizePolicy(sizePolicy)
        self.wg_Central.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.wg_Central.setObjectName("wg_Central")
        self.b_StartDownload = QtWidgets.QPushButton(self.wg_Central)
        self.b_StartDownload.setGeometry(QtCore.QRect(-10, 730, 1041, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_StartDownload.sizePolicy().hasHeightForWidth())
        self.b_StartDownload.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.b_StartDownload.setFont(font)
        self.b_StartDownload.setStyleSheet("color: rgb(255, 255, 255);")
        self.b_StartDownload.setDefault(False)
        self.b_StartDownload.setFlat(True)
        self.b_StartDownload.setObjectName("b_StartDownload")
        self.l_DownloadBar = QtWidgets.QLabel(self.wg_Central)
        self.l_DownloadBar.setGeometry(QtCore.QRect(0, 729, 1031, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_DownloadBar.sizePolicy().hasHeightForWidth())
        self.l_DownloadBar.setSizePolicy(sizePolicy)
        self.l_DownloadBar.setStyleSheet("background-color: rgb(54, 54, 54);")
        self.l_DownloadBar.setText("")
        self.l_DownloadBar.setObjectName("l_DownloadBar")
        self.li_MaxImages = QtWidgets.QLineEdit(self.wg_Central)
        self.li_MaxImages.setGeometry(QtCore.QRect(10, 660, 191, 31))
        self.li_MaxImages.setText("")
        self.li_MaxImages.setObjectName("li_MaxImages")
        self.li_FolderName = QtWidgets.QLineEdit(self.wg_Central)
        self.li_FolderName.setGeometry(QtCore.QRect(10, 630, 191, 31))
        self.li_FolderName.setText("")
        self.li_FolderName.setObjectName("li_FolderName")
        self.li_Url = QtWidgets.QLineEdit(self.wg_Central)
        self.li_Url.setGeometry(QtCore.QRect(10, 570, 191, 31))
        self.li_Url.setStyleSheet("border-color: rgb(54, 54, 54);\n"
"gridline-color: rgb(54, 54, 54);")
        self.li_Url.setText("")
        self.li_Url.setFrame(True)
        self.li_Url.setObjectName("li_Url")
        self.pb_ProgressBar = QtWidgets.QProgressBar(self.wg_Central)
        self.pb_ProgressBar.setGeometry(QtCore.QRect(10, 700, 1001, 23))
        self.pb_ProgressBar.setProperty("value", 0)
        self.pb_ProgressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.pb_ProgressBar.setObjectName("pb_ProgressBar")
        self.cb_DisableAlert = QtWidgets.QCheckBox(self.wg_Central)
        self.cb_DisableAlert.setGeometry(QtCore.QRect(210, 570, 161, 17))
        self.cb_DisableAlert.setObjectName("cb_DisableAlert")
        self.cb_create_folder = QtWidgets.QCheckBox(self.wg_Central)
        self.cb_create_folder.setGeometry(QtCore.QRect(210, 590, 191, 18))
        self.cb_create_folder.setChecked(True)
        self.cb_create_folder.setObjectName("cb_create_folder")
        self.cb_resume_download = QtWidgets.QCheckBox(self.wg_Central)
        self.cb_resume_download.setGeometry(QtCore.QRect(210, 610, 211, 18))
        self.cb_resume_download.setObjectName("cb_resume_download")
        self.lb_picture = QtWidgets.QLabel(self.wg_Central)
        self.lb_picture.setGeometry(QtCore.QRect(0, 0, 1024, 300))
        self.lb_picture.setText("")
        self.lb_picture.setPixmap(QtGui.QPixmap("Data/img/header-image-1.png"))
        self.lb_picture.setScaledContents(True)
        self.lb_picture.setObjectName("lb_picture")
        self.li_separator = QtWidgets.QLineEdit(self.wg_Central)
        self.li_separator.setGeometry(QtCore.QRect(10, 600, 191, 31))
        self.li_separator.setText("")
        self.li_separator.setMaxLength(1)
        self.li_separator.setObjectName("li_separator")
        self.cb_auto_detect_links = QtWidgets.QCheckBox(self.wg_Central)
        self.cb_auto_detect_links.setGeometry(QtCore.QRect(210, 630, 231, 18))
        self.cb_auto_detect_links.setObjectName("cb_auto_detect_links")
        self.pb_select_custom_dir = QtWidgets.QPushButton(self.wg_Central)
        self.pb_select_custom_dir.setGeometry(QtCore.QRect(210, 660, 181, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(98, 98, 98))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(98, 98, 98))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(98, 98, 98))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(98, 98, 98))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(98, 98, 98))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(98, 98, 98))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(98, 98, 98))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(98, 98, 98))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(98, 98, 98))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.pb_select_custom_dir.setPalette(palette)
        self.pb_select_custom_dir.setAutoDefault(False)
        self.pb_select_custom_dir.setDefault(False)
        self.pb_select_custom_dir.setFlat(False)
        self.pb_select_custom_dir.setObjectName("pb_select_custom_dir")
        self.l_DownloadBar.raise_()
        self.b_StartDownload.raise_()
        self.li_MaxImages.raise_()
        self.li_FolderName.raise_()
        self.li_Url.raise_()
        self.pb_ProgressBar.raise_()
        self.cb_DisableAlert.raise_()
        self.cb_create_folder.raise_()
        self.cb_resume_download.raise_()
        self.lb_picture.raise_()
        self.li_separator.raise_()
        self.cb_auto_detect_links.raise_()
        self.pb_select_custom_dir.raise_()
        w_MainWindow.setCentralWidget(self.wg_Central)
        self.m_MenuBar = QtWidgets.QMenuBar(w_MainWindow)
        self.m_MenuBar.setGeometry(QtCore.QRect(0, 0, 1024, 22))
        self.m_MenuBar.setStyleSheet("background-color: rgb(54, 54, 54);\n"
"selection-background-color: rgb(98, 98, 98);\n"
"color: rgb(255, 255, 255);")
        self.m_MenuBar.setObjectName("m_MenuBar")
        self.m_Menu = QtWidgets.QMenu(self.m_MenuBar)
        self.m_Menu.setObjectName("m_Menu")
        self.m_Info = QtWidgets.QMenu(self.m_MenuBar)
        self.m_Info.setObjectName("m_Info")
        self.m_Help = QtWidgets.QMenu(self.m_MenuBar)
        self.m_Help.setObjectName("m_Help")
        w_MainWindow.setMenuBar(self.m_MenuBar)
        self.a_BuildInfo = QtWidgets.QAction(w_MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Data/img/i_Info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.a_BuildInfo.setIcon(icon2)
        self.a_BuildInfo.setObjectName("a_BuildInfo")
        self.a_Discord = QtWidgets.QAction(w_MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Data/img/i_Discord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.a_Discord.setIcon(icon3)
        self.a_Discord.setObjectName("a_Discord")
        self.a_Credits = QtWidgets.QAction(w_MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Data/img/i_Credits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.a_Credits.setIcon(icon4)
        self.a_Credits.setObjectName("a_Credits")
        self.a_Settings = QtWidgets.QAction(w_MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Data/img/i_Settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.a_Settings.setIcon(icon5)
        self.a_Settings.setObjectName("a_Settings")
        self.a_Exit = QtWidgets.QAction(w_MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Data/img/i_Exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.a_Exit.setIcon(icon6)
        self.a_Exit.setObjectName("a_Exit")
        self.a_Donate = QtWidgets.QAction(w_MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("Data/img/i_Donate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.a_Donate.setIcon(icon7)
        self.a_Donate.setObjectName("a_Donate")
        self.a_GitHub = QtWidgets.QAction(w_MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("Data/img/i_GitHub.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.a_GitHub.setIcon(icon8)
        self.a_GitHub.setObjectName("a_GitHub")
        self.m_Menu.addAction(self.a_Settings)
        self.m_Menu.addSeparator()
        self.m_Menu.addAction(self.a_Exit)
        self.m_Info.addAction(self.a_BuildInfo)
        self.m_Info.addAction(self.a_Discord)
        self.m_Info.addAction(self.a_Donate)
        self.m_Info.addSeparator()
        self.m_Info.addAction(self.a_Credits)
        self.m_Help.addAction(self.a_GitHub)
        self.m_MenuBar.addAction(self.m_Menu.menuAction())
        self.m_MenuBar.addAction(self.m_Info.menuAction())
        self.m_MenuBar.addAction(self.m_Help.menuAction())

        """
            Buttons connection section
        """
        
        self.a_Exit.triggered.connect(self.Exit)
        self.a_BuildInfo.triggered.connect(self.pu_BuildInfo)
        self.a_GitHub.triggered.connect(self.GitHub)
        self.a_Discord.triggered.connect(self.Discord)
        self.a_Credits.triggered.connect(self.pu_Credits)
        self.a_Donate.triggered.connect(self.Donate)
        self.a_Settings.triggered.connect(self.s_Settings)
        self.b_StartDownload.clicked.connect(self.wait_before_download)
        self.pb_select_custom_dir.clicked.connect(self.file_dialog)
        #LEGACY
        #self.b_Notification.clicked.connect(self.s_Notification)
        #self.b_Account.clicked.connect(self.s_Account)

        """
            Required variables
        """
        self.__database_manipulator = Manager(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))))
        self.custom_dir = None

        self.retranslateUi(w_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(w_MainWindow)

    def retranslateUi(self, w_MainWindow):
        """
            Disable this later
        """
        _translate = QtCore.QCoreApplication.translate
        w_MainWindow.setWindowTitle(_translate("w_MainWindow", "Multporn-Image-Downloader-v2"))
        self.b_StartDownload.setWhatsThis(_translate("w_MainWindow", "Start Download"))
        self.b_StartDownload.setText(_translate("w_MainWindow", "Download"))
        self.li_MaxImages.setPlaceholderText(_translate("w_MainWindow", "Maximum Images"))
        self.li_FolderName.setPlaceholderText(_translate("w_MainWindow", "Custom Folder Name"))
        self.li_Url.setPlaceholderText(_translate("w_MainWindow", "Links"))
        self.cb_DisableAlert.setText(_translate("w_MainWindow", "Disable Alerts"))
        self.cb_create_folder.setText(_translate("w_MainWindow", "Create new folder"))
        self.cb_resume_download.setText(_translate("w_MainWindow", "Resume Download"))
        self.li_separator.setPlaceholderText(_translate("w_MainWindow", "Separator (Default: \":\")"))
        self.cb_auto_detect_links.setText(_translate("w_MainWindow", "Automatically detect links"))
        self.pb_select_custom_dir.setText(_translate("w_MainWindow", "Select Custom Directory"))
        self.m_Menu.setTitle(_translate("w_MainWindow", "Menu"))
        self.m_Info.setTitle(_translate("w_MainWindow", "Info"))
        self.m_Help.setTitle(_translate("w_MainWindow", "Help"))
        self.a_BuildInfo.setText(_translate("w_MainWindow", "Build Info"))
        self.a_Discord.setText(_translate("w_MainWindow", "Discord"))
        self.a_Credits.setText(_translate("w_MainWindow", "Credits"))
        self.a_Settings.setText(_translate("w_MainWindow", "Settings"))
        self.a_Exit.setText(_translate("w_MainWindow", "Exit"))
        self.a_Donate.setText(_translate("w_MainWindow", "Donate"))
        self.a_GitHub.setText(_translate("w_MainWindow", "GitHub"))

    def file_dialog(self):
        self.custom_dir = str(QtWidgets.QFileDialog.getExistingDirectory(None,"Select Directory",os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))))

    def ProgressBar(self, max_img, complete = None):
        self.complete = complete
        if self.complete is None:
            self.complete = 0
        else:
            complete += 1
        prog_val = (complete/max_img)*100
        prog_val = int(str(prog_val).split(".")[0])
        self.pb_ProgressBar.setValue(prog_val)

    # Exit Application
    def Exit(self):
        quit()
    
    # Pop-Up Credits
    def pu_Credits(self):
        msg1 = QtWidgets.QMessageBox()
        msg1.setWindowTitle("Credits")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("Data/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg1.setWindowIcon(icon8)
        msg1.setText("UI Coming Soon!\nIn the meantime:\nOriginal creator: Husko\nContributor: oguh43/ MIAU\nTester: drache")
        msg1.setIcon(QtWidgets.QMessageBox.Information)
        msg1.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg1.setDefaultButton(QtWidgets.QMessageBox.Ok)
        x = msg1.exec()

    # Pop-Up Build Info
    def pu_BuildInfo(self):
        msg2 = QtWidgets.QMessageBox()
        msg2.setWindowTitle("Build Info")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("Data/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg2.setWindowIcon(icon8)
        msg2.setText("Current Build Version: v3.0p")
        msg2.setIcon(QtWidgets.QMessageBox.Information)
        msg2.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg2.setDefaultButton(QtWidgets.QMessageBox.Ok)

        x = msg2.exec()

    # GitHub Redirect
    def GitHub(self):
        ws_GitHub = "https://cutt.ly/multporn-image-downloader-v2_info"
        webbrowser.open_new_tab(ws_GitHub)

    # Discord Redirect
    def Discord(self):
        ws_Discord = "https://cutt.ly/main-invite"
        webbrowser.open_new_tab(ws_Discord)

    # Donate/Patreon Redirect
    def Donate(self):
        ws_Donate = "https://cutt.ly/donation-variant-2"
        webbrowser.open_new_tab(ws_Donate)

    # Account System (Currently not implemented)
    def s_Account(self):
        msg3 = QtWidgets.QMessageBox()
        msg3.setWindowTitle("Account")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("Data/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg3.setWindowIcon(icon8)
        msg3.setText("Account Function Coming Soon!")
        msg3.setIcon(QtWidgets.QMessageBox.Information)
        msg3.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg3.setDefaultButton(QtWidgets.QMessageBox.Ok)

        x = msg3.exec()

    # Notification System (Currently not implemented)
    def s_Notification(self):
        msg4 = QtWidgets.QMessageBox()
        msg4.setWindowTitle("Notifications")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("Data/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg4.setWindowIcon(icon8)
        msg4.setText("Notifications Function Coming Soon!")
        msg4.setIcon(QtWidgets.QMessageBox.Information)
        msg4.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg4.setDefaultButton(QtWidgets.QMessageBox.Ok)

        x = msg4.exec()

         # Settings System (Currently not implemented)
    def s_Settings(self):
        msg5 = QtWidgets.QMessageBox()
        msg5.setWindowTitle("Settings")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("Data/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg5.setWindowIcon(icon8)
        msg5.setText("Settings Function Coming Soon!")
        msg5.setIcon(QtWidgets.QMessageBox.Information)
        msg5.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg5.setDefaultButton(QtWidgets.QMessageBox.Ok)

        x = msg5.exec()
    
    async def pu_starting(self, s_max):
        msg7 = QtWidgets.QMessageBox()
        msg7.setWindowTitle("Starting")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("Data/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg7.setWindowIcon(icon8)
        msg7.setText("Started Downloading: " + str(s_max))
        msg7.setIcon(QtWidgets.QMessageBox.Information)
        msg7.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg7.setDefaultButton(QtWidgets.QMessageBox.Ok)
        x = msg7.exec()

    def wait_before_download(self):
        asyncio.run(self.execute_downloader())
    
    async def get_source(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()
            
    async def refresh_gui(self,prog=False,max_img = None,prog_val=None):
        if prog == True:
            self.ProgressBar(max_img,prog_val)
        QtCore.QCoreApplication.processEvents()

    async def execute_downloader(self):
        if self.li_Url.text().count("https") != 1:
            if self.cb_auto_detect_links.isChecked():
                s_URL_list = ["https"+link for link in self.li_Url.text().split("https")][1:]
            else:
                s_URL_list = ["https:"+link for link in self.li_Url.text().split(self.li_separator.text() if self.li_separator.text() != "" else ":") if "https" not in link]
        else:
            s_URL_list = [self.li_Url.text()]
        for checkbox in [self.cb_DisableAlert,self.cb_auto_detect_links,self.cb_resume_download,self.cb_create_folder,self.pb_select_custom_dir]:
            checkbox.setEnabled(False)
        for s_URL in s_URL_list:
            s_Folder = self.li_FolderName.text()
            s_Max = self.li_MaxImages.text()
            broken = False
            r1 = await self.get_source(s_URL)
            r1 = r1.decode("utf-8")
            r2 = r1
            prog_val = 0
            links = re.findall(r'(?<={}).*?(?={})'.format("<p class=\"jb-image\"><img src=\"","\" alt=\"\" /><br/></p>"), r1)
            if s_Folder == "" and self.custom_dir is None:
                s_Folder = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))),s_URL.split("/")[-1])
            elif self.custom_dir is not None and s_Folder != "":
                s_Folder = self.custom_dir+"/"+s_Folder
            elif self.custom_dir is not None and s_Folder == "" and self.cb_create_folder.isChecked():
                s_Folder = os.path.join(self.custom_dir,s_URL.split("/")[-1])
            elif self.custom_dir is not None and s_Folder == "" and not self.cb_create_folder.isChecked():
                s_Folder = self.custom_dir
            else:
                s_Folder = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))),s_Folder)
            for i in links:
                if "?itok=" in i:
                    broken = True
            if broken == True:
                links = re.findall(r'(?<={}).*?(?={})'.format("<p class=\"jb-image\"><img src=\"","\?itok="), r2)

            count = 0
            """if self.custom_dir is None:
                temp_folder = s_Folder
            else:
                temp_folder = self.custom_dir"""
            
            temp_folder = s_Folder
            if self.__database_manipulator.exists(s_URL.split("/")[-1]):
                db_custom_name, db_path, db_pages = self.__database_manipulator.get_data(s_URL.split("/")[-1])

            while True and self.cb_create_folder.isChecked() and not self.cb_resume_download.isChecked():
                if not os.path.exists(temp_folder):
                    os.mkdir(temp_folder)
                    s_Folder = temp_folder
                    break
                else:
                    count += 1
                    temp_folder = s_Folder +"_"+ str(count)
            if self.cb_resume_download.isChecked():
                s_Folder = db_path
            orig_links = links.copy()
            if s_Max == "" or int(s_Max) > len(links):
                s_Max = int(len(links))
            if s_Max != len(links):
                links = links[:int(s_Max)]
            if not self.cb_DisableAlert.isChecked() and not self.cb_resume_download.isChecked() and len(s_URL_list)==1:
                await self.pu_starting(len(links))
            elif not self.cb_DisableAlert.isChecked() and self.cb_resume_download.isChecked() and len(s_URL_list)==1:
                await self.pu_starting(len(links)-len(db_pages))
            new_pages = []
            if not self.cb_resume_download.isChecked():
                max_prog = len(links)
            else:
                max_prog = len(links)-len(db_pages)
            for img_link in links:
                new_pages.append(orig_links.index(img_link))
                if self.cb_resume_download.isChecked():
                    if orig_links.index(img_link) in db_pages:
                        continue
                img_type = "." + img_link.split(".")[-1]
                prog_val += 1
                await self.refresh_gui(True,max_prog,prog_val)
                img_data = await self.get_source(img_link)
                try:
                    img_data.decode("utf-8")
                    continue
                except UnicodeDecodeError:
                    pass
                if self.cb_create_folder.isChecked():
                    async with aiofiles.open(s_Folder+"\\"+str(orig_links.index(img_link)+1)+img_type, 'wb+') as f:
                        await f.write(img_data)
                else:
                    async with aiofiles.open(s_Folder+"\\"+str(orig_links.index(img_link)+1)+img_type,"wb") as f:
                        await f.write(img_data)

            if not self.__database_manipulator.exists(s_URL.split("/")[-1]):
                self.__database_manipulator.create_record(s_URL.split("/")[-1],s_URL.split("/")[-1],s_Folder,new_pages)
            else:
                self.__database_manipulator.update_pages(s_URL.split("/")[-1],new_pages)
                if db_path != s_Folder:
                    self.__database_manipulator.update_path(s_URL.split("/")[-1],s_Folder)

        """
        Legacy
        """
        #path, dirs, files = next(os.walk(s_Folder))

        if not self.cb_DisableAlert.isChecked():
            msg6 = QtWidgets.QMessageBox()
            msg6.setWindowTitle("Finished Downloading")
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap("Data/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            msg6.setWindowIcon(icon8)
            if not self.cb_resume_download.isChecked():
                msg6.setText("Total Images Downloaded: " + str(len(links)))
            else:
                msg6.setText("Total Images Downloaded: " + str(len(links)-len(db_pages)))
            msg6.setIcon(QtWidgets.QMessageBox.Information)
            msg6.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg6.setDefaultButton(QtWidgets.QMessageBox.Ok)
            x = msg6.exec()
        
        self.pb_ProgressBar.setValue(0)
        self.li_Url.setText("")
        for checkbox in [self.cb_DisableAlert,self.cb_auto_detect_links,self.cb_resume_download,self.cb_create_folder,self.pb_select_custom_dir]:
            checkbox.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w_MainWindow = QtWidgets.QMainWindow()
    ui = Ui_w_MainWindow()
    ui.setupUi(w_MainWindow)
    w_MainWindow.show()
    sys.exit(app.exec_())
#TODO: 
#   rework "Finished Downloading" to be accurate when encountering missing images
#
#
#
#
#
