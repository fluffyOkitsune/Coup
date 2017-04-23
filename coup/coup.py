'''
@author: おきつね
'''

# import pdb; pdb.set_trace()

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QImage, QColor, QPainter, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)


#--------------------------------------------------
# ウィンドウ
#--------------------------------------------------
class MainWindow(QWidget):
    # 定数
    WINDOW_WIDTH = 160
    WINDOW_HEIGHT = 144
    FPS = 60
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.graphicsView = QGraphicsView()
        
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, MainWindow.WINDOW_WIDTH, MainWindow.WINDOW_HEIGHT)
         
        self.graphicsView.setScene(scene)
        self.screen = Screen(MainWindow.WINDOW_WIDTH, MainWindow.WINDOW_HEIGHT)
        
        scene.addItem(self.screen)

        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.graphicsView)

        self.setLayout(mainLayout)
        self.setWindowTitle("Coup")
        self.updating_rule = False
        self.show()
        
        # タイマースタート
        self.timer = QTimer()
        self.timer.setInterval(int(1000 / MainWindow.FPS))
        self.timer.timeout.connect(self.timeout)
        self.timer.start()
        
    def timeout(self):
        self.screen.gameObj.run()
        self.screen.update()
        self.screen.gameObj.gameTime += 1

    def reset(self):
        self.screen.gameObj.reset()
        self.screen.update()
        
    def keyPressEvent(self, e):
        self.screen.gameObj.keyPressEvent(e)
    
class Screen(QGraphicsItem):
    def __init__(self, width=MainWindow.WINDOW_WIDTH, height=MainWindow.WINDOW_HEIGHT):
        super(Screen, self).__init__()
        
        # 画面のサイズ
        self.width = width
        self.height = height
        
        # ゲームのオブジェ
        self.gameObj = Coup()
        
    # Override
    def paint(self, painter, option, widget):
        self.gameObj.draw(painter)

    # Override
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

import random
import math

# interface
class GameObj :
    def reset(self):
        pass
    
    def run(self):
        pass
            
    def draw(self, painter):
        pass
        
    def keyPressEvent(self, e):
        pass

class Coup(GameObj):
    """大人気謀殺ゲーム「クー」"""
    
    CHIP_SIZE = 16
    FACE_SIZE = 48
    IMG_PATTERN = QImage('pattern.png')
    IMG_FACE = QImage('faces.png')

    def __init__(self):
        self.database = Database()
        
        # ゲーム開始からのフレーム数
        self.gameTime = 0
        
        # オブジェ生成
        self.title = Title(self)
        self.playing = Playing(self)
        
        # イニシャライズ
        self.reset()
        
    def reset(self):        
        self.title.reset()
        self.playing.reset()
        
        self.sceneTmp = self.title
        self.scene = self.sceneTmp
        
    def run(self):
        if self.sceneTmp != None:
            self.scene = self.sceneTmp
            self.sceneTmp = None
        self.scene.run()
        
    def draw(self, painter):
        self.scene.draw(painter)
        
    def keyPressEvent(self, e):
        self.scene.keyPressEvent(e);
        
    def changeScene(self, nextScene):
        if self.sceneTmp == None:
            self.sceneTmp = nextScene
            self.sceneTmp.reset()
    
class Database():
    def __init__(self):
        # 思考中のセリフ
        self.quoteThinking = [
            # 僧侶の人
            [u"ふむ……"],
            # 真実ちゃん
            [u"ふぅん、それならねぇ……"],
            # ちいちい
            [u"(๑╹ω╹)"]
        ]
        # ダウト時のセリフ
        self.quoteDoubt = [
            # 僧侶の人
            [u"怪しい行動ですね……", u"それはダウトです！"],
            # ちゃんレナ
            [u""],
            # 真実ちゃん
            [u"それは嘘"],
            # ちいちい
            [u"(๑╹ω╹)",
             u"(๑╹ω╹)＜ㄘい",
             u"(๑╹ω╹)＜ㄘいㄘい",
             u"(๑╹ω╹)＜ㄘいㄘい通ると思ったんカ",
             u"(๑╹ω╹)＜そんなハッタリで、\nㄘいㄘい嘘通ると思ったんカ",
             u"(๑╹ω╹)",
             u"(๑╹ω╹)<通らヘン〒゛"]
        ]
        # ダウトが通った時のセリフ
        self.quoteDouteAccepting = [
            # 僧侶の人
            [u"……やはり私は嘘をつくのが\n苦手なのかもしれませんね……"],
            # ちゃんレナ
            [u"くっ……！！　なぜ分かったの……！！"],
            # 真実ちゃん
            [u"あら……"],
            # ちいちい
            [u"(๑╹ω╹)＜ㄘいㄘいギャーしてまったンカ"]
         ]
    
