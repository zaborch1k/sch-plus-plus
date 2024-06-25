from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import *

################################################## CURRENT VERSION ######################################################

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.firstTimeLog = True
        self.setUI()

    def setUI(self):
        self.main_widget = QWidget()

        self.width = QApplication.desktop().width()
        self.height = QApplication.desktop().height()
        self.main_widget.setMaximumSize(self.width, self.height)

        self.setWindowTitle("sch1++")
        self.setWindowIcon(QIcon('sch1.ico'))
        self.setStyleSheet('background : rgb(41, 41, 41)')

        self.main_layout = QHBoxLayout()
        
        self.widget1 = QWidget()
        self.widget2 = QWidget()
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()

        self.widget1.setStyleSheet('background : rgb(41, 41, 41);')
        self.widget2.setStyleSheet('background : rgb(41, 41, 41)')

        self.widget1.setMaximumWidth(self.width//3*1)

        # widget1

        # buttons
        self.butt_widget = QWidget()
        self.butt_widget.setStyleSheet('background : rgb(41, 41, 41); color : rgb(180, 180, 180)')
        self.butt_widget.setFixedHeight(35)

        self.butt_layout = QHBoxLayout()

        class NewButton(QPushButton):
            entered = pyqtSignal()
            leaved = pyqtSignal()

            def enterEvent(self, event):
                super().enterEvent(event)
                self.setStyleSheet('background : rgb(80, 80, 80); color : rgb(51, 170, 36); font : 15px Calibri;\
                                   border : 0px; border-radius : 3')

            def leaveEvent(self, event):
                super().leaveEvent(event)
                self.setStyleSheet('background : rgb(41, 41, 41); color : rgb(180, 180, 180); font : 15px Calibri;\
                                    border : 0px; border-radius : 3')

        self.buttons = [NewButton('stop'), NewButton('start'), NewButton('save'), NewButton('open')]

        self.buttons[0].clicked.connect(self.stop)
        self.buttons[1].clicked.connect(self.start)
        self.buttons[2].clicked.connect(self.save)
        self.buttons[3].clicked.connect(self.b_open)

        for b in self.buttons:
            self.butt_layout.addWidget(b, alignment = Qt.AlignTop | Qt.AlignLeft)
            b.setFixedWidth(50)
            b.setFixedHeight(19)
            b.setStyleSheet('font : 15px Calibri; border : 0px; border-radius : 3;')
        
        self.butt_widget.setLayout(self.butt_layout)

        # horizontal border
        self.hscene = QGraphicsScene()
        
        self.hborder = QGraphicsPixmapItem()
        self.hborder.setPixmap(QPixmap('border.png').scaled(self.width//3, 1))
        self.hscene.addItem(self.hborder)

        self.hview = QGraphicsView(self.hscene)
        self.hview.setStyleSheet('border : 0px;')
        self.hview.setFixedHeight(1)
        self.hview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 

        # text box
        self.text_box = QPlainTextEdit()
        self.text_box.setStyleSheet('selection-background-color : rgba(51, 170, 36, 50); border : 0px;\
                                     color : rgb(51, 170, 36);')
        self.text_box.setFont(QFont('Cascadia Code', 10))

        self.layout1.addWidget(self.butt_widget, alignment = Qt.AlignTop | Qt.AlignLeft)
        self.layout1.addWidget(self.hview)
        self.layout1.addWidget(self.text_box)

        # vertical border
        self.bscene = QGraphicsScene()
        
        self.border = QGraphicsPixmapItem()
        self.border.setPixmap(QPixmap('border.png').scaled(2, self.height))
        self.bscene.addItem(self.border)

        self.bview = QGraphicsView(self.bscene)
        self.bview.setStyleSheet('border : 0px;')
        self.bview.setFixedWidth(1)
        self.bview.setMaximumHeight(self.height)
        self.bview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        # widget2

        # field
        self.scene = QGraphicsScene()

        self.field = QGraphicsPixmapItem()
        self.field.setPixmap(QPixmap('field.png').scaled(470, 470))
        self.scene.addItem(self.field)

        self.performer = QLabel()
        self.performer.setFixedWidth(13)
        self.performer.setFixedHeight(13)
        self.performer.setStyleSheet('background : rgb(51, 170, 36); font : 15px Calibri; border : 0px; border-radius : 6;')
        self.scene.addWidget(self.performer)
        self.performer.move(30, 430)

        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet('border : 0px;')

        self.layout2.addWidget(self.view)

        # horizontal border2
        self.hscene2 = QGraphicsScene()
        
        self.hborder2 = QGraphicsPixmapItem()
        self.hborder2.setPixmap(QPixmap('border.png').scaled(self.width//3*2, 1))
        self.hscene2.addItem(self.hborder2)

        self.hview2 = QGraphicsView(self.hscene2)
        self.hview2.setStyleSheet('border : 0px;')
        self.hview2.setFixedHeight(1)
        self.hview2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 

        self.layout2.addWidget(self.hview2)


        # klad tut -> (log info)
        
        self.log_label = QPlainTextEdit()
        self.log_label.setMaximumHeight(150)
        self.log_label.setReadOnly(True)
        self.log_label.setStyleSheet('selection-background-color : rgba(51, 170, 36, 50);\
                                     border-radius : 3; border : 0px; color : rgb(180, 180, 180);\
                                     font : 12px Cascadia Code')
        
        self.layout2.addWidget(self.log_label)


        # all the rest
        self.widget1.setLayout(self.layout1)
        self.widget2.setLayout(self.layout2)

        self.main_layout.addWidget(self.widget1)
        self.main_layout.addWidget(self.bview)
        self.main_layout.addWidget(self.widget2)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
    
    def stop(self):
        self.performer.move(30, 430)

    def start(self):
        from interp import get_data

        self.stop()

        self.mdata = None
        self.err = None

        self.code = self.text_box.toPlainText().strip()

        if len(self.code) != 0:
            data = get_data(self.code)
        
            self.mdata = data[0]
            self.err = data[1]
            self.qpos = data[2]

            if self.log_label.toPlainText() == '\n':
                self.log_label.setPlainText = ''

            self.do_log()

            for i in self.mdata:
                self.execute(i[0], i[1])

            if self.err:
                self.err_msg(self.err)
        
    def do_log(self):
        self.l = len(self.qpos)
        self.n = -1

        def add_log_text():
            pos = self.qpos
            self.n += 1
            if self.l == self.n:
                self.timer.stop()
            if self.n == 0:
                self.log_label.setPlainText(self.log_label.toPlainText() + '[1, 1]')
            else:
                print(self.qpos)
                self.log_label.setPlainText(self.log_label.toPlainText() + '\n' + str(pos[self.n-1]))
        
        self.timer = QTimer(self)
        self.timer.start(500)

        if self.firstTimeLog:
            self.log_label.setPlainText('[execution started]\n')
            self.firstTimeLog = False
        else:
            self.log_label.setPlainText(self.log_label.toPlainText() + '\n\n[execution started]\n')
        
        if self.qpos:
            self.timer.timeout.connect(add_log_text)
        elif self.err:
            self.log_label.setPlainText(self.log_label.toPlainText() + '\n' + f'err : {self.err}')
        else:
            self.timer.stop()

       
    def save(self):
        filename, _ = QFileDialog.getSaveFileName(None, 'Save File', '.', 'Text Files (*.txt);;All Files (*)')
        
        if filename:
            with open(filename, 'w') as file:
                file.write(self.text_box.toPlainText())

    def b_open(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open File', '.', 'Text Files (*.txt);;All Files (*)')

        if filename:
            with open(filename, encoding="utf-8") as file:
                self.text_box.clear()
                self.text_box.insertPlainText(file.read())

    def err_msg(self, err):
        self.error = QMessageBox()
        self.error.setStyleSheet('''font : Cascadia Code 10px; ''')
        self.error.setIconPixmap(QPixmap('warning.jpg').scaled(50,50))
        self.error.setText('\n'+err)
        self.error.setWindowIcon(QIcon('sch1.ico'))
        self.error.setWindowTitle('ooops error :(((')
        self.error.exec_()

    # animation of the performer (REWRITE) 
    def execute(self, dir, num):
        step = 20
        
        self.anim = QPropertyAnimation(self.performer, b'pos')
        old_x = self.performer.pos().x()
        old_y = self.performer.pos().y()
        x = 0
        y = 0

        if dir == 'RIGHT':
            x = step*num

        elif dir == 'LEFT':
            x = -step*num

        elif dir == 'DOWN':
            y = step*num

        elif dir == 'UP':
            y = -step*num
        
        self.anim.setEndValue(QPoint(old_x+x, old_y+y))
        self.anim.start()
        self.anim.setDuration(num*50)
        self.performer.move(QPoint(old_x+x, old_y+y))

################################################## OLD VERSION ###########################################################

def main():
    app = QApplication([])
    window = QWidget()
    window.setFixedSize(1000, 500)
    window.setWindowTitle("sch++")
    window.setWindowIcon(QIcon('sch1.ico'))
    window.setStyleSheet('background : rgb(41, 41, 41)')

    layout = QHBoxLayout()

    button = QPushButton('stop')
    button.setFont(QFont('Cascadia Code', 10))
    button.setStyleSheet('background : rgb(39, 39, 39); color : rgb(180, 180, 180);')
    button.setFixedHeight(35)

    button1 = QPushButton("run")
    button1.setFont(QFont('Cascadia Code', 10))
    button1.setStyleSheet('background : rgb(39, 39, 39); color : rgb(180, 180, 180); ')
    button1.setFixedHeight(35)

    button2 = QPushButton("save")
    button2.setFont(QFont('Cascadia Code', 10))
    button2.setStyleSheet('background : rgb(39, 39, 39); color : rgb(180, 180, 180);')
    button2.setFixedHeight(35)

    button3 = QPushButton("open")
    button3.setFont(QFont('Cascadia Code', 10))
    button3.setStyleSheet('background : rgb(39, 39, 39); color : rgb(180, 180, 180);')
    button3.setFixedHeight(35)

    global text_box
    text_box = QPlainTextEdit()
    text_box.setStyleSheet('border : 0px; color : rgb(51, 170, 36);')
    text_box.setFont(QFont('Cascadia Code', 10))

    scene = QGraphicsScene()

    field = QGraphicsPixmapItem()
    field.setPixmap(QPixmap('field.png').scaled(470, 470))
    scene.addItem(field)

    global performer
    performer = QGraphicsPixmapItem()
    performer.setPixmap(QPixmap('performer.jpg').scaled(15, 15))
    performer.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
    performer.setOffset(29.6, 428)
    scene.addItem(performer)

    view = QGraphicsView(scene)
    view.setStyleSheet('border : 0px;')
    
    layout.addWidget(button)
    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)

    layout2 = QVBoxLayout()
    layout2.addLayout(layout)
    layout2.addWidget(text_box)

    layout1 = QVBoxLayout()
    layout1.addWidget(view)
    
    button.clicked.connect(stop)
    button1.clicked.connect(start)
    button2.clicked.connect(save)
    button3.clicked.connect(b_open)

    main_layout = QHBoxLayout()
    main_layout.addLayout(layout2)
    main_layout.addLayout(layout1)
    window.setLayout(main_layout)
    window.show()
    app.exec_()

def start():
    global performer, text_box
    from interp import get_data

    performer.setPos(0, 0)

    mdata = None
    err = None

    code = text_box.toPlainText().strip()

    if len(code) != 0:
        data = get_data(code)
        
        mdata = data[0]
        err = data[1]
        pos = data[2]#
        
        for i in mdata:
            execute(i[0], i[1])
        if err:
            err_msg(err)

def execute(dir, num):
    global performer
    step = 20

    if dir == 'RIGHT':
        performer.moveBy(step*num, 0)

    elif dir == 'LEFT':
        performer.moveBy(-step*num, 0)

    elif dir == 'DOWN':
        performer.moveBy(0, step*num)

    elif dir == 'UP':
        performer.moveBy(0, -step*num)

def stop():
    performer.setPos(0, 0)

def save():
    global text_box
    filename, _ = QFileDialog.getSaveFileName(None, 'Save File', '.', 'Text Files (*.txt);;All Files (*)')
    
    if filename:
        with open(filename, 'w') as file:
            file.write(text_box.toPlainText())

def b_open():
    global text_box
    filename, _ = QFileDialog.getOpenFileName(None, 'Open File', '.', 'Text Files (*.txt);;All Files (*)')

    if filename:
        with open(filename, encoding="utf-8") as file:
            text_box.clear()
            text_box.insertPlainText(file.read())

def err_msg(err):
    error = QMessageBox()
    error.setStyleSheet('''font : Cascadia Code 10px; ''')
    error.setIconPixmap(QPixmap('warning.jpg').scaled(50,50))
    error.setText('\n'+err)
    error.setWindowIcon(QIcon('sch1.ico'))
    error.setWindowTitle('ooops error :(((')
    error.exec_()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
    # main()
