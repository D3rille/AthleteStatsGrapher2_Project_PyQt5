
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.uic import loadUi
import mysql.connector
from mysql.connector import errorcode

class Athlete_repo(QMainWindow):
     #connect to MySQL database
    cnx = mysql.connector.connect(
         user="root", 
        password="root", 
        host="localhost", 
        database="athletedb")
    
    
    def __init__(self):
        super(Athlete_repo,self).__init__()
        loadUi('athleteMainWindow.ui',self)
        cursor = self.cnx.cursor()  
        cursor.execute("SELECT * FROM teams")
        for row in cursor:
            self.cb_team_searchP.addItem(row[0])
       
        cursor.execute("SELECT * FROM playerinfo WHERE teamName = '%s'" % self.cb_team_searchP.currentText())
        for row in cursor:
            self.cb_searchPlayerId.addItem(row[0])
        cursor.close ()
       
        #Assign function to be called when button is clicked
        self.searchBtn_player.clicked.connect(self.searchPlayer)
        self.actionSearchTeam.triggered.connect(self.goToWindow2)
        self.actionAddPlayer.triggered.connect(self.playerAddition)
        self.actionAddTeam.triggered.connect(self.teamAddition)
        self.actionAddUpdateStats.triggered.connect(self.statsAddition)
        self.cb_team_searchP.currentTextChanged.connect(self.set_id)
        self.deletePlayerBtn.clicked.connect(self.deletePlayer)
        self.showGraphBtn_player.clicked.connect(self.plot_player)
        self.actionExit.triggered.connect(self.exitApp)
      
        
    def goToWindow2(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def setTeams(self):
        cursor = self.cnx.cursor()  
        cursor.execute("SELECT * FROM teams")
        for row in cursor:
            self.cb_team_searchP.addItem(row[0])
        self.set_id()
    def set_id(self):
        try:
            cursor = self.cnx.cursor()
            self.cb_searchPlayerId.clear()
            cursor.execute("SELECT * FROM playerinfo WHERE teamName = '%s'" % self.cb_team_searchP.currentText())
            for row in cursor:
                self.cb_searchPlayerId.addItem(row[0])
            cursor.close()
            
        
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Access Error", "Something is wrong with your user name or password", )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist")
            elif err.errno == 1062:
                QMessageBox.critical(self, "Record Error", "Duplicate Product Code")
            else:
                QMessageBox.critical(self, "Error", str(err)) 
                
   
    def ave(self, matches, record):
       average= round((record / matches), 2)
       return average
   
    def reset(self):
        self.display_lname.setText("Last Name")
        self.display_fname.setText("First Name")
        self.display_jersey.setText("#0")
        self.display_height.setText("0")
        self.display_weight.setText("0")
        self.playerProfile.setPixmap(QtGui.QPixmap("placeholder.jpg"))
        
                
    def searchPlayer(self):
        try:
            cursor = self.cnx.cursor()
            cursor.execute("SELECT * FROM playerinfo WHERE playerId = '%s'" % self.cb_searchPlayerId.currentText())
            row = cursor.fetchone()
            
            if row is not None:
                self.display_lname.setText(row[1])
                self.display_fname.setText(row[2])
                self.display_bdate.setText(str(row[3]))
                self.display_position.setText(row[5])
                self.display_jersey.setText(str(row[6]))
                self.display_height.setText(str(row[7]))
                self.display_weight.setText(str(row[8]))
                self.playerProfile.setPixmap(QtGui.QPixmap("Players/"+ row[9]))
                
                cursor.execute("SELECT teamName FROM playerinfo WHERE playerId= '%s'" % self.cb_searchPlayerId.currentText())
                row=cursor.fetchone()
                if row is not None:
                    self.cb_team_searchP.setCurrentText(row[0])

                cursor.execute("SELECT * FROM playerperformance WHERE playerId = '%s'" % self.cb_searchPlayerId.currentText())
                row= cursor.fetchone()
                if row is not None:
                    matches= row[2]
                    self.display_GP.setText(str(matches))
                    self.display_points.setText(str(self.ave(matches, row[3])))
                    self.display_assists.setText(str(self.ave(matches, row[4])))
                    self.display_rebounds.setText(str(self.ave(matches, row[5])))
                    self.display_steals.setText(str(self.ave(matches, row[6])))
                    self.display_blocks.setText(str(self.ave(matches, row[7])))
            else:
                QMessageBox.information(self, "Not Found", "Record does not exist.")
            cursor.close()
        
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Access Error", "Something is wrong with your user name or password", )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist")
            elif err.errno == 1062:
                QMessageBox.critical(self, "Record Error", "Duplicate SSID Code")
            else:
                QMessageBox.critical(self, "Error", str(err))
                
    def deletePlayer(self):
        try:
            reply = QMessageBox.warning(self, "Delete", "Do you want to delete this record?", QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                cursor = self.cnx.cursor()
                cursor.execute("DELETE FROM playerinfo WHERE playerId = '%s'" % self.cb_searchPlayerId.currentText())
                self.cnx.commit()
                cursor.close()
                QMessageBox.information(self, 'Record Deleted!', 'The record has been deleted.', QMessageBox.Ok)
            
                self.reset()
                self.set_id()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Access Error", "Something is wrong with your user name or password", )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist")
            elif err.errno == 1062:
                QMessageBox.critical(self, "Record Error", "Duplicate SSID Code")
            else:
                QMessageBox.critical(self, "Error", str(err))
                      
    def playerAddition(self):
        pwidget= Player_addition()
        pwidget.window_closed.connect(self.setTeams)
        pwidget.exec()
        
    def teamAddition(self):
        twidget= Team_addition()
        twidget.exec()
        
    def statsAddition(self):
        swidget= Stats_addition()
        swidget.exec()
        
    def exitApp(self):
        widget.close()
        
        
    def plot_player(self):
        maxVal = [30.12, 11.19, 22.89, 2.71, 3.50]
        stats=[]
        cursor = self.cnx.cursor()
        cursor.execute("SELECT * FROM playerperformance WHERE playerId = '%s'" % self.cb_searchPlayerId.currentText())
        row= cursor.fetchone()
        if row is not None:
            matches= row[2]
            for x in range(3,8):
                y= round((self.ave(matches, row[x])/maxVal[x-3]), 2)
                stats.append(y)     
        
        else:
            QMessageBox.information(self, "Not Found", "Record does not exist.")
        cursor.execute("SELECT * FROM playerinfo WHERE playerId = '%s'" % self.cb_searchPlayerId.currentText())
        row= cursor.fetchone()
        if row is not None:
            title = row[2] + " "+ row[1]
        cursor.close()
        graph= Graph(stats, title)
        graph.exec()
        

