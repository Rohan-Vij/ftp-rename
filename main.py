"""Tkinter GUI for the main program."""

import tkinter as tk
from tkinter import ttk, messagebox
from enum import Enum

import ftputil

from utils.ftp_utils import get_files, search_names
from utils.load_configs import load_file
from utils.str_utils import parse_file_name, rewrite_file_name


class Variables(Enum):
    # pylint: disable-msg=C0103
    """Variables for the GUI."""

    _config = load_file("config.yaml")

    CATEGORIES = _config["CATEGORIES"]
    IMAGE_PATTERNS = _config["PATTERNS"]["IMAGES"]

    _ftp_config = load_file("ftp_config.yaml")

    HOST = _ftp_config["FTP"]["HOST"]
    PORT = _ftp_config["FTP"]["PORT"]
    USER = _ftp_config["FTP"]["USER"]
    PASSWORD = _ftp_config["FTP"]["PASSWORD"]


class FTP:
    """FTP connection."""
    # pylint: disable-msg=R0903
    # --- FTP connection ---
    def __init__(self):
        self.host = self._connect()

    def _connect(self):
        """Connect to the FTP server."""
        host = ftputil.FTPHost(Variables.HOST.value, Variables.USER.value,
                               Variables.PASSWORD.value)
        return host

    def close(self):
        """Close the FTP connection."""
        self.host.close()


class RenameFrame(ttk.Frame):
    # pylint: disable-msg=R0901
    # pylint: disable-msg=R0902
    # pylint: disable-msg=R0914
    """Rename frame of Tkinter GUI"""

    def __init__(self, container):
        super().__init__(container)

        self.padding = {"padx": 15, "pady": 5}

        self.options = {"font": ("Tahoma", 12)}

        # -- configuring grid ---
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.window_title = ttk.Label(self, text='FTP Product Renaming Service',
                                      font=("Tahoma", 15), justify="center")
        self.window_title.grid(row=0, column=0, columnspan=2, sticky=tk.N)

        # -- directory name --

        self.directory_label = ttk.Label(self, text="Directory:")
        self.directory_label.grid(column=0, row=1, sticky=tk.E, **self.padding)

        self.option = tk.StringVar()
        self.option.set(Variables.CATEGORIES.value[0])

        self.directory_menu = ttk.OptionMenu(
            self, self.option, Variables.CATEGORIES.value[0], *Variables.CATEGORIES.value)
        self.directory_menu.grid(
            column=1, row=1, sticky=tk.EW+tk.E, **self.padding)

        # -- item id ---

        self.id_label = ttk.Label(self, text="Item ID:")
        self.id_label.grid(column=0, row=2, sticky=tk.E, **self.padding)

        self.id_entry = ttk.Entry(self)
        self.id_entry.grid(column=1, row=2, sticky=tk.EW, **self.padding)

        # -- item name ---

        self.name_label = ttk.Label(self, text="New item name:")
        self.name_label.grid(column=0, row=3, sticky=tk.E, **self.padding)

        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(column=1, row=3, sticky=tk.EW, **self.padding)

        # -- submit button --

        self.button = ttk.Button(self, text="Rename", command=self.rename)
        self.button.grid(column=0, row=4, columnspan=2, sticky=tk.N)

        # -- displaying frame --

        self.place(relx=0.5, rely=0.5, anchor="c")

    def rename(self):
        """Handle button clicking to rename files."""

        # -- connecting to FTP server --
        print("Opened FTP connection!")
        ftp = FTP()

        # -- getting variables --

        item_category = str(self.option.get())
        item_id = str(self.id_entry.get())
        item_name = str(self.name_entry.get())

        # -- checking variables --

        if not item_id:
            messagebox.showwarning("Error", "Item ID is empty!")
            return "Item ID is required"

        if not item_name:
            messagebox.showwarning("Error", "Item name is empty!")
            return "New item name is required"

        category_dir = "/" + item_category + "/"
        search = search_names(item_id, get_files(ftp.host, category_dir))

        if not search:
            messagebox.showwarning("Error", "Item ID not found!")
            return "Item ID not found"

        # pylint: disable-msg=W0703
        try:
            parsed_names = []
            names = []
            rewrittens = []

            print(search)
            for name in reversed(search):
                parsed = parse_file_name(name, Variables.IMAGE_PATTERNS.value)
                rewritten = rewrite_file_name(*parsed, item_name)

                print(parsed)

                names.append(name)
                parsed_names.append(parsed[-1])

                if rewritten[1]:
                    ftp.host.rename(
                        category_dir + name, category_dir + rewritten[0])
                    rewrittens.append(rewritten[0])
                else:
                    try:
                        no_extension = False
                        print(f"{parsed_names[-2]} == {parsed[-1]}")
                        if parsed_names[-2] == parsed[-1]:
                            print("Correct name")
                            rewritten = rewrite_file_name(*parsed[:-1], item_name, item_name)
                            no_extension = True

                    except IndexError:
                        print("Index Error")
                        print(len(parsed_names))
                        if len(parsed_names) - 1 == 0:
                            rewritten = rewrite_file_name(*parsed[:-1], item_name, item_name)
                            no_extension = True

                    if not no_extension:
                        rewrittens.append("NOT RENAMED!!! File image type not found!")
                    else:
                        ftp.host.rename(
                            category_dir + name, category_dir + rewritten[0])
                        rewrittens.append(rewritten[0])

            longest_name = len(max(names, key=len))
            message = [f"{name:{longest_name}}: {rewritten}"
                       for name, rewritten in zip(names, rewrittens)]

            messagebox.showinfo("Success!", "\n".join(message))

            print("Closed FTP connection!")
            ftp.close()
            return "OK"
        except Exception as error:
            messagebox.showerror("Error", error)
            ftp.close()
            raise error


class App(tk.Tk):
    """App class for Tkinter GUI"""

    def __init__(self):
        super().__init__()

        self.title("FTP Product Renaming Service")

        self.geometry('300x175+50+50')
        self.resizable(0, 0)
        self.iconbitmap('./assets/ftplogo.ico')


if __name__ == "__main__":
    app = App()
    RenameFrame(app)
    app.mainloop()
