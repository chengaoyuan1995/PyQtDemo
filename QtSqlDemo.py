import sys,re
from PyQt5.QtWidgets import QMainWindow,QTableView,QMessageBox,QWidget,QInputDialog,QPushButton,QHBoxLayout,QVBoxLayout,QApplication,QGroupBox
from PyQt5.QtSql import QSqlDatabase,QSqlTableModel,QSqlQuery,QSqlError
from PyQt5.QtCore import Qt
 
class Judege_English():
    def judge(self,context):
        context=str(context)
        result=re.findall('[a-zA-Z]',context)
        if len(context)!=len(result):
            return 0
        else:
            return 1
 
class DbOp(QSqlDatabase):
    def __init__(self):
        super().__init__()
        self.db=''
        self.model=''
 
    def database_creator(self,text):
        #创建连接数据库
        self.db=self.addDatabase('QSQLITE') #1，加载驱动
        self.db.setDatabaseName('{}.sqlite'.format(text))#2，设置数据库的名称，或访问已经存在的数据库
        return self.db.open() #打开数据库
 
    def table_creator(self,text):
            querry=QSqlQuery()
            querry.exec_("create table {} (id int primary key,name varchar(20),email varchar(30))".format(text))
     
    def check_table(self,table_name):
        list_table=self.db.tables() 
        if table_name in list_table:
            return 1
        else:
            return 0
 
    def data_show(self,table_name):
        #1,建立模型类Qsqtablemodel
        self.model=QSqlTableModel()
        #2，表与模型类建立联系
        self.model.setTable(table_name)
        #3，表的更改时否同步到数据库
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        #4，设置表的标题行
        self.model.setHeaderData(0,Qt.Horizontal,'id')
        self.model.setHeaderData(1,Qt.Horizontal,'姓名')
        self.model.setHeaderData(2,Qt.Horizontal,'邮箱')
        #5，模型类查询
        self.model.select()
        #6模型类加载到Qtableview显示
        return self.model
 
    def data_add(self):
        row=self.model.rowCount()
        self.model.insertRow(row)
        self.model.submit()
    
 
    def data_del(self,row):
        self.model.removeRow(row)
        self.model.submit()
 
    def data_close(self):
        self.db.close()
        
 
 
class sqlDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dbop=DbOp()
        self.table_name=''
    def initUI(self):
        self.setWindowTitle('界面对数据库操作')
        self.resize(600,400)
        widget=QWidget()
        self.setCentralWidget(widget)
        layout=QHBoxLayout()
        widget.setLayout(layout)
 
#左边
        box=QGroupBox('数据库按钮')
        boxlayout=QVBoxLayout()
        box.setLayout(boxlayout)
        #添加数据库按钮
        self.b1=QPushButton('创建连接数据库')
        boxlayout.addWidget(self.b1)
        self.b1.clicked.connect(self.create_db)
        self.b11=QPushButton('创建表')
        boxlayout.addWidget(self.b11)
        self.b11.setEnabled(False)
        self.b11.clicked.connect(self.create_table)
        self.b11.clicked.connect(self.create_table)
        self.b2=QPushButton('浏览数据')
        boxlayout.addWidget(self.b2)
        self.b2.setEnabled(False)
        self.b2.clicked.connect(self.show_db)
        self.b3=QPushButton('添加一行')
        boxlayout.addWidget(self.b3)
        self.b3.setEnabled(False)
        self.b3.clicked.connect(self.add_db)
        self.b4=QPushButton('删除一行')
        boxlayout.addWidget(self.b4)
        self.b4.setEnabled(False)
        self.b4.clicked.connect(self.del_db)
        self.b5=QPushButton('退出')
        boxlayout.addWidget(self.b5)
        self.b5.setEnabled(False)
        self.b5.clicked.connect(self.exit_db)
 
        layout.addWidget(box)
 
#右边
        self.tableview=QTableView()
        layout.addWidget(self.tableview)
        layout.setStretchFactor(box,1)
        layout.setStretchFactor(self.tableview,3)
 
        
 
    def create_db(self):
        text,ok=QInputDialog.getText(self,'数据库名称','输入数据库名称（输入英文）')
        j=Judege_English()
        if ok and (text.replace(' ','')!='')and j.judge(text):
            fin=self.dbop.database_creator(text)
            if fin:
                self.b11.setEnabled(True)
                self.b2.setEnabled(True)
                
       
 
        else:
            QMessageBox.critical(self,'信息','输入的名字有误,请从新创建',QMessageBox.Ok|QMessageBox.No,QMessageBox.Ok)
            
    def create_table(self):
        text,ok=QInputDialog.getText(self,'数据表的名称添加','输入表名(输入英文)')
        j=Judege_English()
        if ok and (text.replace(' ','')!='')and j.judge(text):
            self.dbop.table_creator(text)        
        else:
            QMessageBox.critical(self,'信息','输入的名字有误,请从新创建',QMessageBox.Ok|QMessageBox.No,QMessageBox.Ok)
 
        
    def show_db(self):
        table_name,ok=QInputDialog.getText(self,'展示数据表','输入表名(输入英文)')
        #判断是否存在输入的表
        isbeing=self.dbop.check_table(table_name)
        #存在
        if isbeing:
            model=self.dbop.data_show(table_name)
            self.tableview.setModel(model)
            self.table_name=table_name
            self.b3.setEnabled(True)
            self.b4.setEnabled(True)
            self.b5.setEnabled(True)
        #不存在
        else:
            QMessageBox.critical(self,'信息','表不存在',QMessageBox.Ok|QMessageBox.No,QMessageBox.Ok)
            self.b3.setEnabled(False)
            self.b4.setEnabled(False)
            self.b5.setEnabled(False)        
    def add_db(self):
        self.dbop.data_add()
    
    def del_db(self):
        row=self.tableview.currentIndex().row()
        self.dbop.data_del(row)
    
    def exit_db(self):
        self.dbop.data_close()
       
        self.b11.setEnabled(False)
        self.b2.setEnabled(False) 
        self.b3.setEnabled(False)
        self.b4.setEnabled(False)
        self.b5.setEnabled(False) 
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    demo=sqlDemo()
    demo.show()
    sys.exit(app.exec_())