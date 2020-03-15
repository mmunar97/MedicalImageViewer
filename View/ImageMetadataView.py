import threading
import tkinter as tk
from tkinter import ttk
from typing import List


class ImageMetadataView(tk.Frame, threading.Thread):

    def __init__(self, root_view: tk.Tk, metadata: List[List[str]], *args, **kwargs):
        threading.Thread.__init__(self)
        tk.Frame.__init__(self, *args, **kwargs)

        self.__root_view = root_view

        columns_labels = ('Index', 'Attribute', 'Value')

        table_view = ttk.Treeview(self.__root_view,
                               columns=columns_labels,
                               show='headings')

        for col in columns_labels:
            table_view.heading(col, text=col)
        table_view.grid(row=1, column=0, columnspan=3)

        for i, (name, score) in enumerate(metadata, start=1):
            table_view.insert("", "end", values=(i, name, score))

        table_view.column("Index", minwidth=100, width=100, stretch=tk.NO)
        table_view.column("Attribute", minwidth=150, width=150, stretch=tk.NO)
        table_view.column("Value", minwidth=400, width=400, stretch=tk.NO)

        table_view.pack(fill=tk.BOTH, expand=1)
        table_view.place(x=0, y=0)
