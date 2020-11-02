from PyQt5.QtWidgets import QMessageBox


def spawnDialogWindow(title, text, subtext="" , type="Information"):
    message = QMessageBox()
    if type == "Question":
        message.setIcon(QMessageBox.Question)
    elif type == "Warning":
        message.setIcon(QMessageBox.Warning)
    elif type == "Critical":
        message.setIcon(QMessageBox.Critical)
    else:
        message.setIcon(QMessageBox.Information)
    message.setWindowTitle(title)
    message.setText(text)
    message.setInformativeText(subtext)
    message.setStandardButtons(QMessageBox.Ok)
    message.exec_()