class Graph(QDialog):
                 
    def __init__(self, stats, title, parent=None):
        super(Graph, self).__init__(parent)
        self.stats = stats
        self.title= title
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_ylabel('Percentage')
        ax.set_title(self.title)
        statslbl = ['Scoring', 'Assisting', 'Rebounding', 'Stealing', 'Blocking']
        ax.bar(statslbl, self.stats)
        self.canvas.draw()

class Athlete_repo2(QMainWindow):
    #connect to MySQL database
    cnx = mysql.connector.connect(
         user="root", 
        password="root", 
        host="localhost", 
        database="athletedb")
    
    def __init__(self):
        super(Athlete_repo2,self).__init__()
        loadUi('athleteMainWindow_SearchTeam.ui',self)
        
        cursor = self.cnx.cursor()  
        cursor.execute("SELECT * FROM teams")
        for row in cursor:
            self.cb_searchTeamName.addItem(row[0])
        cursor.close()
        
        self.searchBtn_team.clicked.connect(self.searchTeam)
        self.actionSearchPlayer.triggered.connect(self.goToWindow1)
        self.deleteTeamBtn.clicked.connect(self.deleteTeam)
        self.actionAddTeam.triggered.connect(self.teamAddition)
        self.actionAddPlayer.triggered.connect(self.playerAddition)
        self.actionAddUpdateStats.triggered.connect(self.statsAddition)
        self.showGraphBtn_team.clicked.connect(self.plot_team)
        
        
    def playerAddition(self):
        pwidget= Player_addition()
        pwidget.exec()
    
    def teamAddition(self):
        twidget= Team_addition()
        twidget.exec()
    
    def statsAddition(self):
        swidget= Stats_addition()
        swidget.exec()        
        
    def goToWindow1(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        
    def reset(self):
        self.display_teamName.setText("Team Name")
        self.display_wins.setText(str(0))
        self.display_loses.setText(str(0))
        self.display_pointsT.setText(str(0))
        self.display_assistsT.setText(str(0))
        self.display_reboundsT.setText(str(0))
        self.display_stealsT.setText(str(0))
        self.display_blocksT.setText(str(0))
        self.teamLogo.setPixmap(QtGui.QPixmap("photo_placeholder2.png"))
        
    def setTeams(self):
        cursor = self.cnx.cursor()  
        cursor.execute("SELECT * FROM teams")
        for row in cursor:
            self.cb_searchTeamName.addItem(row[0])
        
    def searchTeam(self):
        try:
            cursor = self.cnx.cursor()
            cursor.execute("SELECT * FROM teams WHERE teamName = '%s'" % self.cb_searchTeamName.currentText())
            row = cursor.fetchone()
            
            if row is not None:
                self.display_teamName.setText(row[0])
                self.display_wins.setText(str(row[1]))
                self.display_loses.setText(str(row[2]))
                self.display_pointsT.setText(str(row[3]))
                self.display_assistsT.setText(str(row[4]))
                self.display_reboundsT.setText(str(row[5]))
                self.display_stealsT.setText(str(row[6]))
                self.display_blocksT.setText(str(row[7]))
                self.teamLogo.setPixmap(QtGui.QPixmap("Teams/"+ row[8]))
                
            else:
                QMessageBox.information(self, "Not Found", "Record does not exist.")
            cursor.close()
        
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Access Error", "Something is wrong with your user name or password", )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist")
            elif err.errno == 1062:
                QMessageBox.critical(self, "Record Error", "Duplicate SSID Code")
            else:
                QMessageBox.critical(self, "Error", str(err))
                
    def deleteTeam(self):
        try:
            reply = QMessageBox.warning(self, "Delete", "Do you want to delete this record?", QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                cursor = self.cnx.cursor()
                cursor.execute("DELETE FROM teams WHERE teamName = '%s'" % self.cb_searchTeamName.currentText())
                self.cnx.commit()
                cursor.close()
                QMessageBox.information(self, 'Record Deleted!', 'The record has been deleted.', QMessageBox.Ok)
            
                self.reset()
                self.cb_searchTeamName.clear()
                self.setTeams()
                

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Access Error", "Something is wrong with your user name or password", )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist")
            elif err.errno == 1062:
                QMessageBox.critical(self, "Record Error", "Duplicate SSID Code")
            else:
                QMessageBox.critical(self, "Error", str(err))
            
    def plot_team(self):
        maxVal = [126.5, 31.40, 71.53, 9.1, 8.73]
        stats=[]
        cursor = self.cnx.cursor()
        cursor.execute("SELECT * FROM teams WHERE teamName = '%s'" % self.cb_searchTeamName.currentText())
        row= cursor.fetchone()
        if row is not None:
            for x in range(3,8):
                y= round((row[x]/maxVal[x-3]), 2)
                stats.append(y)
            title= row[0]
        else:
            QMessageBox.information(self, "Not Found", "Record does not exist.")
        cursor.close()
        graph= Graph(stats, title)
        graph.exec()
   

