import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlFile
from pyforms.controls import ControlDir
from pyforms.controls import ControlButton
from pyforms.controls import ControlCheckBoxList
from pyforms.controls import ControlCombo
from pyforms.controls import ControlTextArea
from confapp import conf

from lightdataparser.main import main, __version__

conf += 'lightdataparser.gui.local_settings'


class Gui(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Light data parser')

        self._select_mode = ControlCombo('Input mode', items=[['File', 'file'], ['Directory', 'dir']])
        self._inputs_file = ControlFile('Input file')
        self._inputs_dir = ControlDir('Input Dir')
        self._options = ControlCheckBoxList('Use options:')
        self._output = ControlFile('Output file')
        self._run = ControlButton('Select input file')
        self.out_args = {'recursive_option': False, 'union_option': False, 'advanced_option': False, 'output_file': '',
                         'input_path': ''}

        self.setFixedHeight(260)
        self.setMaximumWidth(500)

        self._options += ('Recursive', False)
        self._options += ('Union', False)
        self._options += ('Advanced', False)

        self._inputs_file.changed_event = self.__input_callback
        self._inputs_dir.changed_event = self.__input_callback
        self._inputs_dir.hide()
        self._inputs_dir.enabled = False

        self._select_mode.activated_event = self.__select_mode_callback
        self._output.changed_event = self.__output_callback
        self._output.use_save_dialog = True
        self._run.value = self.__run_callback
        self._run.enabled = False
        self._formset = [
            '_select_mode', '_inputs_file', '_inputs_dir', '_options', '_output', '_run'
        ]

        self.mainmenu = [
            {
                'About': [
                    {'Help': self.__helpEvent},
                    {'Author': self.__aboutEvent},
                ]
            }
        ]

    def __output_callback(self):
        self.out_args['output_file'] = self._output.value

    def __input_callback(self):
        path = self._inputs_dir.value if self._inputs_dir.enabled else self._inputs_file.value
        self.out_args['input_path'] = [path] if path else []
        self._run.label = "Run"
        self._run.enabled = True

    def __select_mode_callback(self, index):
        if self._select_mode.value == "file":
            self._inputs_dir.enabled = False
            self._inputs_dir.hide()
            self._inputs_file.show()
        else:
            self._inputs_dir.enabled = True
            self._inputs_dir.show()
            self._inputs_file.hide()

    def __run_callback(self):
        self._run.enabled = False
        if not self.out_args['input_path']:
            self._run.label = "Select input file before run"
            return
        self._run.label = "Processing"
        for opt in self._options.value:
            if opt is 'Recursive':
                self.out_args['recursive_option'] = True
            elif opt is 'Union':
                self.out_args['union_option'] = True
            elif opt is 'Advanced':
                self.out_args['advanced_option'] = True
        output, status = main(True, self.out_args)
        if status:
            self._run.enabled = True
            self._run.label = "Saved in: {}".format(output)
        else:
            self._run.label = "Process failed"

    def __aboutEvent(self):
        aboutmsg = """
        Author: Vladislav Khutorskoy
        Program version {}
        Github page: {}
        """.format(__version__, "https://github.com/XENKing/lightdataparser")
        self.info(aboutmsg, "About dialog")

    def __helpEvent(self):
        helpmsg = """
        Sorts and saves your files in a convenient format for you.
        Input file/dir - Path to the file or directory to merge
        Output file - Path to the file in which the processed data will be saved
        Avalible options:
        Recursive - Recursive search of files in subfolders at the specified path
        Union - Use union instead of default intersection
        Advanced - Use parse files on advanced conditions
        """
        self.about(helpmsg, "Help dialog")


def start_gui():
    app = pyforms.start_app(Gui, geometry=(320, 260, 320, 260))
