import sys
import pathlib
import subprocess
import json

# main_ui.py file is generated from main.ui. main.ui can be edited in QtCreator
# In order to convert main.ui to main_ui.py, you can use this command:
# pyuic5 main.ui -o main_ui.py -i 4
try:
    import main_ui
except ImportError:
    from . import main_ui

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialogButtonBox
from PyQt5 import QtGui
import psutil



class FetchCordMainUI(QMainWindow, main_ui.Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(FetchCordMainUI, self).__init__(*args, **kwargs)

        self.fetchcord_process = None
        script_dir = pathlib.Path(__file__).parent

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(str(script_dir / "FetchDis.png")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.setWindowIcon(icon)

        self.setupUi(self)

        self.buttonBox.button(QDialogButtonBox.Ok).setText("Start")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Stop")

        with open(script_dir.parent / "resources/fetchcord_ids.json") as f:
            terminals = list(json.load(f)["terminal"].keys())
        for term in terminals:
            self.terminalName.addItem(term)

        self.installSystemd.clicked.connect(self._install_systemd)
        self.uninstallSystemd.clicked.connect(self._uninstall_systemd)
        self.enableSystemd.clicked.connect(self._enable_systemd)
        self.disableSystemd.clicked.connect(self._disable_systemd)
        self.startSystemd.clicked.connect(self._start_systemd)
        self.stopSystemd.clicked.connect(self._stop_systemd)
        self.update.clicked.connect(self._update_database)

        self.detect_running_fetchcord_processes()

    def detect_running_fetchcord_processes(self):

        for proc in psutil.process_iter():
            if "fetchcord" in proc.name() and "--gui" not in proc.cmdline():
                self.fetchcord_process = proc

        if self.fetchcord_process is not None:
            print(f'FetchCord Process ID: {self.fetchcord_process.pid}')
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def collect_arguments(self):
        args = {}

        if not self.distroInfo.isChecked():
            args["--nodistro"] = ""

        if not self.hardwareInfo.isChecked():
            args["--nohardware"] = ""

        if not self.shellInfo.isChecked():
            args["--noshell"] = ""

        if not self.hostInfo.isChecked():
            args["--nohost"] = ""

        if self.disableNeofetchConfig.isChecked():
            args["--noconfig"] = ""

        if "GiB" in str(self.memoryUnits.currentText()):
            args["--memtype"] = "gb"
        else:
            args["--memtype"] = "mb"

        if self.terminalName.currentText() != "Terminal Name":
            args["--terminal"] = self.terminalName.currentText()

        if self.terminalFont.text():
            args["--termfont"] = self.terminalFont.text()

        args["--time"] = str(self.cycleTime.value())

        if self.pauseCycle.value():
            args["--pause-cycle"] = str(self.pauseCycle.value())

        args["--poll-rate"] = str(self.pollRate.value())

        return args

    def flatten(self, iterable):
        if isinstance(iterable, (list, tuple, set, range)):
            for sub in iterable:
                yield from self.flatten(sub)
        else:
            yield iterable

    def accept(self):
        args = self.collect_arguments()
        self.run_fetchcord(args, disable_start_button=True)

    def reject(self):
        if self.fetchcord_process is not None:
            self.fetchcord_process.terminate()
            self.fetchcord_process = None
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def _install_systemd(self):
        self.run_fetchcord({"--install": ""})

    def _uninstall_systemd(self):
        self.run_fetchcord({"--uninstall": ""})

    def _enable_systemd(self):
        self.run_fetchcord({"--enable": ""})

    def _disable_systemd(self):
        self.run_fetchcord({"--disable": ""})

    def _start_systemd(self):
        self.run_fetchcord({"--start": ""})

    def _stop_systemd(self):
        self.run_fetchcord({"--stop": ""})

    def _update_database(self):
        args = {"--update": ""}
        if self.testingBranch.isChecked():
            args["--testing"] = ""
        self.run_fetchcord(args)

    def run_fetchcord(self, args: dict, disable_start_button: bool = False):
        process_call_args = ["fetchcord"] + list(self.flatten(list(args.items())))
        process_call_args = list(filter(None, process_call_args))
        print(f"DEBUG: {subprocess.list2cmdline(process_call_args)}")
        self.fetchcord_process = subprocess.Popen(process_call_args)
        if disable_start_button:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)


def main():
    app = QApplication(sys.argv)
    window = FetchCordMainUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