class Player_addition(QDialog):
    
    #connect to MySQL database
    cnx = mysql.connector.connect(
         user="root", 
        password="root", 
        host="localhost", 
        database="athletedb")
        
    def __init__(self):
        super(Player_addition,self).__init__()
        loadUi('addPlayer.ui',self)
        
        cursor = self.cnx.cursor()  
        cursor.execute("SELECT position_name FROM positions")
        for row in cursor:
            self.cb_position.addItem(row[0])
         
        cursor.execute("SELECT * FROM teams")
        for row in cursor:
            self.cb_team_addplayer.addItem(row[0])
        cursor.close()
        
    
        self.addBtn_addplayer.clicked.connect(self.addPlayer)
        self.resetBtn_addplayer.clicked.connect(self.reset)
               
        
     #used to get date from the dateEdit widget           
    def getDate(self):
        temp_var = self.de_birthdate.date()
        date = temp_var.toPyDate()
        return date
    
    def reset(self):
        self.le_playerId.setText("")
        self.le_lastName.setText("")
        self.lineEdit_3.setText("")
        self.sb_jerseyNo.setValue(0)
        self.le_height.setText("")
        self.le_weight.setText("")
        self.le_photoname.setText("")
    
    def addPlayer(self):
        try:
            # Database Connection
            cursor = self.cnx.cursor()
            # Insert new student information
            cursor.execute("INSERT INTO playerinfo VALUES ('%s', '%s','%s','%s','%s','%s','%s', '%s', '%s', '%s')" % (
                self.le_playerId.text(),
                self.le_lastName.text(),
                self.lineEdit_3.text(),
                self.getDate(),
                self.cb_team_addplayer.currentText(),
                self.cb_position.currentText(),
                self.sb_jerseyNo.value(),
                self.le_height.text(),
                self.le_weight.text(),
                self.checkPic()
                ))
            self.cnx.commit()
            cursor.close()
            QMessageBox.information(self, 'Record Added!', 'The record has been added.', QMessageBox.Ok)
            
            self.close()
           
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Access Error", "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist")
            elif err.errno == 1062:
                QMessageBox.critical(self, "Record Error", "Duplicate SSID")
            else:
                QMessageBox.critical(self, "Error", str(err))
    def checkPic(self):
        if not self.le_photoname.text() == "":
            return self.le_photoname.text()
        else:
            return 'placeholder1.1.jpg'
                
