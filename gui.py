# -*- coding: utf-8 -*-
"""
    gui.py
"""
from copy import deepcopy
from collections import OrderedDict
from pathlib import Path
import xml.etree.ElementTree as ET
# gui
import tkinter as tk


def __make_reporter(name: str='gui'):
    from logging import Logger, getLogger, Formatter, StreamHandler
    from logging import DEBUG
    handler = StreamHandler()
    formatter = Formatter('%(asctime)s pid:%(process)05d, tid:%(thread)05d - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(DEBUG)
    logger = getLogger(name)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    return logger


LOGGER = __make_reporter()


def create_widget(tree, master):
    controls = OrderedDict()
    widget_names = {"Button": tk.Button, "Entry": tk.Entry, "Frame": tk.Frame,
                    "Label": tk.Label, "LabelFrame": tk.LabelFrame, "Listbox": tk.Listbox,
                    "Menu": tk.Menu, "MenuBar": tk.Menu,
                    "Scale": tk.Scale}
    # 親,子のMAP
    parent_map = {c: p for p in tree.iter() for c in p}
    # フレームだけのコンポーネント
    frames = {}

    import copy
    for root in tree.getroot():
        # Windowを除外するために、ループを分ける。
        for child in root.iter():
            attribute = deepcopy(child.attrib)  # type:dict
            control_name = attribute.pop('id', None)
            # 親を検索する。
            parent = frames.get(parent_map.get(child).tag, master)
            widget = widget_names[child.tag]
            attributes = {key: v for key, v in attribute.items() if not key.startswith("data-")}
            # 画面項目の生成
            w = widget(parent, attributes)
            # data-* 属性を登録
            w.data_attributes = {key: v for key, v in attribute.items() if key.startswith("data-")}
            if child.tag in ["LabelFrame", "Frame", "Menu", "MenuBar"]:
                # フレームを登録
                frames[child.tag] = w
            controls[control_name] = w
    return controls, frames



def open_filedialog():
    pass


def save_filedialog():
    pass

def on_application_exit():
    import sys
    sys.exit(0)

def toggle_changed(sender):
    LOGGER.info(sender)

def create_menubar(controls) -> tk.Menu:
    """
    MenuBarの作成
    :return:
    """
    from functools import partial
    def crate_file_menu(menu) -> tk.Menu:
        """
        ファイルメニュー
        """
        # open
        menu.add_command(label='Open(O)...', under=6, accelerator='Ctrl+O', command=open_filedialog)
        menu.add_command(label='Save(S)...', under=6, accelerator='Ctrl+S', command=save_filedialog)
        menu.add_separator()
        # exit
        menu.add_command(label='Exit', under=0, accelerator='Ctrl+Shift+Q', command=on_application_exit)
        return menu

    def crate_image_menu(menu) -> tk.Menu:
        """
        イメージメニュー
        """
        menu.add_checkbutton(label="Show Original Image...", accelerator='Ctrl+1',
                             command=partial(toggle_changed, sender=1))
        menu.add_checkbutton(label="Show GrayScale Image...", accelerator='Ctrl+2',
                             command=partial(toggle_changed, sender=2))
        return menu

    for menu in [crate_file_menu(controls["File"]), crate_image_menu(controls["Image"])]:
        controls["menu_bar"].add_cascade(menu=menu, label=menu.data_attributes['data-label'])
    return controls["menu_bar"]


def main():
    """
        Entry Point

    """
    xml_file = str(Path(Path(__file__).parent, './MainWindow.xml'))
    LOGGER.info('load file:%s', xml_file)
    tree = ET.parse(xml_file)
    ET.dump(tree)


    frame = tk.Frame(tk.Tk())
    controls, _ = create_widget(tree, frame)
    for c in controls.values():
        if not isinstance(c, tk.Menu):
            c.pack()

    frame.master.configure(menu=create_menubar(controls))
    frame.pack()
    frame.mainloop()


if __name__ == "__main__":
    main()