#----------------------------------------------------------------------------------------------------
# タイトル画面
#----------------------------------------------------------------------------------------------------
class Title(GameObj):
    def __init__(self, g):
        self.gameObj = g
    
    def reset(self):
        self.time = 0
    
    def run(self):
        self.time += 1
            
    def draw(self, painter):
        CX = 10 + 10 * math.cos(self.time / 15)
        CY = 40 + 10 * math.sin(self.time / 20)
        
        OX = 50 + 10 * math.cos(self.time / 25)
        OY = 50 + 10 * math.sin(self.time / 20)
        
        UX = 90 + 10 * math.cos(self.time / 20)
        UY = 40 + 10 * math.sin(self.time / 25)
        
        PX = 130 + 10 * math.cos(self.time / 25)
        PY = 50 + 10 * math.sin(self.time / 30)
        
        # C
        painter.drawImage(CX, CY, Coup.IMG_PATTERN, 3 * Coup.CHIP_SIZE, 0 * Coup.CHIP_SIZE, 2 * Coup.CHIP_SIZE, 2 * Coup.CHIP_SIZE)
        # O
        painter.drawImage(OX, OY, Coup.IMG_PATTERN, 5 * Coup.CHIP_SIZE, 0 * Coup.CHIP_SIZE, 2 * Coup.CHIP_SIZE, 2 * Coup.CHIP_SIZE)
        # U
        painter.drawImage(UX, UY, Coup.IMG_PATTERN, 7 * Coup.CHIP_SIZE, 0 * Coup.CHIP_SIZE, 2 * Coup.CHIP_SIZE, 2 * Coup.CHIP_SIZE)
        # P
        painter.drawImage(PX, PY, Coup.IMG_PATTERN, 9 * Coup.CHIP_SIZE, 0 * Coup.CHIP_SIZE, 2 * Coup.CHIP_SIZE, 2 * Coup.CHIP_SIZE)
    
    def keyPressEvent(self, e):
        self.gameObj.changeScene(self.gameObj.playing)


