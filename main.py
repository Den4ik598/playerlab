from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl, QTime
from qt_material import apply_stylesheet
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QAction, QComboBox
from PyQt5.QtGui import QIcon, QMouseEvent, QPixmap
import sys, os
 
# Класс MainWindow для видеоплеера
class Videoplayer(QMainWindow):
    def __init__(self, parent=None):
        super(Videoplayer, self).__init__(parent)
 
        # Установка размеров окна и иконки
        self.setMinimumSize(800, 600)
        self.windowStateBeforeFullScreen = None
        self.setWindowIcon(QIcon('icons/app.png'))
 
        # Создание плеера и виджета видео
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        videoWidget.setMouseTracking(True)
        videoarea = QWidget(self)
        self.setCentralWidget(videoarea)
 
        # Создание кнопок и элементов управления
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pausebutton=QPushButton()
        self.pausebutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pausebutton.setEnabled(False)
        self.spaceAction = QAction(QIcon('icons/play_arrow.png'), 'Воспроизвести/Пауза', self)
        self.spaceAction.setShortcut('Space')
        self.spaceAction.triggered.connect(self.togglePlayPause)
        self.stopbutton=QPushButton()
        self.stopbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopbutton.setEnabled(False)
        self.stopbutton.clicked.connect(self.stop)
        self.currentTimeLabel = QLabel()
        self.currentTimeLabel.setVisible(False)
        self.timeSeparatorLabel = QLabel("/")
        self.timeSeparatorLabel.setVisible(False)
        self.totalTimeLabel = QLabel()
        self.totalTimeLabel.setVisible(False)
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setEnabled(False)
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeImageLabel = QLabel()
        self.updateVolumeImage()
        self.volumeSlider.valueChanged.connect(self.setVolume)
        self.volumeSlider.valueChanged.connect(self.updateVolume)
        self.volumeSlider.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.fullscreenButton = QPushButton()
        self.fullscreenButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.fullscreenButton.clicked.connect(self.toggleFullScreen)
        self.fullscreenAction = QAction(QIcon('icons/fullscreen.png'), 'Во весь экран', self)
        self.fullscreenAction.setShortcut('F')
        self.fullscreenAction.triggered.connect(self.toggleFullScreen)
        self.speedComboBox = QComboBox()
        self.speedComboBox.addItems(["0.25x", "0.5x", "0.75x", "1x", "1.25x", "1.5x", "1.75x", "2x"])
        self.speedComboBox.currentIndexChanged.connect(self.changePlaybackSpeed)
        self.speedComboBox.setCurrentIndex(3)
        self.backwardButton = QPushButton()
        self.backwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.backwardButton.setEnabled(False)
        self.backwardButton.clicked.connect(self.backward)
        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forwardButton.setEnabled(False)
        self.forwardButton.clicked.connect(self.forward)
        self.screenshotButton = QPushButton()
        self.screenshotButton.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.screenshotButton.setEnabled(False)
        self.screenshotButton.clicked.connect(self.createScreenshot)
        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
 
        # создание "горячих" клавиш 
        openAction = QAction(QIcon('icons/open_file.png'), 'Открыть файл', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.openfile)
        exitAction = QAction(QIcon('icons/exit_app.png'), 'Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.exit)
        stopAction=QAction(QIcon('icons/stop.png'), 'Стоп', self)
        stopAction.setShortcut('S')
        stopAction.triggered.connect(self.stop)
        toggleMuteAction = QAction(QIcon('icons/tooglemute.png'), 'Включить/Отключить звук', self)
        toggleMuteAction.setShortcut('M')
        toggleMuteAction.triggered.connect(self.toggleMute)
        increaseVolumeAction = QAction(QIcon('icons/volume_up.png'), 'Увеличить громкость', self)
        increaseVolumeAction.setShortcut(Qt.Key_Up)
        increaseVolumeAction.triggered.connect(self.increaseVolume)
        decreaseVolumeAction = QAction(QIcon('icons/volume_down.png'), 'Уменьшить громкость', self)
        decreaseVolumeAction.setShortcut(Qt.Key_Down)
        decreaseVolumeAction.triggered.connect(self.decreaseVolume)
        backwardAction = QAction(QIcon('icons/backward.png'), 'Назад', self)
        backwardAction.setShortcut('Left')
        backwardAction.triggered.connect(self.backward)
        forwardAction = QAction(QIcon('icons/forward.png'), 'Вперед', self)
        forwardAction.setShortcut('Right')
        forwardAction.triggered.connect(self.forward)
 
        #создание верхнего меню - бара 
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('Медиа')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        Editmenu=menuBar.addMenu('Воспроизведение')
        Editmenu.addAction(self.spaceAction)
        Editmenu.addAction(stopAction)
        Editmenu.addAction(backwardAction)
        Editmenu.addAction(forwardAction)
        Audiomenu=menuBar.addMenu('Аудио')
        Audiomenu.addAction(toggleMuteAction)
        Audiomenu.addAction(increaseVolumeAction)
        Audiomenu.addAction(decreaseVolumeAction)
        VideoMenu=menuBar.addMenu('Видео')
        VideoMenu.addAction(self.fullscreenAction)
 
        #подключение кнопок и других графических элементов
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.stopbutton)
        controlLayout.addWidget(self.pausebutton)
        controlLayout.addWidget(self.currentTimeLabel)
        controlLayout.addWidget(self.timeSeparatorLabel)
        controlLayout.addWidget(self.totalTimeLabel)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.volumeImageLabel)
        controlLayout.addWidget(self.volumeSlider)
        controlLayout.addWidget(self.fullscreenButton)
        controlLayout.addWidget(self.speedComboBox)
        controlLayout.addWidget(self.backwardButton)
        controlLayout.addWidget(self.forwardButton)
        controlLayout.addWidget(self.screenshotButton)
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
        videoarea.setLayout(layout)
 
        # Подключение сигналов к слотам для обработки событий
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.detectionError)
 
    def openfile(self):
        # Открытие файла и настройка видеоплеера
        fileName, _ = QFileDialog.getOpenFileName(self, "Выберите видеофайл",  "", "Все файлы (*);;Видеофайл (*.mp4 *.avi *.wmv *.mov *.mkv *.3gp, *flv, *ogv, *webm ,*.mp3 *.wav *.ogg *.flac)")
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromUserInput(fileName)))
            self.playButton.setEnabled(True)
            self.stopbutton.setEnabled(True)
            self.pausebutton.setEnabled(True)
            self.screenshotButton.setEnabled(True)
            self.positionSlider.setEnabled(True)
            self.currentTimeLabel.setVisible(True)
            self.timeSeparatorLabel.setVisible(True)
            self.totalTimeLabel.setVisible(True)
            file_name = os.path.basename(fileName)
            file_name_without_ext = os.path.splitext(file_name)[0]
            self.setWindowTitle(f"Видеоплеер - {file_name_without_ext}")
            self.errorLabel.clear()
        else:
            self.detectionError()
 
    def exit(self):
        # Завершение приложения
        sys.exit(app.exec_())
 
    def play(self):
        # Воспроизведение или пауза видео
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
           self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def pause(self):
        # Пауза видео
        self.mediaPlayer.pause()
 
    def togglePlayPause(self): 
        #Кнопка пауза и воспроизвести
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def stop(self):
        # Остановка видео
        self.mediaPlayer.stop()
 
    def mediaStateChanged(self, state):
        # Обработка изменения состояния видеоплеера (воспроизведение, пауза и др.)
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.pausebutton.setEnabled(True)
            self.backwardButton.setEnabled(True)
            self.forwardButton.setEnabled(True)
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.pausebutton.setEnabled(True)
            self.backwardButton.setEnabled(True)
            self.forwardButton.setEnabled(True)
 
        playbackRate = self.mediaPlayer.playbackRate()
        speedText = f"{playbackRate}x"
        index = self.speedComboBox.findText(speedText)
        if index != -1:
            self.speedComboBox.setCurrentIndex(index)
 
    def positionChanged(self, position):
        # Обработка изменения позиции воспроизведения
        self.positionSlider.setValue(position)
        self.currentTimeLabel.setText(self.formatTime(position))
 
    def durationChanged(self, duration):
        # Обработка изменения продолжительности видео
        self.positionSlider.setRange(0, duration)
        self.totalTimeLabel.setText(self.formatTime(duration))
 
    def formatTime(self, milliseconds):
        # Форматирование времени в удобный для отображения вид
        duration = QTime(0, 0, 0, 0).addMSecs(milliseconds)
        return duration.toString('hh:mm:ss')
 
    def setPosition(self, position):
        # Установка позиции воспроизведения
        self.mediaPlayer.setPosition(position)
 
    def unmute(self):
        # Включение звука
        self.mediaPlayer.setMuted(False)
        if self.volumeSlider.value() == 0:
            self.volumeSlider.setValue(self.previousVolume)
        self.updateVolumeImage()
 
    def mute(self):
        # Отключение звука
        self.mediaPlayer.setMuted(True)
        self.previousVolume = self.volumeSlider.value()
        self.volumeSlider.setValue(0)
        self.updateVolumeImage()
 
    def toggleMute(self):
        # Переключение звука
        if self.mediaPlayer.isMuted():
            self.mediaPlayer.setMuted(False)
            if self.volumeSlider.value() == 0:
                self.volumeSlider.setValue(self.previousVolume)
            self.updateVolumeImage()
        else:
            self.mediaPlayer.setMuted(True)
            self.previousVolume = self.volumeSlider.value()
            self.volumeSlider.setValue(0)
            self.updateVolumeImage()
 
    def setVolume(self, volume):
        # установка громкости 
        self.mediaPlayer.setVolume(volume)
 
    def updateVolume(self):
        # обновление громкости
        volume = self.volumeSlider.value()
        if volume == 0:
            self.mediaPlayer.setMuted(True)
        else:
            self.mediaPlayer.setMuted(False)
            self.mediaPlayer.setVolume(volume)
        self.updateVolumeImage()
 
    def updateVolumeImage(self):
        # обновление громкости звука в видео, которое вы запустили 
        volume = self.volumeSlider.value()
        if volume == 0:
            image = QPixmap('icons/volume_off.png').scaled(35, 35)
        elif volume <= 50:
            image = QPixmap('icons/volume_down.png').scaled(35, 35)
        else:
            image = QPixmap('icons/volume_up.png').scaled(35, 35)
        self.volumeImageLabel.setPixmap(image)
 
    def increaseVolume(self):
        #увеличение громкости 
        volume = self.volumeSlider.value()
        if volume < 100:
            volume += 5
            self.volumeSlider.setValue(volume)
 
    def decreaseVolume(self):
        # Уменьшение громкости
        volume = self.volumeSlider.value()
        if volume > 0:
            volume -= 5
            self.volumeSlider.setValue(volume)
 
    def toggleFullScreen(self):
        # Переключение в полноэкранный режим
        if self.isFullScreen():
            self.showNormal()
            if self.windowStateBeforeFullScreen is not None:
                self.setWindowState(self.windowStateBeforeFullScreen)
            self.windowStateBeforeFullScreen = None
        else:
            self.windowStateBeforeFullScreen = self.windowState()
            self.showFullScreen()
 
    def keyPressEvent(self, event):
        # Обработка нажатий клавиш
        if event.key() == Qt.Key_F:
            self.toggleFullScreen()
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.toggleFullScreen()
        elif event.key() == Qt.Key_Left:
            self.backward()
        elif event.key() == Qt.Key_Right:
            self.forward()
        elif event.key() == Qt.Key_Shift:
            self.createScreenshot()
        else:
            super().keyPressEvent(event)
 
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        # Обработка двойного щелчка мыши
        if event.button() == Qt.LeftButton:
            self.toggleFullScreen()
        else:
            super().mouseDoubleClickEvent(event)
 
    def changePlaybackSpeed(self):
        # Изменение скорости воспроизведения
        speedText = self.speedComboBox.currentText()
        speed = float(speedText[:-1])
        self.mediaPlayer.setPlaybackRate(speed)
 
    def backward(self):
        # Вернуться назад в видео
        position = self.mediaPlayer.position()
        self.mediaPlayer.setPosition(position - 10000)
 
    def forward(self):
        # Перейти вперед в видео
        position = self.mediaPlayer.position()
        duration = self.mediaPlayer.duration()
        new_position = position + 10000
        if new_position > duration:
            new_position = duration
        self.mediaPlayer.setPosition(new_position)
 
    def detectionError(self):
        # Обработка ошибки воспроизведения
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Ошибка: " + self.mediaPlayer.errorString())
 
    def wheelEvent(self, event):
        # обработка колесика мыши для регулировки громкости 
        volume = self.volumeSlider.value()
        if event.angleDelta().y() > 0:
            # увеличение громкости
            if volume < 100:
                volume += 5
                self.volumeSlider.setValue(volume)
        else:
            # уменьшение громкости
            if volume > 0:
                volume -= 5
                self.volumeSlider.setValue(volume)
 
    def createScreenshot(self):
    # Создание скриншота из видео
        fileName, _ = QFileDialog.getSaveFileName(self, "Выберите файл для сохранения скриншота", "", "Изображение (*.png)")
        if fileName:
            videoWidget = self.mediaPlayer.videoOutput()
            pixmap = QPixmap(videoWidget.size())
            painter = QPainter(pixmap)
            videoWidget.render(painter)
            painter.end()
            pixmap.save(fileName, "png")
 
if __name__ == '__main__':
    # Создание и запуск приложения
    app = QApplication(sys.argv)
    app.setApplicationName("Видеоплеер")
    apply_stylesheet(app, theme='light_teal.xml')
    player = Videoplayer()
    player.show()
    sys.exit(app.exec_())