class Team_addition(QDialog):
    #connect to MySQL database
    cnx = mysql.connector.connect(
         user="root", 
        password="root", 
        host="localhost", 
        database="athletedb")
    
    def __init__(self):
        super(Team_addition,self).__init__()
        loadUi('addTeam.ui',self)
        
        cursor = self.cnx.cursor()  
        cursor.execute("SELECT * FROM teams")
        for row in cursor:
            self.cb_teamName_AddUpdate.addItem(row[0])
            self.sb_wins.setValue(row[1])
            self.sb_losses.setValue(row[2])
            self.dsb_points.setValue(row[3])
            self.dsb_assists.setValue(row[4])
            self.dsb_rebounds.setValue(row[5])
            self.dsb_steals.setValue(row[6])
            self.dsb_blocks.setValue(row[7])
        
        cursor.execute("SELECT pic_filename FROM teams WHERE teamName = '%s'" % self.cb_teamName_AddUpdate.currentText())
        for row in cursor:
            self.le_photoName.setText(row[0])
            self.teamlogo.setPixmap(QtGui.QPixmap("Teams/"+ row[0]))
        
        cursor.close()   
            
        self.addBtn_addteam.clicked.connect(self.addTeam)
        self.resetBtn_addteam.clicked.connect(self.reset)
        self.le_photoName.textChanged.connect(self.loadLogo)
        self.updateTeamBtn.clicked.connect(self.updateTeam)
        self.cb_teamName_AddUpdate.currentTextChanged.connect(self.loadInfo)
    
    def loadInfo(self):
        cursor = self.cnx.cursor()
        cursor.execute("Select * FROM teams WHERE teamName = '%s'" % self.cb_teamName_AddUpdate.currentText())
        for row in cursor:
            self.sb_wins.setValue(row[1])
            self.sb_losses.setValue(row[2])
            self.dsb_points.setValue(row[3])
            self.dsb_assists.setValue(row[4])
            self.dsb_rebounds.setValue(row[5])
            self.dsb_steals.setValue(row[6])
            self.dsb_blocks.setValue(row[7])
            self.le_photoName.setText(row[8])
            self.teamlogo.setPixmap(QtGui.QPixmap("Teams/"+ row[8]))
        
    def reset(self):
        self.sb_wins.setValue(0),
        self.sb_losses.setValue(0),
        self.dsb_points.setValue(0),
        self.dsb_assists.setValue(0),
        self.dsb_rebounds.setValue(0),
        self.dsb_steals.setValue(0),
        self.dsb_blocks.setValue(0),
        self.le_photoName.setText("")
        self.teamlogo.setPixmap(QtGui.QPixmap("photo_placeholder2.png"))
        
    def addTeam (self):
        try:
            # Database Connection
            cursor = self.cnx.cursor()
            # Insert new student information
            cursor.execute("INSERT INTO teams VALUES ('%s', '%s','%s','%s','%s','%s','%s', '%s', '%s')" % (
                self.cb_teamName_AddUpdate.currentText(),
                self.sb_wins.value(),
                self.sb_losses.value(),
                self.dsb_points.value(),
                self.dsb_assists.value(),
                self.dsb_rebounds.value(),
                self.dsb_steals.value(),
                self.dsb_blocks.value(),
                self.checkLogo()
                ))
            self.cnx.commit()
            cursor.close()
            QMessageBox.information(self, 'Record Added!', 'The record has been added.', QMessageBox.Ok)
            
            self.close()
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Access Error", "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist")
            elif err.errno == 1062:
                QMessageBox.critical(self, "Record Error", "Duplicate SSID")
            else:
                QMessageBox.critical(self, "Error", str(err))
                
    def checkLogo(self):
        if not self.le_photoName.text() == "":
            return self.le_photoName.text()
        else:
            return 'photo_placeholder2.1.png'
                
    def loadLogo(self):
        # cursor= self.cnx.cursor()
        # cursor.execute("SELECT pic_filename FROM teams WHERE")
        try:
            self.teamlogo.setPixmap(QtGui.QPixmap("Teams/"+ self.le_photoName.text()))
        except:
            self.teamlogo.setPixmap(QtGui.QPixmap("photo_placeholder2.png"))
            
    
            
    def updateTeam(self):
        try:
            reply = QMessageBox.warning(self, "Update", "Do you want to update this record?", QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                cursor = self.cnx.cursor()
                query = "UPDATE teams SET wins= %s, loses= %s, ave_scores= %s, ave_assists= %s, ave_rebound = %s, ave_steals=%s, ave_blocks= %s, pic_filename=%s WHERE teamName= %s "
                val = (self.sb_wins.value(), self.sb_losses.value(), self.dsb_points.value(), self.dsb_assists.value(), self.dsb_rebounds.value(), self.dsb_steals.value(), 
                    self.dsb_blocks.value(), self.checkLogo(), self.cb_teamName_AddUpdate.currentText())
                cursor.execute(query, val)
                self.cnx.commit()
                cursor.close()
                QMessageBox.information(self, 'Record Updated!', 'The record has been updated.', QMessageBox.Ok)
                self.close()
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Access Error", "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist")
            elif err.errno == 1062:
                QMessageBox.critical(self, "Record Error", "Duplicate SSID")
            else:
                QMessageBox.critical(self, "Error", str(err))
        
                
                
class Stats_addition(QDialog):
    #connect to MySQL database
    cnx = mysql.connector.connect(
        user="root", 
        password="root", 
        host="localhost", 
        database="athletedb")
    
    def __init__(self):
        super(Stats_addition,self).__init__()
        loadUi('addStats.ui',self)
        
        #put product codes to combobox
        cursor = self.cnx.cursor()
        cursor.execute("SELECT pp.playerId, pi.last_name, pi.first_name, pi.teamName, pi.position_name, pi.pic_filename FROM playerinfo pi JOIN teams t ON pi.teamName = t.teamName JOIN playerperformance pp ON pi.playerId = pp.playerId")
        # cursor.execute("SELECT * FROM playerinfo WHERE teamName = '%s'" % self.cb_team_addstats.currentText())
        for row in cursor:
            self.cb_playerId.addItem(row[0])
        cursor.execute("SELECT playerId, last_name, first_name, teamName, position_name, pic_filename FROM playerinfo WHERE playerId = %s " % self.cb_playerId.currentText())
        for row in cursor:
            self.cb_teamAddstats.addItem(row[3])
            self.lbl_name_addstat.setText(row[2]+ " "+ row[1])
            self.lbl_team_addstat.setText(row[3])
            self.lbl_position_addstat.setText(row[4])
            self.profilepic_addstat.setPixmap(QtGui.QPixmap("Players/"+ row[5]))
        cursor.execute("SELECT * FROM playerperformance WHERE playerId= %s"% self.cb_playerId.currentText())
        for row in cursor:
            self.sb_matches.setValue(row[2])
            self.sb_points.setValue(row[3])
            self.sb_assists.setValue(row[4])
            self.sb_rebounds.setValue(row[5])
            self.sb_steals.setValue(row[6])
            self.sb_blocks.setValue(row[7])
        cursor.close ()
        
    
        self.resetBtn_addstats.clicked.connect(self.resetStats)
        self.cb_playerId.currentTextChanged.connect(self.loadInfo)
        self.updateBtn_addStats.clicked.connect(self.updateStats)
        self.addBtn_addstats.clicked.connect(self.addStats)
       
        
    def resetStats(self):
        self.sb_matches.setValue(0)
        self.sb_points.setValue(0)
        self.sb_assists.setValue(0)
        self.sb_rebounds.setValue(0)
        self.sb_steals.setValue(0)
        self.sb_blocks.setValue(0)
        
                

    def loadInfo(self):
        cursor= self.cnx.cursor()
        cursor.execute("SELECT * FROM playerinfo WHERE playerId ='%s'" % self.cb_playerId.currentText())
        for row in cursor:
            self.cb_teamAddstats.setCurrentText(row[4])
            self.lbl_team_addstat.setText(row[4])
            self.lbl_name_addstat.setText(row[2]+" "+ row[1])
            self.lbl_team_addstat.setText(row[4])
            self.lbl_position_addstat.setText(row[5])
            self.profilepic_addstat.setPixmap(QtGui.QPixmap("Players/"+ row[9]))
        cursor.execute("SELECT * FROM playerperformance WHERE playerId= %s"% self.cb_playerId.currentText())
        for row in cursor:
            self.sb_matches.setValue(row[2])
            self.sb_points.setValue(row[3])
            self.sb_assists.setValue(row[4])
            self.sb_rebounds.setValue(row[5])
            self.sb_steals.setValue(row[6])
            self.sb_blocks.setValue(row[7])
            
        cursor.close()
        
    def addStats(self):
        try:
            # Database Connection
            cursor = self.cnx.cursor()
            # Insert new student information
            query =  ("INSERT INTO playerperformance "
               "(statId, playerId, no_Matches, points, assists, rebounds, steals, blocks) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            val = (self.cb_playerId.currentText(), self.cb_playerId.currentText(), self.sb_matches.value(), self.sb_points.value(), self.sb_assists.value(),  self.sb_rebounds.value(),self.sb_steals.value(), self.sb_blocks.value())
            cursor.execute(query, val)
            self.cnx.commit()
            cursor.close()
            QMessageBox.information(self, 'Record Added!', 'The record has been added.', QMessageBox.Ok)
            
            self.close()
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Access Error", "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist")
            elif err.errno == 1062:
                QMessageBox.critical(self, "Record Error", "Duplicate SSID")
            else:
                QMessageBox.critical(self, "Error", str(err))

            
    def updateStats(self):
        try:
            reply = QMessageBox.warning(self, "Update", "Do you want to update this record?", QMessageBox.Yes, QMessageBox.No)
    
            if reply == QMessageBox.Yes:
                cursor = self.cnx.cursor()
                cursor.execute("UPDATE playerperformance SET no_Matches = '%s', points='%s', assists= '%s', rebounds= '%s', steals='%s', blocks='%s' WHERE playerId = '%s'" % 
                               (self.sb_matches.value(),
                                self.sb_points.value(),
                                self.sb_assists.value(),
                                self.sb_rebounds.value(),
                                self.sb_steals.value(),
                                self.sb_blocks.value(), 
                                self.cb_playerId.currentText())) 
                self.cnx.commit()
                cursor.close()
                QMessageBox.information(self, 'Record Updated!', 'The record has been updated.', QMessageBox.Ok)
    
                self.close()
            
    
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Access Error", "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist")
            elif err.errno == 1062:
                QMessageBox.critical(self, "Record Error", "Duplicate SSID")
            else:
                QMessageBox.critical(self, "Error", str(err))
                
    
    
        
if __name__== "__main__":  
    import sys
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    window1= Athlete_repo()
    window2= Athlete_repo2()
    widget.addWidget(window1)
    widget.addWidget(window2)
    widget.setFixedHeight(770)
    widget.setFixedWidth(1000)
    widget.update()
    widget.show()
    sys.exit(app.exec_())
