#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from timeit import default_timer as timer

# import psutil
from PyQt5.QtGui import QPixmap, QPainterPath, QBrush, QPainter, QFont, QPen
from PyQt5.QtCore import Qt, pyqtProperty, QPoint, QPointF, QPropertyAnimation
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtProperty
from gui import Ui_Form
from PyQt5 import QtCore, QtWidgets

timelimit = 60

productDict = {} # productDict: store the dictionary of product ID and its location
productLocation = [] # store all the locations of the products
prevOrderProductLoc = [] #store the previous order product locations, to change back the color
orderProductLoc = [] #store all the product locations in the order
warehouseMap = []  # use 0, 1 to represent the empty space and shelves
product = []
users = []  # store all the users
path = []   # store all the directions of different paths
maxWidth = 0   # store the map’s height and width
maxHeight = 0
graphStartPixel = (100, 780) # store where to draw the static map graph background
mapPath=''
orderListPath = ''

pathStartPixel = (105, 785)  # store which pixel to start drawing the path and end the drawing
pathEndPixel = (105, 785)
pathStartPoint = (0, 0)  # store where the path starts and ends
pathEndPoint = (0, 0)

animatedPathPixel = [] # store pixels the animation needs to generate the path

'''
Attributes of User Class
name: a string corresponding to the user’s real name  
username: a string with the maximum length of 10, created by the user
id: a string with the maximum length of 5, assigned by the manager
password: a string with the maximum length of 10
position([x, y]): an int array corresponding to the user’s real position, the first element is x coordinate and the second element is y coordinate
'''
class User:
    def __init__(self, username, password, position):
        self.username = username
        self.password = password
        self.position = position
    def getUsername(self):
        return self.username
    def getID(self):
        return self.id
    def getPosition(self):
        return self.position
    def getProductPosition(Product):
        return Product.getPosition()

'''
Attributes of Product Class 
id: an int type data with the maximum length of 7, assigned by the warehouse system, each product has a unique id 
x: location in x coordinate
y: location in y coordinate
'''             
class Product:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    def getID(self):
        return self.id
    def getPosition(self):
        return (self.x, self.y)

'''
Attributes of Map Class
width: the length in x coordinate
height: the length in y coordinate
''' 
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0]*width for i in range(height)]
        
    def addShelves(self, product):
        for p in product:
            (x, y) = p.getPosition()
            self.map[maxHeight - y][x] = 1
