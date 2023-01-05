import datetime
import shutil
import posixpath
import json
import os
from subprocess import call
from ui.packaging_toolUI import Ui_MainWindow
from PySide2.QtCore import QTimer, QRunnable, Slot, Signal, QObject, QThreadPool
import traceback
import sys

from PySide2 import QtCore, QtGui, QtWidgets

import run_integrity_checker
from collections import defaultdict

from config import PROJECTS, SERVER_PATH



class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)




class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done






class image_packaging(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        """
        Class Initialize
        :param parent: build_image_metadata
        """
        super(image_packaging, self).__init__()
        self.setupUi(self)
        self.ui_object_switch()
        self.connect_ui()
        self.log_text = ""
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def connect_ui(self):
        """
        Signal and slotting
        :return:
        """
        self.input_dir_browse_pushButton.clicked.connect(self.browse_input_directory)
        self.output_dir_browse_pushButton.clicked.connect(self.browse_output_directory)
        self.cancel_pushButton.clicked.connect(self.close)
        self.remove_dir_pushButton.clicked.connect(self.remove_input_dir_list)
        self.comboBox.currentIndexChanged.connect(self.populate_outdirdata)
        self.validate_pushButton.clicked.connect(self.execute_process)
        self.create_pushButton.clicked.connect(self.startThread)
        self.populate_projects()
        self.ui_object_switch()
        self.ui_edit_text()


    def ui_edit_text(self, input_msg='Source Directory', output_msg='Destination Directory'):
        """
        UI Object for set text
        :param input_msg:
        :param output_msg:
        :return:
        """
        self.input_dir_path.clear()
        self.output_dir_path.clear()
        # self.input_dir_lineEdit.setText(input_msg)
        # self.output_dir_lineEdit.clear()
        # self.output_dir_lineEdit.setText(output_msg)
        self.dir_treeWidget.clear()
        # self.dir_treeWidget.addItem('Multiple Directory Inputs')

    def ui_object_switch(self, input_dir=1, rem_dir=0, dir_tree_widget=0, log_text=1,
                          validate_button=0,package_button=0, progress_bar=1, combo=0, show_combo=0, cancel_button=1):
        """
        UI object for enable/disable
        :param input_dir:
        :param rem_dir:
        :param dir_tree_widget:
        :param log_text:
        :param output_dir:
        :param out_button:
        :param progress_bar:
        :param exe_button:
        :param cancel_button:
        :return:
        """
        self.input_dir_path.setEnabled(input_dir)
        self.output_dir_path.setEnabled(input_dir)
        self.remove_dir_pushButton.setEnabled(rem_dir)
        self.dir_treeWidget.setEnabled(dir_tree_widget)
        self.log_textEdit.setEnabled(log_text)
        self.comboBox.setEnabled(combo)
        self.show_combo.setEnabled(show_combo)

        self.validate_pushButton.setEnabled(validate_button)
        self.create_pushButton.setEnabled(package_button)

        self.image_progressBar.setEnabled(progress_bar)
        self.cancel_pushButton.setEnabled(cancel_button)


    def browse_input_directory(self):
        """
        browse the input directory
        :return:
        """
        source_directory = QtWidgets.QFileDialog.\
            getOpenFileName(self, "Open file", "{}".format(os.path.dirname(__file__)))
        if source_directory:

            self.input_dir_path.setText(str(source_directory[0]))

            self.ui_object_switch(rem_dir=1, dir_tree_widget=1,
                                  log_text=1)

        else:
            self.input_dir_lineEdit.setText('None')



    def populate_projects(self):
        for i in PROJECTS.keys():
            self.show_combo.addItem(i)


    def populate_outdirdata(self):
        self.ui_object_switch(validate_button=1, cancel_button=1, dir_tree_widget=1, combo= 1)
        # self.packagefolder = self.destpackagelineEdit.text() if self.destpackagelineEdit.text() else str(datetime.datetime.today().date())

        self.outdir_path = f'{SERVER_PATH}/{str(self.comboBox.currentText())}/{str(datetime.datetime.today().year)}/{str(self.show_combo.currentText())}/Output/{str(datetime.datetime.today().month).capitalize()}/{str(datetime.datetime.today().date()).replace("-", "")}'

        # self.destpackagelineEdit.setPlaceholderText(self.packagefolder)

        self.log_textEdit.insertPlainText('click on validate button to validate the package')


    def nested_dict(self):
        """
        Creates a default dictionary where each value is an other default dictionary.
        """
        return defaultdict(self.nested_dict)

    def default_to_regular(self, d):
        """
        Converts defaultdicts of defaultdicts to dict of dicts.
        """
        if isinstance(d, defaultdict):
            d = {k: self.default_to_regular(v) for k, v in d.items()}
        return d

    def get_path_dict(self, paths):
        new_path_dict = self.nested_dict()
        for path in paths:

            parts = path.split('\\')
            if parts:
                marcher = new_path_dict
                for key in parts[:-1]:
                    marcher = marcher[key]
                marcher[parts[-1]] = parts[-1]
        return self.default_to_regular(new_path_dict)

    def add_input_dir_list(self,source_directory):
        """
        Adding the input directory folder to list
        :return:
        """
        l1 = []
        for s, d, files in os.walk(source_directory):
            for i in files:

                l1.append(os.path.join(s, i).replace(source_directory, ''))

        result = self.get_path_dict(l1)


        if str(self.input_dir_path.text()) == 'None':
            return
        else:

            self.dir_treeWidget.clear()


            for i, value in result[''].items():

                parent = QtWidgets.QTreeWidgetItem(self.dir_treeWidget)
                parent.setText(0, i)

                parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

                for i, j in value.items():
                    child = QtWidgets.QTreeWidgetItem(parent)
                    child.setText(0, i)

            # self.dir_treeWidget.expandToDepth(0)


    def remove_input_dir_list(self):
        """
        Remove selected items from list
        :return:
        """
        self.dir_treeWidget.clear()
        self.input_dir_path.clear()
        self.output_dir_path.clear()

        self.ui_object_switch(rem_dir=0, dir_tree_widget=0, log_text=1,
                              validate_button=0, show_combo=0 )


    def browse_output_directory(self):
        """
        Get the Output folder
        :return:
        """
        out_directory = QtWidgets.QFileDialog.\
            getExistingDirectory(self, "Choose Folder", "{}".format(os.path.dirname(__file__)))
        if out_directory:
            self.output_dir_path.setText(out_directory)
            self.ui_object_switch(dir_tree_widget=1, rem_dir=1,
                                  log_text=1, show_combo=1, combo= 1)
        else:
            self.output_dir_lineEdit.setText('None')
            self.ui_object_switch(dir_tree_widget=1, rem_dir=1,
                                  log_text=1, show_combo=1, combo= 1)

        self.add_input_dir_list(out_directory)


    def dump_json_data(self, json_dict):
        """
        Creating Jason Object
        :param json_dict: dictionary
        :return:
        """
        json_file_path = posixpath.join(str(self.output_dir_lineEdit.text()), "json_manifest.json")
        if os.path.exists(json_file_path):
            try:
                load_fp = open(json_file_path, 'r')
                data = json.load(load_fp)
            except:
                self.log_text += "\n\tJSON Load Error...{}\n".format(json_file_path)
            load_fp.close()
        else:
            data = dict()
        data.update(json_dict)
        with open(json_file_path, 'w') as dump_fp:
            try:
                json.dump(data, dump_fp, indent=4)
            except:
                self.log_text += "\n\tJSON write Error...{}\n".format(json_file_path)

    def progress_fn(self, n):
        self.image_progressBar.setValue(n)

    def print_output(self, s):
        print(">>>>>>>>",s)

    def thread_complete(self):
        self.message_box("\t\tPackage has been created at destination\t\t", "Done")
        print("THREAD COMPLETE!")

    def startThread(self):

        worker = Worker(self.create_package, self.list, self.input_dir, self.out_dir)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    def execute_process(self):
        """
        :return:
        """

        self.log_textEdit.clear()

        self.input_dir = os.path.basename(str(self.input_dir_path.text())).split('.')[0]
        self.out_dir = str(self.output_dir_path.text())
        self.packagefolder= datetime.datetime.now().month
        self.destination_path = os.path.join(self.out_dir, str(self.packagefolder))
        department_type = str(self.comboBox.currentText())
        self.show = str(self.show_combo.currentText())
        # self.show = 'cool'
        # self.input_dir = r'fear_100_081_270_retime_exr_v002'
        # self.out_dir = r'C:/Repo/nuke_glb/com_packaging_tool/ROTO/Cool_Client/Output/fear_100_081_270_roto_output_v001'
        # department_type = 'roto'
        # self.destination_path =' not yet desided'

        if not os.path.exists(self.out_dir):
            self.message_box("Invalid Input Path", "Error!")
            self.log_text += "\n\tInvalid Path--->{}\n"


        status = run_integrity_checker.main(self.input_dir,self.out_dir,self.destination_path, department_type, self.show)

        self.list = status[0][1]

        if True in status[0]:

            self.log_text = ''
            for i in status[0][1]:
                self.log_text += i

            self.log_textEdit.setTextColor(QtGui.QColor(255,0,0))
            self.log_textEdit.insertPlainText(self.log_text)
            return
        else:
            self.log_text = ''

            for i in status[0][2]:
                self.log_text += i+"\n"

            self.log_textEdit.setTextColor(QtGui.QColor(0, 204, 0))
            self.log_textEdit.insertPlainText(self.log_text)
            self.log_textEdit.setTextColor(QtGui.QColor(255, 0, 255))
            self.log_textEdit.insertPlainText('\n\n\nSanity check has been done \nNo errors found. \n\n')#Click on "Publish" button to publish the package to Server.\n\n\n'
            self.ui_object_switch(dir_tree_widget=1, rem_dir=1, log_text=1, validate_button=1, package_button = 0)



    def create_package(self, list, input,out_dir,progress_callback):

        all_paths = {}
        for each in list:
            each = os.path.dirname(each) if '%04d' in each else each
            all_paths.update({each:each.replace(os.path.dirname(input), out_dir)})

        total_count = 0

        for src, dst in all_paths.items():

            if not os.path.exists(os.path.dirname(dst)):
                self.log_text += "\nMaking Directories{}\n".format(os.path.dirname(dst))
                try:
                    os.makedirs(os.path.dirname(dst))
                except:
                    self.log_text += "\n\tUnable to Create Directories--->{}\n".format(os.path.dirname(dst))
            if os.path.isdir(src):
                call(['robocopy', src, dst, "/S", "/MIR"])
            else:
                shutil.copyfile(src, dst)
            self.log_text += "\nCopying Files...{}\n".format(src)
            total_count += (100/len(all_paths))

            progress_callback.emit(total_count)

            self.log_textEdit.insertPlainText(src+"\n")
        self.log_textEdit.insertPlainText('\n\n\t{}\n'.format(self.out_dir))
        self.log_textEdit.insertPlainText("\n\n\tCopied Files successfully...\n")
        return list


    def message_box(self, msg, title):
        """
        Display Message window
        :param msg:
        :param title:
        :return:
        """
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(msg)
        msgBox.setWindowTitle(title)
        msgBox.exec_()


def main():
    """
    Calling Main Object
    :return:
    """
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = image_packaging()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()