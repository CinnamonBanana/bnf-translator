import imp
import tkinter as tk
from tkinter import font as tkFont

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, start="1.0", end="end",
                          regexp=False):
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)
        self.tag_configure("highlight", background="red", foreground="white")
        self.tag_configure("default", background="white", foreground="black")
        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd", "searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add("highlight", "matchStart", "matchEnd")
        

class BNFWindow():
    def __init__(self, func=None) -> None:
        self.window = tk.Tk()
        self.window.geometry("800x600+1000+300")
        self.window.title('Translator')
        self.code_space()
        self.lang_space()
        self.start_button(func)
        self.output()
        self.config()

    def code_space(self):
        self.code = CustomText(self.window, wrap=tk.WORD)
        self.code.grid(row=0, column=0, sticky=tk.NE+tk.SE, padx=5, pady=5)
        self.code.tag_configure("highlight", background="red", foreground="white")

    def lang_space(self):
        with open('lang.txt', 'r') as f:
            bnf = f.read()
        self.lang = tk.Text(self.window, wrap=tk.WORD)
        self.lang.grid(row=0, column=1, sticky=tk.NW+tk.SW, padx=5, pady=5)
        self.lang.insert(1.0, bnf)

        
    def start_button(self, func):
        self.runbutton = tk.Button(self.window, text="Запуск", command=func)
        self.runbutton.grid(row=1, column=0, pady=5)

    def output(self):
        self.console = tk.Text(self.window, height=5, wrap=tk.WORD)
        self.console.grid(row=2, column=0, columnspan=2, sticky=tk.SW+tk.SE)

    def config(self):
        self.window.rowconfigure(0, weight=3)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

    def get_code(self):
        return self.code.get("1.0", tk.END)
    
    def set_code(self, code):
        self.code.delete("1.0", tk.END)
        self.code.insert(1.0, code)
    
    def update_code(self):
        code = self.code.get("1.0", tk.END)
        self.code.delete("1.0", tk.END)
        self.code.insert(1.0, code)
    
    def set_con(self, out):
        self.console.delete("1.0", tk.END)
        self.console.insert(1.0, out)
    
    def clear_con(self):
        self.console.delete("1.0", tk.END)

    def mainloop(self):
        self.window.mainloop()


if __name__ == '__main__':
    window = BNFWindow()
    window.mainloop()