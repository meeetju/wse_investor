import logging
from _best_companies import get
from tkinter import *
from threading import *


logger = logging.getLogger()


class StdoutDirector:

    def __init__(self, text_area):
        self.text_area = text_area

    def write(self, msg):
        self.text_area.insert(END, msg)
        self.text_area.yview(END)

    def flush(self):
        pass


class Gui:

    def __init__(self):
        self._root = Tk()
        self._frame = Frame(self._root)
        self._main_menu = Menu(self._frame)
        self._configure_window()
        self._configure_main_menu()
        self._configure_listbox()

    def _configure_window(self):
        self._root.title("WSE Investor")
        self._root.geometry("1000x600")
        self._root.config(menu=self._main_menu)
        self._frame.pack()

    def _configure_listbox(self):
        self._scroll_y_axis = Scrollbar(self._frame)
        self._scroll_y_axis.pack(side=RIGHT, fill=Y)
        self._text = Text(self._frame, undo=True, height=35, width=165, yscrollcommand=self._scroll_y_axis.set)
        self._text.pack(expand=True, fill=BOTH)
        self._scroll_y_axis.config(command=self._text.yview, )

    def _configure_main_menu(self):
        self._main_menu.add_command(label="Start", command=self._start)
        self._main_menu.add_command(label="Exit", command=self._exit)

    def run(self):
        self._root.mainloop()

    def _start(self):
        _thread_get_companies = Thread(target=self._get_companies_process, daemon=True)
        sys.stdout = StdoutDirector(self._text)
        _text_widget_handler = logging.StreamHandler(stream=sys.stdout)
        logger.addHandler(_text_widget_handler)
        _thread_get_companies.start()

    def _exit(self):
        self._root.destroy()

    @staticmethod
    def _get_companies_process():
        get()


gui = Gui()
gui.run()
