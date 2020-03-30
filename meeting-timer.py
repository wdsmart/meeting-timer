#/usr/bin/env python3


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer

from datetime import datetime, timedelta


class MeetingTimer(QWidget):
    def __init__(self, minutes=30, amber=5, red=2):
        super().__init__()

        # Meeting times
        self.minutes = minutes
        self.amber = amber * 60
        self.red = red * 60

        # Vertical layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Horizontal layout
        self.button_layout = QVBoxLayout()

        # Display
        self.display = QLabel('00:00')
        self.display.setStyleSheet('font: 100pt')

        # Start/stop button
        self.control_button = QPushButton('Start\nMeeting')
        self.control_button.setCheckable(True)
        self.control_button.clicked.connect(self.start_stop_callback)

        # Quit button
        self.quit_button = QPushButton('Quit')
        self.quit_button.clicked.connect(app.exit)

        # Do the layout
        self.layout.addWidget(self.display)
        self.layout.addSpacing(50)
        self.layout.addLayout(self.button_layout)

        # Buttons
        self.button_layout.addWidget(self.control_button)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.quit_button)

        # Set the end time for the timer
        self.reset_callback()

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_callback)

        # Are we running?
        self.running = None

    def start_stop_callback(self, timer_running):
        if timer_running:
            self.control_button.setText('Stop\nMeeting')
            self.running = True
            self.timer_callback()
        else:
            self.control_button.setText('Start\nMeeting')
            self.reset_callback()
            self.running = False

    def reset_callback(self):
        self.end_time = datetime.now() + timedelta(minutes = self.minutes, seconds = 1)
        self.update_display()

    def timer_callback(self):
        self.update_display()

        if self.running:
            self.timer.start(1000)
        else:
            self.timer.stop()

    def update_display(self):
        remaining_time = max(round((self.end_time - datetime.now()).seconds), 0)
        self.display.setText('{0:02}:{1:02}'.format(remaining_time // 60, remaining_time % 60))

        if remaining_time == 0:
            self.running = False
            print('We are done!')
        elif remaining_time <= self.red:
            self.display.setStyleSheet('background-color: red; font: 100pt')
        elif remaining_time <= self.amber:
            self.display.setStyleSheet('background-color: gold; font: 100pt')

if __name__ == '__main__':
    # We need a global application context.  Every GUI will have one of these
    app = QApplication([])

    timer = MeetingTimer()

    timer.show()

    app.exec_()