#----------------------------------------------------------------------------------------------------
# プレイ画面
#----------------------------------------------------------------------------------------------------
class Playing(GameObj) :
    NUM_PLAYER = 5
    CARD_TYPE = ("公爵", "刺客", "大使", "船長", "女伯")
    
    def __init__(self, g):
        self.gameObj = g
    
    def reset(self):
        # プレイヤー
        self.player = [Player("Player", -1), Player("タカツキ", 0), Player("マキハラ", 1), Player("ナガオカ", 2), Player("タカハシ", 3)]
        for i in range(len(self.player)):
            self.player[i].reset()
            # 座標セット
            rad = i * 2 * math.pi / len(self.player)
            self.player[i].posX = 80 + 60 * math.sin(rad)
            self.player[i].posY = 73 + 40 * math.cos(rad)    
        # カード
        self.card = [Card(0, 0), Card(1, 1), Card(2, 2), Card(3, 3), Card(4, 4),
                     Card(5, 0), Card(6, 1), Card(7, 2), Card(8, 3), Card(9, 4),
                     Card(10, 0), Card(11, 1), Card(12, 2), Card(13, 3), Card(14, 4)]
        for i in range(len(self.card)):
            self.card[i].reset()
            # 座標をセット
            self.card[i].posX = 35 + 20 * (i % 5)
            if i < 5:  # 0~4
                self.card[i].posY = 50
            elif i < 10:  # 5~9
                self.card[i].posY = 70
            else:  # 10~14
                self.card[i].posY = 90
            
        # 画面表示用
        self.cursol = 0
        self.explain = None 
        # ゲームの進行状態（ステート）
        self.state = "Intro"
        self.time = 0
    
    def run(self):
        # プレイヤー
        for i in range(len(self.player)):
            self.player[i].run()
        # カード
        for i in range(len(self.card)):
            self.card[i].run()
        
        # カードを配る
        if self.state == "Intro":
            if self.time == 60:
                # カードを伏せる
                for i in range(len(self.card)):
                    self.card[i].animActivate("CLOSE")
            if self.time == 120:
                # カードを配る
                self.dealCards(self.card)
            if self.time == 180:
                # プレイヤーのカード開示
                self.card[0].animActivate("OPEN")
                self.card[5].animActivate("OPEN")
            if self.time == 240:
                # カード移動アニメ処理
                self.state = "SelectCommand"
                self.time = 0
        elif self.state == "SelectCommand":
            pass
        elif self.state == "SelectPlayer":
            self.cursolOfPlayer.run()
        
        self.time += 1
        
    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Escape:
            self.gameObj.sceneTmp = self.gameObj.title
        if self.state == "Intro":
            pass
        elif self.state == "SelectCommand":
            if key == Qt.Key_Z:
            # 決定
                self.selectedCommand = self.cursol
                self.cursol = 1
                self.cursolOfPlayer = CursolOfPlayer()
                self.cursolOfPlayer.reset()
                self.cursolOfPlayer.setPos(self.player[self.cursol].posX, self.player[self.cursol].posY)
                self.state = "SelectPlayer"
            if key == Qt.Key_X:
            # キャンセル
                pass
            elif key == Qt.Key_Right or key == Qt.Key_D:
            # カーソル右移動
                self.cursol += 1
                self.cursol %= 5
            elif key == Qt.Key_Left or key == Qt.Key_G:
            # カーソル左移動
                self.cursol -= 1
                self.cursol %= 5
        elif self.state == "SelectPlayer":
            print(self.cursol)
            if key == Qt.Key_Z:
            # 決定
                pass
            if key == Qt.Key_X:
            # キャンセル
                self.cursol = self.selectedCommand
                self.state = "SelectCommand"
            if key == Qt.Key_Right or key == Qt.Key_D:
            # カーソル右移動
                self.cursol += 1
                if(self.cursol >= 5):
                    self.cursol = 1
                self.cursolOfPlayer.moveTo(10, self.player[self.cursol].posX, self.player[self.cursol].posY)
            if key == Qt.Key_Left or key == Qt.Key_G:
            # カーソル左移動
                self.cursol -= 1
                if(self.cursol < 1):
                    self.cursol = 4
                self.cursolOfPlayer.moveTo(10, self.player[self.cursol].posX, self.player[self.cursol].posY)
            
    def animStart(self, array):
        pass
        
    def draw(self, painter):
        # 円卓
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QColor(192, 168, 0))
        painter.drawEllipse(80 - 60, 72 - 40, 120, 80)
        # プレイヤー
        for i in range(len(self.player)):
            self.player[i].draw(painter)
            # カード
        for i in range(len(self.card)):
            self.card[i].draw(painter)
        
        # カードを配るアニメ
        if self.state == "Intro":
            pass
        # コマンドを選択
        elif self.state == "SelectCommand":
            # 選択枠
            painter.setPen(QColor(240, 0, 0))
            painter.setBrush(QColor(240, 0, 0, 120 + (80 * math.sin(self.time / 20))))
            painter.drawRect(12, 106, 16, 16)
            # 説明文
            if self.cursol == 0:
                command = u"収入"
                self.explain = u"金貨を1つ得る"
            elif self.cursol == 1:
                command = u"援助"
                self.explain = u"金貨を2つ得る"
            elif self.cursol == 2:
                command = u"徴税"
                self.explain = u"金貨を3つ得る"
                painter.drawImage(12, 106, Coup.IMG_PATTERN, 4 * Coup.CHIP_SIZE, 3 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
            elif self.cursol == 3:
                command = u"暗殺"
                self.explain = u"金貨3つと引き換えに、選んだ相手の影響力を1つ失わせる"
                painter.drawImage(12, 106, Coup.IMG_PATTERN, 5 * Coup.CHIP_SIZE, 3 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
            elif self.cursol == 4:
                command = u"交換"
                self.explain = u"自分の影響力1つを山札の人物カードと交換する"
                painter.drawImage(12, 106, Coup.IMG_PATTERN, 6 * Coup.CHIP_SIZE, 3 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
            elif self.cursol == 3:
                command = u"強奪"
                self.explain = u"選んだ相手から金貨を2つ奪う"
                painter.drawImage(12, 106, Coup.IMG_PATTERN, 7 * Coup.CHIP_SIZE, 3 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
            else:
                self.explain = None
            # 説明文の表示
            if self.explain != None:
                painter.setPen(QColor(0, 0, 0))
                painter.drawText(32, 120, command)
                # 枠
                painter.setPen(QColor(0, 0, 0))
                painter.setBrush(QColor(0, 0, 0))
                painter.drawRect(0, 132, 160, 12)
                # メッセージ本体
                strLength = len(self.explain) + 2
                painter.setPen(QColor(240, 240, 240))
                painter.drawText(0 - self.time % (12 * strLength), 142, self.explain)
                painter.drawText((12 * strLength) - self.time % (12 * strLength), 142, self.explain)
        # 強奪などの対象の選択
        elif self.state == "SelectPlayer":
            # 選んだコマンド
            if self.selectedCommand == 0:
                command = u"収入"
            elif self.selectedCommand == 1:
                command = u"援助"
            elif self.selectedCommand == 2:
                command = u"徴税"
                painter.drawImage(12, 106, Coup.IMG_PATTERN, 4 * Coup.CHIP_SIZE, 3 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
            elif self.selectedCommand == 3:
                command = u"暗殺"
                painter.drawImage(12, 106, Coup.IMG_PATTERN, 5 * Coup.CHIP_SIZE, 3 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
            elif self.selectedCommand == 4:
                command = u"交換"
                painter.drawImage(12, 106, Coup.IMG_PATTERN, 6 * Coup.CHIP_SIZE, 3 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
            elif self.selectedCommand == 3:
                command = u"強奪"
                painter.drawImage(12, 106, Coup.IMG_PATTERN, 7 * Coup.CHIP_SIZE, 3 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
            else:
                self.explain = None
            painter.setPen(QColor(0, 0, 0))
            painter.drawText(32, 120, command)
                
            # 選択枠
            self.cursolOfPlayer.draw(painter)
            # 枠
            painter.setPen(QColor(0, 0, 0))
            painter.setBrush(QColor(0, 0, 0))
            painter.drawRect(0, 132, 160, 12)
            # メッセージ本体
            str = u"対象を選んでください"
            strLength = len(str) + 2
            painter.setPen(QColor(240, 240, 240))
            painter.drawText(0 - self.time % (12 * strLength), 142, str)
            painter.drawText((12 * strLength) - self.time % (12 * strLength), 142, str)
            
    #--------------------------------------------------  
    def dealCards(self, array):
        """カードを配る"""
        self.shuffle(array)
        
        # カードをプレイヤーに割付け
        for i in range(len(self.player)):
            # 1枚目のカード
            array[i].moveTo(20, self.player[i].posX - 10, self.player[i].posY)
            # 2枚目のカード
            array[i + len(self.player)].moveTo(20, self.player[i].posX + 10, self.player[i].posY)
            # あまりのカード(中央に配置)
            array[i + 2 * len(self.player)].moveTo(20, 80, 72)
            
            self.player[i].card = [array[i], array[i + len(self.player)]]
        
    def shuffle(self, array):
        """配列をシャッフル"""
        for i in range(len(array)):
            j = random.randint(0, len(array) - 1)
            temp = array[i]
            array[i] = array[j]
            array[j] = temp
        
class Player(GameObj):
    def __init__(self, name, id):
        self.card = [-1, -1]
        self.name = name
        self.faceID = id
        self.posX = 0
        self.posY = 0
        self.emotion = 0

    def reset(self):
        pass
    
    def run(self):
        pass
            
    def draw(self, painter):
        # ポートレート
        painter.drawImage(self.posX - 24, self.posY - 40, Coup.IMG_FACE, self.emotion * Coup.FACE_SIZE, self.faceID * Coup.FACE_SIZE, Coup.FACE_SIZE, Coup.FACE_SIZE)
                    
    def keyPressEvent(self, e):
        pass
    
class CursolOfPlayer(GameObj):
    def __init__(self):
        pass
        
    def reset(self):
        # 移動
        self.moveTime = 0
        self.posX = 0
        self.posY = 0
        self.velX = 0.0
        self.velY = 0.0
        self.toX = 0
        self.toY = 0
        
    def run(self):
        if self.moveTime > 0:
            self.posX += self.velX
            self.posY += self.velY
            self.moveTime -= 1
            if self.moveTime == 0:
                self.posX = self.toX
                self.posY = self.toY
            
    def setPos(self, x, y):
        self.posX = x
        self.posY = y
           
    def moveTo(self, t, x, y):
        self.moveTime = t
        self.toX = x
        self.toY = y
        # 速度計算
        self.velX = (x - self.posX) / t
        self.velY = (y - self.posY) / t
        
    def draw(self, painter):
        painter.drawImage(self.posX - 24, self.posY - 40, Coup.IMG_PATTERN, 0 * Coup.CHIP_SIZE, 6 * Coup.CHIP_SIZE, 48, 48)

class Card(GameObj):
    def __init__(self, id, type):
        self.ID = id
        
        # -1無効,0公爵,1刺客,2大使,3船長,4女伯
        self.TYPE = type
        
    def reset(self):
        self.isOpen = True
        # 移動
        self.moveTime = 0
        self.posX = 0
        self.posY = 0
        self.velX = 0.0
        self.velY = 0.0
        self.toX = 0
        self.toY = 0
        # アニメーション
        self.animName = None
        self.animTime = 0
        
    def run(self):
        if self.moveTime > 0:
            self.posX += self.velX
            self.posY += self.velY
            self.moveTime -= 1
            if self.moveTime == 0:
                self.posX = self.toX
                self.posY = self.toY
            
    def setPos(self, x, y):
        self.posX = x
        self.posY = y
           
    def moveTo(self, t, x, y):
        self.moveTime = t
        self.toX = x
        self.toY = y
        # 速度計算
        self.velX = (x - self.posX) / t
        self.velY = (y - self.posY) / t
        
    def animActivate(self, name):
        self.animName = name
        if self.animName == "OPEN":
            self.animTime = 30
        elif self.animName == "CLOSE":
            self.animTime = 30
    
    def draw(self, painter):
        if self.TYPE >= 0 :
            self.drawAnim(painter)
            
    def drawAnim(self, painter):
        self.animTime -= 1
        if self.animName == None:
            # posの値ははカードの中心
            if self.isOpen:
                painter.drawImage(self.posX - 8, self.posY - 8, Coup.IMG_PATTERN, (4 + self.TYPE) * Coup.CHIP_SIZE, 2 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
                painter.drawImage(self.posX - 8, self.posY - 8, Coup.IMG_PATTERN, (4 + self.TYPE) * Coup.CHIP_SIZE, 3 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
            else:
                painter.drawImage(self.posX - 8, self.posY - 8, Coup.IMG_PATTERN, 4 * Coup.CHIP_SIZE, 4 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)
        if self.animName == "OPEN":
            # 30フレーム / 5枚
            imgPos = 4 - math.floor(self.animTime / 6)
            painter.drawImage(self.posX - 8, self.posY - 8, Coup.IMG_PATTERN, (4 + imgPos) * Coup.CHIP_SIZE, 4 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)    
        elif self.animName == "CLOSE":
            # 30フレーム / 5枚
            imgPos = math.floor(self.animTime / 6)
            painter.drawImage(self.posX - 8, self.posY - 8, Coup.IMG_PATTERN, (4 + imgPos) * Coup.CHIP_SIZE, 4 * Coup.CHIP_SIZE, Coup.CHIP_SIZE, Coup.CHIP_SIZE)    
        # アニメ終了
        if((self.animName != None) & (self.animTime == 0)):
            if self.animName == "OPEN":
                self.isOpen = True 
            elif self.animName == "CLOSE":
                self.isOpen = False
            self.animName = None
        
#--------------------------------------------------
# main
#--------------------------------------------------
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
sys.exit(app.exec_())