'''
Attributes of Loading Class

''' 
class Loading(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(Loading, self).__init__()
        self.resize(300, 100)
        self.setWindowTitle('Map Loading System')

        self.select_button = QPushButton('Select Map', self)
        self.default_button = QPushButton('Use Default Map', self)

        self.grid_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.pushbutton_init()  # button
        self.layout_init()

    def layout_init(self): #  initialize the interface
        self.h_layout.addWidget(self.select_button)    
        self.h_layout.addWidget(self.default_button)
        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    def pushbutton_init(self):
        self.select_button.clicked.connect(self.selectmap)
        self.default_button.clicked.connect(self.defaultmap)

    def selectmap(self):
        global mapPath
        mapPath, imgType = QFileDialog.getOpenFileName(self, "Select Map", "", "*.txt;;*.txt;;All Files(*)")
        if(mapPath):
            self.switch_window.emit()

    def defaultmap(self):
        global mapPath
        mapPath = 'qvBox-warehouse-data-f21-v01.txt'
        self.switch_window.emit()

'''
Attributes of Loading2 Class

''' 
class Loading2(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(Loading2, self).__init__()
        self.resize(300, 100)
        self.setWindowTitle('Order List Loading System')
        self.select_button = QPushButton('Select Order List', self)
        self.default_button = QPushButton('Use Default List', self)

        self.grid_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.pushbutton_init()  # button
        self.layout_init()

    def layout_init(self): #  initialize the interface
        self.h_layout.addWidget(self.select_button)     
        self.h_layout.addWidget(self.default_button)
        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    def pushbutton_init(self):
        self.select_button.clicked.connect(self.selectOrderList)
        self.default_button.clicked.connect(self.defaultOrderList)

    def selectOrderList(self):
        global orderListPath
        orderListPath, imgType = QFileDialog.getOpenFileName(self, "Select Order List", "", "*.txt;;*.txt;;All Files(*)")
        if(orderListPath):
            self.switch_window.emit()

    def defaultOrderList(self):
        global orderListPath
        orderListPath = 'qvBox-warehouse-orders-list-part01.txt'
        self.switch_window.emit()

'''
Attributes of Controller Class

''' 
class Controller:

    def __init__(self):
        pass

    def show_loading(self): # show the map loading system
        self.loading = Loading()
        self.loading.switch_window.connect(self.show_loading2)
        self.loading.show()

    def show_loading2(self): # show orderlist loading system
        self.loading2 = Loading2()
        self.loading2.switch_window.connect(self.show_main)
        self.loading2.show()
        self.loading.close()
        
    def show_main(self): #  close the loading system and show the navigation system
        initWarehouse()
        warehouse = Map(maxWidth + 1, maxHeight + 1)
        warehouse.addShelves(product)
        self.window = Gui()
        self.loading2.close()
        self.window.show()
'''
Attributes of QSSLoader Class

'''         
class QSSLoader:
    def __init__(self):
        pass
    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r',  encoding='UTF-8') as file:
            return file.read()
'''
Attributes of workericon Class

''' 
class workerIcon(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        pix = QPixmap("worker.png")
        self.h = pix.height()
        self.w = pix.width()
        self.setPixmap(pix)
    def _set_pos(self, pos):
        self.move(int(pos.x() - self.w/2), int(pos.y() - self.h/2))
    pos = pyqtProperty(QPoint, fset=_set_pos)      

'''
Attributes of Gui Class

''' 
class Gui(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.worker = workerIcon(self)
        self.worker.pos = QPointF(pathStartPixel[0], pathStartPixel[1])
        self.animatedPath = None
        #style
        style_file = './mystylesheet.qss'
        style_sheet = QSSLoader.read_qss_file(style_file)
        self.setStyleSheet(style_sheet)
        #buffer for map
        self.pix = QPixmap(1400, 1000)
        self.pix.fill(Qt.transparent)
        self.GenerateGraph(self.pix)
        #click event
        self.pushButton.clicked.connect(self.btnProcess)
        self.pushButton.clicked.connect(self.initAnimation)
        self.pushButton1.clicked.connect(self.btnProcess1)
        self.pushButton1.clicked.connect(self.initAnimation)
        self.pushButton2.clicked.connect(self.btnProcess2)
        self.pushButton3.clicked.connect(self.orderbtnProcess)
        self.pushButton3.clicked.connect(self.initAnimation)
        self.pushButton4.clicked.connect(self.orderbtnProcess1)
        self.pushButton4.clicked.connect(self.initAnimation)
        self.pushButton5.clicked.connect(self.orderbtnProcess2)
        
        self.setFixedSize(1600, 900)
        self.number = 0
        self.visitednumber = [0]
        self.unvisitednumber = 0

    def orderbtnProcess(self):
        orders = [[1]]
        with open(orderListPath, 'r') as f:
            lines = f.read().splitlines()
        for line in lines:
            order = line.strip().split(", ")
            orders.append(order)

        global path, pathStartPoint, pathEndPoint, orderProductLoc
        path = []
        productLocList = []
        number1 = self.textEdit4.toPlainText()
        number1 =  number1.strip()
        if number1:
            self.number = int(number1)
            if self.number >= len(orders):
                self.textBrowser.setText("Order number out of range!")
                return
        else:
            while self.unvisitednumber in self.visitednumber:
                self.unvisitednumber += 1
            self.number = self.unvisitednumber
            if self.number >= len(orders):
                self.textBrowser.setText("All orders are finished!")
                return
        self.visitednumber.append(self.number)
        input = orders[self.number]
        sLoc = self.textEdit2.toPlainText()
        sLoc = sLoc.strip().split()
        eLoc = self.textEdit3.toPlainText()
        eLoc = eLoc.strip().split()

        for i in input:
            if i in productDict.keys():
                productLocList.append(productDict.get(i))
            else:
                path = []
                self.textBrowser.setText("product not found")
                return
        orderProductLoc = productLocList
        if sLoc:
            pathStartPoint = (int(sLoc[0]), int(sLoc[-1]))
        if eLoc:
            pathEndPoint = (int(eLoc[0]), int(eLoc[-1]))
        idOrder = []
        locOrder = []
        stime = timer()
        locOrder, indexOrder = NNgeneratePickupLocOrder(pathStartPoint, productLocList)
        # memory2 = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        # print(u'Current Memory：%.4f MB' % (memory2 - memory1))
        etime = timer()
        interval = etime - stime
        # find new ID order, based on index order

        # inside productLocList: (startLoc,firstproductLoc, secondproductLoc....., endLoc)
        # remember, these are productLoc, not the pickupLoc
        productLocList = locOrder
        productLocList.insert(0, pathStartPoint)
        productLocList.append(pathEndPoint)
        # print to console
        print(productLocList)
        next = (0, 0)
        # now based on productLocList, we generate all the pickupLoc, so that we can draw path
        for i, productLoc in enumerate(productLocList):
            if i == 0:
                count = 2
                # while(productLocList[i+1]==productLocList[i+count]):
                #     count += 1
                _,y1 = productLocList[i+1]
                _,yc = productLocList[i+count]
                while True:
                    _,yc = productLocList[i+count]
                    if yc == y1:
                        if(i+count<len(productLocList)-1):
                            count += 1
                        else:
                            break
                    else:
                        break
                next = choosePoint(pathStartPoint, productLocList[i + 1], productLocList[i + count])
                generatePath(bfs(warehouseMap, productLocList[i], next))
            elif i == len(productLocList) - 2:
                generatePath(bfs(warehouseMap, next, productLocList[i + 1]))
                break
            else:
                if productLocList[i] == productLocList[i + 1]:
                    generatePath(bfs(warehouseMap, next, next))
                else:
                    count = 2
                    # while(productLocList[i+1]==productLocList[i+count]):
                    #     count += 1
                    x1,y1 = productLocList[i+1]
                    xc,yc = productLocList[i+count]
                    while True:
                        _,yc = productLocList[i+count]
                        if yc == y1:
                            if(i+count<len(productLocList)-1):
                                count += 1
                            else:
                                break
                        else:
                            break
                    tmp = choosePoint(next, productLocList[i + 1], productLocList[i + count])
                    generatePath(bfs(warehouseMap, next, tmp))
                    next = tmp
        pathlength = 0
        for p in path:
            pathlength += len(p)

        for i in indexOrder:
            idOrder.append(input[i])
        self.textBrowser.setText("Order Number:" + str(self.number) +
                                 "\nPickup ID order:" + str(idOrder) +
                                 "\n\nTime interval(seconds):%.3f" % interval +
                                 "\n\nPath length:%d" % pathlength +
                                 "\n\nPath:\n" + toPathStr(path, idOrder)
                                 )
        if len(path):
            self.updateAnimation()
            self.animatedPath = generateAnimatedPath()
        self.update()

    def orderbtnProcess1(self):
        # global memory
        # memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        global path, pathStartPoint, pathEndPoint, timelimit, orderProductLoc
        orders = [[1]]
        with open(orderListPath, 'r') as f:
            lines = f.read().splitlines()
        for line in lines:
            order = line.strip().split(", ")
            orders.append(order)
        path = []
        productLocList = []
        number1 = self.textEdit4.toPlainText()
        number1 = number1.strip()
        if number1:
            self.number = int(number1)
            if self.number >= len(orders):
                self.textBrowser.setText("Order number out of range!")
                return
        else:
            while self.unvisitednumber in self.visitednumber:
                self.unvisitednumber += 1
            self.number = self.unvisitednumber
            if self.number >= len(orders):
                self.textBrowser.setText("All orders are finished!")
                return
        self.visitednumber.append(self.number)

        input = orders[self.number]
        sLoc = self.textEdit2.toPlainText()
        sLoc = sLoc.strip().split()
        eLoc = self.textEdit3.toPlainText()
        eLoc = eLoc.strip().split()
        tl = self.textEdit_time.toPlainText()
        if tl:
            timelimit = int(tl)

        global bfroutelist, bfroutes, bfdict
        bfroutelist = []
        bfroutes = []
        bfdict = {(0, 0): {(0, 0): 0}
                  }

        for i in input:
            if i in productDict.keys():
                productLocList.append(productDict.get(i))
            else:
                path = []
                self.textBrowser.setText("product not found")
                return

        orderProductLoc = productLocList

        if sLoc:
            pathStartPoint = (int(sLoc[0]), int(sLoc[-1]))
            if eLoc:
                pathEndPoint = (int(eLoc[0]), int(eLoc[-1]))
        idOrder = []
        stime = timer()
        shortestdisctance, shortestpath = bfallpath(pathStartPoint, pathEndPoint, productLocList)
        etime = timer()
        interval = etime - stime

        cnt = 0
        for j in range(0, len(shortestpath)):
            q = 0
            p1 = shortestpath[j]
            indexs = bffindNeighbours(warehouseMap, p1)
            if len(indexs) != 0:
                i = 0
                length = len(input)
                while i < length:
                    if productDict[input[i]] in indexs:
                        idOrder.append(input[i])
                        input.remove(input[i])
                        length -= 1
                        q += 1
                        if (length == 0):
                            cnt = j
                        if (j == 0 or j == len(shortestpath) or q > 1):
                            bf = bfs(warehouseMap, shortestpath[j], shortestpath[j])
                            generatePath(bf)
                        else:
                            bf = bfs(warehouseMap, shortestpath[j - 1], shortestpath[j])
                            generatePath(bf)
                    else:
                        i += 1

        for i in range(cnt, len(shortestpath) - 1):
            bf = bfs(warehouseMap, shortestpath[i], shortestpath[i + 1])
            generatePath(bf)
        print(shortestpath)
        pathlength = 0

        for p in path:
            pathlength += len(p)

        self.textBrowser.setText("Order Number:" + str(self.number) +
                                 "\nPickup ID order:" + str(idOrder) +
                                 "\n\nTime interval(seconds):%.3f" % interval +
                                 "\n\nPath length:%d" % pathlength +
                                 "\n\nPath:\n" + toPathStr(path, idOrder)
                                 )
        if len(path):
            self.updateAnimation()
            self.animatedPath = generateAnimatedPath()
        self.update()

    def orderbtnProcess2(self):
        global orderProductLoc, path
        productLocList = []
        orders = [[1]]
        with open(orderListPath, 'r') as f:
            lines = f.read().splitlines()
        for line in lines:
            order = line.strip().split(", ")
            orders.append(order)
        path = []
        productLocList = []
        number1 = self.textEdit4.toPlainText()
        number1 = number1.strip()
        if number1:
            self.number = int(number1)
            if self.number >= len(orders):
                self.textBrowser.setText("Order number out of range!")
                return
        else:
            while self.unvisitednumber in self.visitednumber:
                self.unvisitednumber += 1
            self.number = self.unvisitednumber
            if self.number >= len(orders):
                self.textBrowser.setText("All orders are visited!")
                return
        self.visitednumber.append(self.number)

        input = orders[self.number]
        s = ""

        for i in input:
            if i in productDict.keys():
                s += "Product: " + i
                id = productDict.get(i)
                x , y = id
                productLocList.append(id)
                s = s + " " +"\n( X "+ str(x)  +",  Y "  + str(y) +") \n"

            else:
                self.textBrowser.setText("product not found")
                return
        orderProductLoc = productLocList
        path = []
        self.textBrowser.setText("Order Number:" + str(self.number) + "\n" + s)
        self.update()

    def btnProcess(self):
        # memory1 = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        global path, pathStartPoint, pathEndPoint, orderProductLoc
        path = []
        productLocList = []
        orderProductLoc = []
        input = self.textEdit.toPlainText()
        input = input.strip().split()
        sLoc = self.textEdit2.toPlainText()
        sLoc = sLoc.strip().split()
        eLoc = self.textEdit3.toPlainText()
        eLoc = eLoc.strip().split()

        for i in input:
            if i in productDict.keys():
                productLocList.append(productDict.get(i))
            else:
                path = []
                self.textBrowser.setText("product not found")
                return
        orderProductLoc = productLocList

        if sLoc:
            pathStartPoint = (int(sLoc[0]), int(sLoc[-1]))
        if eLoc:
            pathEndPoint = (int(eLoc[0]), int(eLoc[-1]))
        idOrder = []
        locOrder = []
        stime = timer()
        locOrder, indexOrder = NNgeneratePickupLocOrder(pathStartPoint, productLocList)
        # memory2 = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        # print(u'Current Memory：%.4f MB' % (memory2 - memory1))
        etime = timer()
        interval = etime - stime
        # find new ID order, based on index order

        # inside productLocList: (startLoc,firstproductLoc, secondproductLoc....., endLoc)
        # remember, these are productLoc, not the pickupLoc
        productLocList = locOrder
        productLocList.insert(0, pathStartPoint)
        productLocList.append(pathEndPoint)
        # print to console
        print(productLocList)
        next = (0, 0)
        # now based on productLocList, we generate all the pickupLoc, so that we can draw path
        for i, productLoc in enumerate(productLocList):
            if i == 0:
                count = 2
                # while(productLocList[i+1]==productLocList[i+count]):
                #     count += 1
                _,y1 = productLocList[i+1]
                _,yc = productLocList[i+count]
                while True:
                    _,yc = productLocList[i+count]
                    if yc == y1:
                        if(i+count<len(productLocList)-1):
                            count += 1
                        else:
                            break
                    else:
                        break
                next = choosePoint(pathStartPoint, productLocList[i + 1], productLocList[i + count])
                print(next)
                generatePath(bfs(warehouseMap, pathStartPoint, next))
            elif i == len(productLocList) - 2:
                generatePath(bfs(warehouseMap, next, productLocList[i + 1]))
                break
            else:
                if productLocList[i] == productLocList[i + 1]:
                    generatePath(bfs(warehouseMap, next, next))
                else:
                    count = 2
                    # while(productLocList[i+1]==productLocList[i+count]):
                    #     count += 1
                    _,y1 = productLocList[i+1]
                    _,yc = productLocList[i+count]
                    while True:
                        _,yc = productLocList[i+count]
                        if yc == y1:
                            if(i+count<len(productLocList)-1):
                                count += 1
                            else:
                                break
                        else:
                            break
                    tmp = choosePoint(next, productLocList[i + 1], productLocList[i + count])
                    generatePath(bfs(warehouseMap, next, tmp))
                    next = tmp
        pathlength = 0
        for p in path:
            pathlength += len(p)

        for i in indexOrder:
            idOrder.append(input[i])
        self.textBrowser.setText("Pickup ID order:" + str(idOrder) +
                                 "\n\nTime interval(seconds):%.3f" % interval +
                                 "\n\nPath length:%d" % pathlength +
                                 "\n\nPath:\n" + toPathStr(path, idOrder)
                                 )
        if len(path):
            self.updateAnimation()
            self.animatedPath = generateAnimatedPath()
        self.update()
        
    def btnProcess1(self):
        # global memory
        # memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        global path, pathStartPoint, pathEndPoint,timelimit,orderProductLoc 
        path = []
        productLocList = []
        orderProductLoc = []
        input = self.textEdit.toPlainText()
        input = input.strip().split()
        sLoc = self.textEdit2.toPlainText()
        sLoc = sLoc.strip().split()
        eLoc = self.textEdit3.toPlainText()
        eLoc = eLoc.strip().split()
        tl = self.textEdit_time.toPlainText()
        if tl:
            timelimit = int(tl)


        global bfroutelist, bfroutes, bfdict
        bfroutelist = []
        bfroutes = []
        bfdict = {(0, 0): {(0, 0): 0}
                  }

        for i in input:
            if i in productDict.keys():
                productLocList.append(productDict.get(i))
            else:
                path = []
                self.textBrowser.setText("product not found")
                return
        orderProductLoc = productLocList

        if sLoc:
            pathStartPoint = (int(sLoc[0]), int(sLoc[-1]))
            if eLoc:
                pathEndPoint = (int(eLoc[0]), int(eLoc[-1]))
        idOrder = []
        stime = timer()
        shortestdisctance, shortestpath = bfallpath(pathStartPoint, pathEndPoint, productLocList)
        etime = timer()
        interval = etime - stime

        cnt = 0
        for j in range(0, len(shortestpath)):
            q = 0
            p1 = shortestpath[j]
            indexs = bffindNeighbours(warehouseMap, p1)
            if len(indexs) != 0:
                i = 0
                length = len(input)
                while i < length:
                    if productDict[input[i]] in indexs:
                        idOrder.append(input[i])
                        input.remove(input[i])
                        length -= 1
                        q += 1
                        if (length == 0):
                            cnt = j
                        if (j == 0 or j == len(shortestpath) or q >1 ):
                            bf = bfs(warehouseMap, shortestpath[j], shortestpath[j])
                            generatePath(bf)
                        else:
                            bf = bfs(warehouseMap, shortestpath[j - 1], shortestpath[j])
                            generatePath(bf)
                    else:
                        i += 1


        for i in range(cnt, len(shortestpath) - 1):
            bf = bfs(warehouseMap, shortestpath[i], shortestpath[i + 1])
            generatePath(bf)
        print(shortestpath)
        pathlength = 0

        for p in path:
            pathlength += len(p)
    

    
        self.textBrowser.setText("Pickup ID order:" + str(idOrder) +
                                 "\n\nTime interval(seconds):%.3f" % interval +
                                 "\n\nPath length:%d" % pathlength +
                                 "\n\nPath:\n" + toPathStr(path, idOrder)
                                 )
        if len(path):
            self.updateAnimation()
            self.animatedPath = generateAnimatedPath()
        self.update()
    

    def btnProcess2(self):
        global path, orderProductLoc
        orderProductLoc = []
        productLocList = []
        input = self.textEdit.toPlainText()
        input = input.strip().split()
        s = ""

        for i in input:
            if i in productDict.keys():
                s += "Product: " + i
                id = productDict.get(i)
                x , y = id
                productLocList.append(id)
                s = s + " " +"\n( X "+ str(x)  +",  Y "  + str(y) +") \n"

            else:
                self.textBrowser.setText("product not found")
                return
        print(s)
        orderProductLoc = productLocList
        path = []
        self.update()
        self.textBrowser.setText(s)
        
        
    def GenerateGraph(self, pix): #  draw the layout
        global flag
        p = QPainter(pix)
        p.setFont(QFont('Times New Roman', 30))
        p.drawText(500, 100, 'Warehouse Map')
        p.setPen(QPen(Qt.black,  1, Qt.SolidLine))
        p.drawRect(80, 780 - 30 * (maxHeight + 1), 40 + (maxWidth+1) * 30, 40 + maxHeight * 31)

        p.setPen(QPen(Qt.white,  1, Qt.SolidLine))
        p.setBrush(QBrush(Qt.lightGray, Qt.SolidPattern))
        center = QPoint(80, 10)
        p.drawEllipse(center,5 , 5)
        p.setPen(QPen(Qt.black,  1, Qt.SolidLine))
        p.setFont(QFont('Times New Roman', 12))
        p.drawText(120, 15, "Empty space")

        p.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        p.drawRect(75, 35, 8, 8)  
        p.setFont(QFont('Times New Roman', 12))
        p.drawText(120, 45, "Shelf  Location")

        p.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        center = QPoint(80, 70)
        p.drawEllipse(center,5 , 5)
        p.setFont(QFont('Times New Roman', 12))
        p.drawText(120, 75, "Start Location ---- Default(0, 0)")

        p.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        center = QPoint(80, 100)
        p.drawEllipse(center,5 , 5)
        p.drawText(120, 105, "Pick up product")

        p.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        center = QPoint(80, 130)
        p.drawEllipse(center,5 , 5)
        p.drawText(120, 135, "End Location ---- Default(0, 0)")

        p.drawText(75, 840, "X")
        p.drawText(50, 815, "Y")
        p.drawText(13, 845, "(X, Y)")

        for i in range(maxHeight+1):
            for j in range(maxWidth+1):
                p.setPen(QPen(Qt.black,  1, Qt.SolidLine))
                if i == 0:
                    p.setFont(QFont('Times New Roman', 12))
                    p.drawText(100 + j*30, 840, str(j))
                if j == 0:
                    p.setFont(QFont('Times New Roman', 12))
                    p.drawText(50 , 790 - i * 30, str(i))

                if (j,i) in productLocation :
                    p.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                    p.drawRect(100+j*30, 780 - i*30 , 10, 10)  
                else:
                    p.setPen(QPen(Qt.white,  1, Qt.SolidLine))
                    p.setBrush(QBrush(Qt.lightGray, Qt.SolidPattern))
                    p.drawEllipse(100+j*30, 780 - i*30 , 10, 10)

    def updateAnimation(self): # generate the animated path
        global path, flag, animatedPathPixel, pathStartPixel, pathEndPixel
        animatedPathPixel = []
        pathStartPixel = (105 + pathStartPoint[0] * 30, 785 - pathStartPoint[1] * 30)
        pathEndPixel = (105 + pathEndPoint[0] * 30, 785 - pathEndPoint[1] * 30)

        startPixel = (105 + pathStartPoint[0] * 30, 785 - pathStartPoint[1] * 30)
        for m, s in enumerate(path):
            d = 30
            for n, i in enumerate(s):
                x1, y1 = startPixel
                animatedPathPixel.append(QPoint(x1, y1))
                if i == 'r':
                    startPixel = (x1 + d, y1)
                    animatedPathPixel.append(QPoint(x1 + d, y1))
                elif i == 'l':
                    startPixel = (x1 - d, y1)
                    animatedPathPixel.append(QPoint(x1 - d, y1))
                elif i == 'u':
                    startPixel = (x1, y1 - d)
                    animatedPathPixel.append(QPoint(x1, y1 - d))
                else:
                    startPixel = (x1, y1 + d)
                    animatedPathPixel.append(QPoint(x1, y1 + d))

    def paintEvent(self, event): # draw the corresponding map towards the product
        global path, flag, animatedPathPixel, pathStartPixel, pathEndPixel, orderProductLoc, prevOrderProductLoc
        
        startPixel = (105 + pathStartPoint[0] * 30, 785 - pathStartPoint[1] * 30)
        endPixel = (105 + pathEndPoint[0] * 30, 785 - pathEndPoint[1] * 30)
          
        p = QPainter(self)  
        p.drawPixmap(QPoint(), self.pix) #load graph from Bitmap
        #change the color of previous pickup product locations 
        p.setPen(QPen(Qt.black,  1, Qt.SolidLine))
        p.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        for m in prevOrderProductLoc:
            i, j = m
            p.drawRect(100+i*30, 780 - j*30 , 10, 10) 

        #draw pickup product locations
        p.setPen(QPen(Qt.black,  1, Qt.SolidLine))
        p.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        for m in orderProductLoc:
            i, j = m
            p.drawRect(100+i*30, 780 - j*30 , 10, 10)
        prevOrderProductLoc = orderProductLoc

        # draw start location
        p.setPen(QPen(Qt.black,  1, Qt.SolidLine))
        p.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        center = QPoint(startPixel[0], startPixel[1])
        p.drawEllipse(center,5 , 5)

        for m, s in enumerate(path):
            p.setPen(QPen(Qt.red,  4, Qt.SolidLine))
            d = 30
            for n, i in enumerate(s):
                x1, y1 = startPixel
                animatedPathPixel.append(QPoint(x1, y1))
                if i == 'r':
                    p.drawLine(x1, y1, x1+d, y1)
                    startPixel = (x1 + d, y1)
                    
                elif i == 'l':
                    p.drawLine(x1, y1, x1-d, y1)
                    startPixel = (x1 - d, y1)
                    
                elif i == 'u':
                    p.drawLine(x1, y1 - d, x1, y1)
                    startPixel = (x1, y1 - d)
                    
                else:
                    p.drawLine(x1, y1, x1, y1 + d)
                    startPixel = (x1, y1 + d)
                    

            p.setPen(QPen(Qt.red,  2, Qt.SolidLine))
            p.setBrush(QBrush(Qt.red, Qt.SolidPattern))
            center = QPoint(startPixel[0], startPixel[1])
            p.drawEllipse(center,4 , 4)

        # draw end location
        p.setPen(QPen(Qt.black,  1, Qt.SolidLine))
        p.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        center = QPoint(endPixel[0], endPixel[1])
        p.drawEllipse(center,5 , 5)


    def initAnimation(self):
        self.anim = QPropertyAnimation(self.worker, b'pos')
        l = 0
        for i in path:
            l += len(i)
        self.anim.setDuration(l*150)
        self.anim.setStartValue(QPointF(pathStartPixel[0], pathStartPixel[1]))
        vals = [p/200 for p in range(0, 201)]
        if self.animatedPath:
            for i in vals:
                self.anim.setKeyValueAt(i, self.animatedPath.pointAtPercent(i))  
            self.anim.setEndValue(QPointF(pathEndPixel[0], pathEndPixel[1]))        
            self.anim.start()
###########################################################################################################
#Initialize Warehouse Functions
###########################################################################################################
'''
initializes the map of the warehouse

'''  
def initWarehouse(): 
    global product, maxWidth, maxHeight, productDict, productLocation, warehouseMap, filepath
    lines = []
    #with open('warehouse.txt','r') as f:
    with open(mapPath, 'r') as f:
        title = f.readline()
        lines = f.read().splitlines()
    for line in lines:
        info = line.split("\t")
        x = int(float(info[1]))
        maxWidth = x if x > maxWidth else maxWidth
        y = int(float(info[2]))
        maxHeight = y if y > maxHeight else maxHeight
        product.append(Product(info[0], x, y))
        productLocation.append((x,y))
        productDict[info[0]] = (x, y)

    map = [[0]*(maxWidth+1) for i in range(maxHeight+1)]
    for p in product:
        (x, y) = p.getPosition()
        map[y][x] = 1 
    warehouseMap = map

###########################################################################################################
#Breadth First Search Functions
########################################################################################################### 
'''
find a path between two nodes

'''  
def bfs(map, start, end): 
    explored = []
    queue = [[start]]
    if start == end:
        # print("Same Node")
        return []
    while queue:
        # print(queue)
        path1 = queue.pop(0)
        node = path1[-1]
        
        if node not in explored:
            neighbours = findNeighbours(map, node)
            for neighbour in neighbours:
                new_path = list(path1)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == end:
                    print("Shortest path = ", *new_path)
                    return new_path
            explored.append(node)

    print("Can't find any path between these two points")
    return []

'''
returns the neighbors of one location

'''  
def findNeighbours(map, location): 
    neighbours = []
    h = len(map)
    w = len(map[0])
    x, y = location
    if x + 1 < w and map[y][x+1] != 1:
        neighbours.append((x+1, y))
    if x - 1 >= 0 and map[y][x-1] != 1:
        neighbours.append((x-1, y))

    if y + 1 < h and map[y+1][x] != 1:
        neighbours.append((x, y+1))

    if y - 1 >= 0 and map[y-1][x] != 1:
        neighbours.append((x, y-1))
    return neighbours




###########################################################################################################
#Draw path/ text path/ animated path functions
###########################################################################################################
'''
convert coordinates to directions

'''  

def generatePath(bfsPath): 
    global path
    tmpPath = []
    if bfsPath: 
        start = bfsPath[0] 
        for i in range(len(bfsPath)):
            next = bfsPath[i]
            if next[0] - start[0] == 1:
                tmpPath.append('r')
            if next[0] - start[0] == -1:
                tmpPath.append('l')
            if next[1] - start[1] == 1:
                tmpPath.append('u')
            if next[1] - start[1] == -1:
                tmpPath.append('d')
            start = next
    path.append(tmpPath)

'''
generates the animated path that workerIcon will follow

'''  

def generateAnimatedPath(): 
    start = pathStartPixel
    path = animatedPathPixel
    p = QPainterPath()
    p.moveTo(start[0], start[1])
    for i in path:
        p.lineTo(i)
    return p

'''
combine same direction path

'''      

def combinePath(distance, direction, d, start,  pathStr):
    x, y = start
    #generate new start point
    if direction == 'l':
        x -= distance
    elif direction == 'r':
        x += distance
    elif direction == 'u':
        y += distance
    else:
        y -= distance
    pathStr += ("From" + str(start) + "to" + str((x, y)))
    if d == 'l':
        pathStr += ", then go left\n"
    elif d == 'r':
        pathStr += ", then go right\n"
    elif d == 'u':
        pathStr += ", then go up\n"
    elif d == 'd':
        pathStr += ", then go down\n"
    else:
        pathStr += ", then stop\n"
    distance = 1
    direction = d
    start = (x, y)
    return pathStr, start, direction, distance
'''
#generate the detailed path string 

'''  

def toPathStr(path, idorder):
    start = pathStartPoint
    end = pathEndPoint
    pathStr = ""
    direction = ''
    i = 0
    for m, p in enumerate(path):
        if not p: #empty path, means two products have the same location. 
            pathStr += "Pick up product(" + idorder[i] +")\n"
            i += 1
        else:
            direction = p[0]
            distance = 0
            for n, d in enumerate(p):
                if d == direction:
                    distance += 1
                    if n == len(p) - 1:
                        #end of the path, pick up product
                        pathStr, start, direction, distance = combinePath(distance, direction, 'p', start,  pathStr)
                        #end of the whole path, last location is the end point, no need to pick up products
                        if m != len(path) - 1:
                            pathStr += "Pick up product(" + idorder[i] +")\n"
                            i += 1
                else:
                    pathStr, start, direction, distance = combinePath(distance, direction, d, start,  pathStr)
                    if n == len(p) - 1:
                        pathStr, start, direction, distance = combinePath(distance, direction, 'p', start,  pathStr)
                        if m != len(path) - 1:
                            pathStr += "Pick up product(" + idorder[i] +")\n"
                            i += 1
    return pathStr
###########################################################################################################
#Optimized NN Functions
###########################################################################################################
'''
generate the distance matrix used in NN algorithm

'''  
def generateDistanceMatrix(productLocList):
    l = len(productLocList)
    m = [[0]*l for i in range(l)]
    for i in range(l):
        pickupLoc1 = []
        p1 = productLocList[i]
        x, y = p1
        if y == 0 : #only consider pick up the product from up/down
            list1 = [(x, y+1)]
        elif y == maxHeight - 1:
            list1 = [(x, y-1)]
        else:
            list1 = [(x, y+1), (x, y-1)]
        for tmp in list1: 
            if tmp not in productLocation:
                pickupLoc1.append(tmp)
        for j, productLoc in enumerate(productLocList):
            if i == j:
                m[i][j] = 999
                continue
            elif productLocList[i] == productLoc: #p1Loc == p2Loc, set min distance = 0
                m[i][j] = 0
                continue
            pickupLoc2 = []
            p2 = productLoc
            x, y = p2
            if y == 0 : #only consider pick up the product from up/down
                list2 = [(x, y+1)]
            elif y == maxHeight - 1:
                list2 = [(x, y-1)]
            else:
                list2 = [(x, y+1), (x, y-1)]
            for tmp in list2:
                if tmp not in productLocation:
                    pickupLoc2.append(tmp)
            m[i][j] = findDistance(pickupLoc1, pickupLoc2)
    return m
'''
find distance between two products

'''  
def findDistance(pickupLoc1, pickupLoc2):
    min = 999
    for i in pickupLoc1:
        if i in pickupLoc2:
            dis = 0.5  
            # p1Loc != p2Loc, but can be picked up from the same spot; set dis = 0.5 to make it has lower priority than p1Loc == p2Loc
            return dis
        for j in pickupLoc2:
            l = len(bfs(warehouseMap, i, j))#use bfs to find distance between 2 points, points are from available pickup spots
            if l < min:
                min = l
                dis = min
    return dis - 1
'''
use the NN algorithm to generate the pickup order

'''  
#Nearest Neighbour Algorithm
def NNgeneratePickupLocOrder(start, productLocList):
    dMatrix = generateDistanceMatrix(productLocList)
    pickupLocOrder = []
    min = 999
    xs, ys = start
    index = 0
    visitedIndex = []
    # find the first pickup product based on the starting point
    for i, p in enumerate(productLocList):
        x,y = p
        dis = abs(xs - x) + abs(ys - y)
        if dis < min:
            min = dis
            first = p
            index = i
    pickupLocOrder.append(first)
    visitedIndex.append(index)
    # find the order of rest of the products
    while len(visitedIndex) != len(dMatrix):
        min = 1000
        for i in range(len(dMatrix)):
            if i not in visitedIndex:
                if dMatrix[index][i] < min:
                    next = productLocList[i]
                    tmpindex = i
                    min = dMatrix[index][i]
        index = tmpindex
        pickupLocOrder.append(next)
        visitedIndex.append(index)
        #we need to return indexlist, in order to find the ID 
    return pickupLocOrder, visitedIndex
'''
choose pick up products from up/down/left/right 
based on current location, the next pickup product's location and the pickup product's location after next
'''  
def choosePoint(currentLoc, firstLoc, secondLoc):  
    x, y = currentLoc
    x1, y1 = firstLoc
    x2, y2 = secondLoc
    # currentloc and secondpickupProduct are both below the firstpickupProduct
    if y<y1 and y2<y1:
        if (y1-1)>0:
            firstLoc = (x1, y1-1)
            return firstLoc
        else:
            if (x1-1, y1) not in productLocation:
                firstLoc = (x1-1, y1)
            else:
                firstLoc = (x1,y1+1)
            return firstLoc 
    # currentloc and secondpickupProduct are both above the firstpickupProduct    
    if y>y1 and y2>y1:
        if (y1+1) < maxHeight:
            firstLoc = (x1, y1+1) 
        else:
            if (x1-1, y1) not in productLocation:
                firstLoc = (x1-1, y1)
            else:
                firstLoc = (x1,y1-1)
        return firstLoc
    # currentloc and secondpickupProduct are both on the left side of the firstpickupProduct / other leftside pickup situations 
    if (x<x1 and x2<=x1) or (y>y1 and x2<x1 and y2<y1):
        if (x1-1, y1) not in productLocation:
            firstLoc = (x1-1, y1)
        else:
            firstLoc = (x1, y1+1)
        return firstLoc
    # currentloc and secondpickupProduct are both on the right side of the firstpickupProduct / other rightside pickup situations
    if (x>x1 and x2>x1) or (y2>y1 and x2>x1 and y<y1 and x<x1 ):
        if (x1+1, y1) not in productLocation:
            firstLoc = (x1+1, y1)
        elif (x1-1, y1) not in productLocation:
            firstLoc = (x1-1, y1)
        else:
            firstLoc = (x1, y1+1)
        return firstLoc
    #rest of the situations
    if y2 >= y1:
        firstLoc = (x1, y1 + 1)
    else:
        firstLoc = (x1, y1 - 1)
    return firstLoc



###########################################################################################################
#Brute Force Functions
###########################################################################################################
def generateBfroutelist(node,productLocList,path):
    path.append(node)
    if (len(productLocList) + 1 == len(path)):
        bfroutelist.append(path[1:])
    else:
        for product in productLocList:
            if (product not in path):
                generateBfroutelist(product, productLocList, list(path))

def bfneighbours(bfroute, map) :
    neighbours = []
    for node in bfroute:
        neighbours.append(findNeighbours(map, node))
    return neighbours

def bfonepath(node, neighbours, path, distance, end):
    # memory3 = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    # print(u'Current Memory：%.4f MB' % (memory3 - memory))
    etime = timer()
    if (etime - sstime) > timelimit:
        return
    path.append(node)
    # Calculate path length from current to last node
    if len(path) > 1:
        if (node in bfdict and path[-2] in bfdict[node]):
            distance += bfdict[node][path[-2]]
        elif (path[-2] in bfdict and node in bfdict[path[-2]]):
            distance += bfdict[path[-2]][node]
        else:
            length = len(bfs(warehouseMap, path[-2], node)) - 1
            distance += length
            bfdict[path[-2]] = {node: length}
        # distance += len(bfs(warehouseMap, path[-2], node)) - 1
    # If path contains all cities and is not a dead end,
    # add path from last to first city and return.
    if (len(neighbours) + 1 == len(path)):
        path.append(end)
        if (end in bfdict and path[-2] in bfdict[end]):
                distance += bfdict[end][path[-2]]
        elif (path[-2] in bfdict and end in bfdict[path[-2]]):
                distance += bfdict[path[-2]][end]
        else:
            length = len(bfs(warehouseMap, path[-2], end)) - 1
            distance += length
            bfdict[path[-2]] = {end: length}
        # distance += len(bfs(warehouseMap, path[-2], end)) - 1
        global bfroutes
        bfroutes.append([distance, path])
        bfroutes.sort()
        best = bfroutes[0]
        bfroutes = []
        bfroutes.append(best)
        return

    # Fork paths for all possible cities not yet used
    for neighbour in neighbours:
        i = 0
        for n in neighbour:
            if (n not in path) :
                i += 1
        if ( i== len(neighbour)):
            for n in neighbour:
                bfonepath(n, neighbours, list(path), distance, end)

def bfallpath(start, end, productLocList):
    productLocList1 = []
    for i in productLocList:
        if not i in productLocList1:
            productLocList1.append(i)
    generateBfroutelist(start, productLocList1, [])
    global sstime
    sstime = timer()
    for route in bfroutelist:
        neighbour = bfneighbours(route, warehouseMap)
        bfonepath(start, neighbour, [], 0, end)
    shortestpath,shortestdistance = bfroutes[0]
    return shortestpath,shortestdistance

def bffindNeighbours(map, location):
    neighbours = []
    h = len(map)
    w = len(map[0])
    x, y = location
    if x + 1 < w and map[y][x+1] == 1:
        neighbours.append((x+1, y))
    if x - 1 >= 0 and map[y][x-1] == 1:
        neighbours.append((x-1, y))

    if y + 1 < h and map[y+1][x] == 1:
        neighbours.append((x, y+1))

    if y - 1 >= 0 and map[y-1][x] == 1:
        neighbours.append((x, y-1))
    return neighbours




if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_loading()
    sys.exit(app.exec_())


