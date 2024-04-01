from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter

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
    main()