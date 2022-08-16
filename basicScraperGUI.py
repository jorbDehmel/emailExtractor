import tkinter as tk
from tkinter import filedialog as fd
import requests as r
from regex import split

class Scraper:
    """
    GUI for basic web scraping.
    """

    def get_paths(self):
        """
        Opens a file selection screen,
        then gets links from selected file.
        :return: None
        """
        with fd.askopenfile() as file:
            self.links = split(r'[ \n]', file.read())
        self.label.configure(text='File opened')
        return

    def end(self, filepath):
        """
        Runs after data processing.
        Displays a simple panel of what was
        scraped.
        :param filepath: The path of the output file
        :return: None
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        # Label
        tk.Label(self.root, text='Found:').pack()

        # Display output file
        with open(filepath, 'r') as file:
            text = file.read()
        scrollbar = tk.Scrollbar(self.root)
        mylist = tk.Listbox(self.root, yscrollcommand=scrollbar.set, height=5, width=24)
        for i in split('\n', text):
            mylist.insert(tk.END, i)
        mylist.pack()

        tk.Label(self.root, text='(Saved to output file)').pack()
        tk.Button(self.root, text='Quit', command=self.root.destroy).pack()

        return

    def update(self):
        """
        Moves from the type selection screen
        to the data input screen.
        :return: None
        """
        selection = self.clicked.get()
        if selection == 'Input type':
            self.label.configure(text='Fields missing!')
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        # Label
        self.label = tk.Label(self.root, text=self.name)
        self.label.pack()

        if selection == 'Enter file':
            # File select button
            button = tk.Button(self.root, text='Select file', command=self.get_paths)
            button.pack()
        else:  # Enter link
            # Link input text box
            self.field = tk.Text(self.root, width=10, height=1)
            self.field.pack()

        # Run button
        run_button = tk.Button(self.root, text='Run', command=self.run)
        run_button.pack()

        return

    def run(self):
        """
        Does all data processing.
        :return: None
        """
        self.label.configure(text='Working...')

        if not isinstance(self.field, bool):
            self.links = [self.field.get('0.0', tk.END)]
        out = []

        for link in self.links:
            link = link.strip()
            if 'http' not in link:
                link = 'http://' + link
            read = r.get(url=link, headers={"User-Agent": "Mozilla/5.0"})
            if read.status_code == 404:
                out.append('REQUEST FAILED: ' + read.url)
                continue
            read = read.text
            for i in self.run_func(read):
                if i is not None:
                    out.append(''.join(i))
                    out.append('\n')

        path = fd.askopenfilename()
        with open(path, 'w') as file:
            for string in out:
                file.write(string)
        self.end(path)

        return

    def __init__(self, func, name='Web scraper', windowname='', geom='160x160'):
        """
        Creates and opens a window containing a
        basic web scraping Graphical User Interface.

        Flow in window:
        Input type selection screen -> Input screen ->
            *data processing* -> End screen
        :param func: The function that extracts useful data from
            the raw html received.
        """
        self.name = name
        self.field = False
        self.path = ''
        self.output_path = ''
        self.links = []

        self.run_func = func

        self.root = tk.Tk()
        self.root.geometry(geom)
        self.root.title(windowname)

        self.label = tk.Label(self.root, text=self.name)
        self.label.pack()

        # Menu selector
        self.clicked = tk.StringVar()
        self.clicked.set("Input type")
        drop = tk.OptionMenu(self.root, self.clicked, *["Enter link", "Enter file"])
        drop.pack()

        # Update button
        select = tk.Button(self.root, text='Update', command=self.update)
        select.pack()

        # Dev info label
        devinfo = tk.Label(self.root, text='\n\n\n\n2022, jdehmel@outlook.com')
        devinfo.pack()

        self.root.mainloop()
