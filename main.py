import configparser
from msilib.schema import SelfReg
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow,QFileDialog,QLineEdit,QGridLayout,QInputDialog,QLabel
from PyQt6.QtGui import QIcon, QAction
import os
from compressor import Compressor
import time
class MLineEdit(QLineEdit):
    def __init__(self, title, main, video):
        super().__init__(title, main)
        self.setAcceptDrops(True)
        self.main = main
        self.video = video

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        filePathList = e.mimeData().text()
        filePath = filePathList.split('\n')[0] #拖拽多文件只取第一个地址
        filePath = filePath.replace('file:///', '', 1) #去除文件地址前缀的特定字符
        self.setText(filePath)
        if(self.video):
            self.main.set_root(filePath)

class MainWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(os.path.dirname(__file__),'config.ini')
        self.config.read(self.config_path,encoding='utf-8')
        self.__default_input_path = self.__default_subtitle_path = self.__default_output_path = self.config['DEFAULT']['root']
        self.__default_prefix = self.config['DEFAULT']['prefix']

    def initUI(self):

        centralWidget = QWidget()
        grid = QGridLayout()

        # 状态栏
        self.statusBar = self.statusBar()
        # self.statusBar.showMessage('Ready')
        self.statusLabel = QLabel(' Ready')
        self.statusBar.addPermanentWidget(self.statusLabel, stretch=1)
        self.statusBar.setSizeGripEnabled(False)

        # 菜单栏
        menubar = self.menuBar()
        settingMenu = menubar.addMenu('Setting')
        defaultPrefix = QAction('输出前缀',self)
        defaultRoot = QAction('默认路径',self)
        settingMenu.addAction(defaultPrefix)
        settingMenu.addAction(defaultRoot)
        
        defaultPrefix.triggered.connect(self.setPrefix)
        defaultRoot.triggered.connect(self.setRoot)

        # defaultPrefix.setStatusTip('Setting')
        # defaultRoot.setStatusTip('Setting')

        # 视频
        self.input_lineEdit = MLineEdit('',self,True)
        self.input_lineEdit.setPlaceholderText('视频文件，可拖拽')
        self.input_pushButton = QPushButton('视频')
        grid.addWidget(self.input_lineEdit,0,1)
        grid.addWidget(self.input_pushButton,0,2)
        self.input_lineEdit.setReadOnly(True)
        

        # 字幕
        self.subtitle_lineEdit = MLineEdit('',self,False)
        self.subtitle_lineEdit.setPlaceholderText('字幕文件，可拖拽')
        self.subtitle_pushButton = QPushButton('字幕')
        grid.addWidget(self.subtitle_lineEdit,1,1)
        grid.addWidget(self.subtitle_pushButton,1,2)
        self.subtitle_lineEdit.setReadOnly(True)

        # 输出
        self.output_lineEdit = QLineEdit('')
        self.output_pushButton = QPushButton('输出')
        grid.addWidget(self.output_lineEdit,2,1)
        grid.addWidget(self.output_pushButton,2,2)

        # 事件绑定
        self.input_pushButton.clicked.connect(self.select_input_file)
        self.subtitle_pushButton.clicked.connect(self.select_subtitle_file)
        self.output_pushButton.clicked.connect(self.select_output_file)   

        # 压制按钮
        cbtn = QPushButton('压制',self)
        grid.addWidget(cbtn,3,1)
        cbtn.clicked.connect(self.compressor)

        # 退出按钮
        qbtn = QPushButton('退出', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        grid.addWidget(qbtn,3,2)

        self.setFixedSize(400, 200)
        self.center()

        self.setWindowTitle('FFmpeg Subtitle Compressor')
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)
        self.show()

    # 窗口居中
    def center(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 压制
    def compressor(self):
        input_path = self.input_lineEdit.text()
        subtitle_path = self.subtitle_lineEdit.text()
        output_path = self.output_lineEdit.text()

        check,msg = self.perCheck(input_path,subtitle_path,output_path)
        self.statusBar.showMessage(msg)
        if(check):
            self.statusLabel.setText('Running...')
            time.sleep(2)
            # Compressor(input_path,subtitle_path,output_path)
            self.statusLabel.setText('1')
            time.sleep(2)
            self.statusLabel.setText('2')
            time.sleep(2)
            self.statusLabel.setText('3')
            # self.statusBar.showMessage(Compressor(input_path,subtitle_path,output_path))
            self.clear()
        

    # 前缀
    def setPrefix(self):
        text,ok = QInputDialog.getText(self,'Setting','默认输出前缀:')
        if (ok and text != ''):
            self.__default_prefix = str(text)
            self.config['DEFAULT']['prefix'] = str(text)
            with open(self.config_path,'w',encoding = 'utf-8') as configfile:
                self.config.write(configfile)

    # 根目录
    def setRoot(self):
        home_dir = './'
        dirpath = QFileDialog.getExistingDirectory(self, 'Open file', home_dir)

        if (dirpath):
            self.__default_input_path = self.__default_subtitle_path = self.__default_output_path = dirpath
            self.config['DEFAULT']['root'] = dirpath
            with open(self.config_path,'w',encoding = 'utf-8') as configfile:
                self.config.write(configfile)
    
    def select_input_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, '选择视频文件',self.__default_input_path,"Video (*.mp4;*.flv;*.mkv;*.avi;*.wmv;*.mpg;*.avs);;All Files (*.*)")
        if(filepath!=''):
            self.input_lineEdit.setText(filepath)
            self.set_root(filepath)

    def select_subtitle_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选择字幕文件",self.__default_subtitle_path,"Subtitle (*.ass;*.ssa;*.srt);;All Files (*.*)")
        if(filepath != ''):
            self.subtitle_lineEdit.setText(filepath)

    def select_output_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "输出至",self.__default_output_path + '',"Video (*.mp4;*.flv;*.mkv;*.avi;*.wmv;*.mpg;*.avs);;All Files (*.*)")
        self.output_lineEdit.setText(filename)

    def set_root(self, filepath):
        self.__default_input_path = filepath
        self.__default_subtitle_path = os.path.dirname(filepath)
        self.__default_output_path = self.get_output_filepath(filepath,self.__default_prefix)
        self.output_lineEdit.setText(self.__default_output_path)

    def get_output_filepath(self, filepath, prefix):
        dirname = os.path.dirname(filepath)
        basename = os.path.basename(filepath)
        return os.path.join(dirname, prefix + basename)

    def clear(self):
        self.input_lineEdit.setText('')
        self.subtitle_lineEdit.setText('')
        self.output_lineEdit.setText('')

    def perCheck(self,input_path,subtitle_path,output_path):
        if(input_path == ''):
            return False,'视频为空'
        elif(subtitle_path == ''):
            return False,'字幕为空'
        elif(output_path == ''):
            return False,'输出路径为空'
        else:
            return True,'Running...'

def main():
    app = QApplication(sys.argv)
    mainWidget = MainWidget()
    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()