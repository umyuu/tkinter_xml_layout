# -*- coding: utf-8 -*-
"""
    AdaptiveThreshold Simulator
"""
from copy import deepcopy
import xml.etree.ElementTree as ET

# gui
import tkinter as tk


def main():
    """
        Entry Point

    """
    root = tk.Tk()
    frame = tk.Frame(root)
    tree = ET.parse('MainWindow.xml')
    widget_names = {"Scale": tk.Scale}
    controls = {}  # type:dict
    for child in tree.getroot():
        attribute = deepcopy(child.attrib)  # type:dict
        control_name = attribute.pop('name')
        widget = widget_names[child.tag]
        controls[control_name] = widget(frame, attribute)

    for child in frame.children.values():
        child.pack()

    frame.pack()
    frame.mainloop()


if __name__ == "__main__":
    main()
