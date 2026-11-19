import json
import os
import webbrowser
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except (AttributeError, OSError):
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "links.json")

SECTIONS = (
    ("Готово к отправлению", "Готово к отправке"),
    ("Отправленные задания", "Отправлено"),
)


def load_links():
    try:
        with open(LINKS_FILE, encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def scan_works():
    works = []
    for folder, status in SECTIONS:
        root = os.path.join(BASE, folder)
        if not os.path.isdir(root):
            continue
        for subject in sorted(os.listdir(root)):
            subject_path = os.path.join(root, subject)
            if not os.path.isdir(subject_path):
                continue
            for name in sorted(os.listdir(subject_path)):
                path = os.path.join(subject_path, name)
                if os.path.isdir(path):
                    works.append({
                        "subject": subject,
                        "name": name,
                        "status": status,
                        "path": path,
                        "key": subject + "/" + name,
                    })
    works.sort(key=lambda work: (work["status"] != "Готово к отправке", work["subject"], work["name"]))
    return works


def collect_files(folder):
    files = []
    for root, dirs, names in os.walk(folder):
        dirs[:] = [name for name in dirs if not name.startswith(".")]
        for name in names:
            lower = name.lower()
            if lower == "readme.md" or lower.endswith(".zip"):
                continue
            files.append(os.path.join(root, name))
    return files


def format_size(size):
    if size < 1024:
        return str(size) + " Б"
    if size < 1024 * 1024:
        return "{:.1f} КБ".format(size / 1024)
    return "{:.1f} МБ".format(size / (1024 * 1024))


class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Учебный лаунчер")
        self.minsize(780, 520)
        self.works = []
        self.links = load_links()
        self.current = None
        self.build_ui()
        self.refresh()
        self.place_window()

    def place_window(self):
        width = 940
        height = 620
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry("{}x{}+{}+{}".format(width, height, x, y))

    def build_ui(self):
        style = ttk.Style(self)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TButton", font=("Segoe UI", 10))

        top = ttk.Frame(self, padding=(16, 12, 16, 8))
        top.pack(fill="x")
        ttk.Label(top, text="Учебный лаунчер", font=("Segoe UI", 15, "bold")).pack(side="left")
        self.count_label = ttk.Label(top, text="", foreground="#555555")
        self.count_label.pack(side="right")

        table = ttk.Frame(self, padding=(16, 0, 16, 0))
        table.pack(fill="both", expand=True)

        columns = ("subject", "name", "status")
        self.tree = ttk.Treeview(table, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("subject", text="Предмет")
        self.tree.heading("name", text="Работа")
        self.tree.heading("status", text="Статус")
        self.tree.column("subject", width=150, stretch=False)
        self.tree.column("name", width=560, stretch=True)
        self.tree.column("status", width=150, stretch=False)
        scrollbar = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Double-1>", self.on_double_click)

        details = ttk.LabelFrame(self, text="Выбранная работа", padding=12)
        details.pack(fill="x", padx=16, pady=12)

        self.title_label = ttk.Label(details, text="Выберите работу в списке", font=("Segoe UI", 11, "bold"))
        self.title_label.pack(anchor="w")
        self.meta_label = ttk.Label(details, text="", foreground="#555555")
        self.meta_label.pack(anchor="w", pady=(2, 6))
        self.path_label = ttk.Label(details, text="", foreground="#777777", justify="left")
        self.path_label.pack(anchor="w", pady=(0, 10))

        buttons = ttk.Frame(details)
        buttons.pack(anchor="w")
        self.open_button = ttk.Button(buttons, text="Открыть папку", command=self.open_folder, state="disabled")
        self.open_button.pack(side="left")
        self.readme_button = ttk.Button(buttons, text="Открыть README", command=self.open_readme, state="disabled")
        self.readme_button.pack(side="left", padx=(8, 0))
        self.zip_button = ttk.Button(buttons, text="Собрать ZIP", command=self.make_zip, state="disabled")
        self.zip_button.pack(side="left", padx=(8, 0))
        self.moodle_button = ttk.Button(buttons, text="Открыть в Moodle", command=self.open_moodle, state="disabled")
        self.moodle_button.pack(side="left", padx=(8, 0))

        bottom = ttk.Frame(self, padding=(16, 0, 16, 12))
        bottom.pack(fill="x")
        ttk.Label(
            bottom,
            text="Двойной щелчок по строке открывает папку работы.",
            foreground="#777777",
        ).pack(side="left")
        ttk.Button(bottom, text="Обновить", command=self.refresh).pack(side="right")

        details.bind("<Configure>", self.on_details_resize)

    def on_details_resize(self, event):
        width = max(300, event.width - 40)
        self.title_label.configure(wraplength=width)
        self.path_label.configure(wraplength=width)

    def refresh(self):
        selected_key = self.current["key"] if self.current else None
        self.works = scan_works()
        self.links = load_links()
        self.tree.delete(*self.tree.get_children())
        selected_item = None
        for index, work in enumerate(self.works):
            item = self.tree.insert("", "end", iid=str(index), values=(work["subject"], work["name"], work["status"]))
            if work["key"] == selected_key:
                selected_item = item
        ready = sum(1 for work in self.works if work["status"] == "Готово к отправке")
        self.count_label.configure(text="К отправке: {}    Отправлено: {}".format(ready, len(self.works) - ready))
        if selected_item:
            self.tree.selection_set(selected_item)
            self.tree.focus(selected_item)
            self.on_select()
        else:
            self.clear_details()

    def clear_details(self):
        self.current = None
        self.title_label.configure(text="Выберите работу в списке")
        self.meta_label.configure(text="")
        self.path_label.configure(text="")
        for button in (self.open_button, self.readme_button, self.zip_button, self.moodle_button):
            button.configure(state="disabled")

    def on_select(self, event=None):
        selection = self.tree.selection()
        if not selection:
            self.clear_details()
            return
        self.current = self.works[int(selection[0])]
        work = self.current
        self.title_label.configure(text=work["name"])
        self.meta_label.configure(text=work["subject"] + " · " + work["status"])
        self.path_label.configure(text=work["path"])
        has_readme = os.path.isfile(os.path.join(work["path"], "README.md"))
        has_link = work["key"] in self.links
        self.open_button.configure(state="normal")
        self.readme_button.configure(state="normal" if has_readme else "disabled")
        self.zip_button.configure(state="normal")
        self.moodle_button.configure(state="normal" if has_link else "disabled")

    def on_double_click(self, event):
        row = self.tree.identify_row(event.y)
        if row:
            self.tree.selection_set(row)
            self.open_folder()

    def open_folder(self):
        if not self.current:
            return
        try:
            os.startfile(self.current["path"])
        except (OSError, AttributeError) as error:
            messagebox.showerror("Открыть папку", "Не удалось открыть папку:\n" + str(error))

    def open_readme(self):
        if not self.current:
            return
        path = os.path.join(self.current["path"], "README.md")
        if not os.path.isfile(path):
            messagebox.showinfo("Открыть README", "В папке работы нет README.md.")
            return
        try:
            os.startfile(path)
        except (OSError, AttributeError) as error:
            messagebox.showerror("Открыть README", "Не удалось открыть файл:\n" + str(error))

    def make_zip(self):
        if not self.current:
            return
        work = self.current
        files = collect_files(work["path"])
        if not files:
            messagebox.showwarning("Собрать ZIP", "В папке работы нет файлов для архива.")
            return
        target = filedialog.asksaveasfilename(
            parent=self,
            title="Сохранить архив",
            initialdir=work["path"],
            initialfile=work["name"] + ".zip",
            defaultextension=".zip",
            filetypes=[("ZIP-архив", "*.zip")],
        )
        if not target:
            return
        try:
            with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
                for path in files:
                    archive.write(path, os.path.relpath(path, work["path"]).replace(os.sep, "/"))
        except OSError as error:
            messagebox.showerror("Собрать ZIP", "Не удалось создать архив:\n" + str(error))
            return
        messagebox.showinfo(
            "Собрать ZIP",
            "Архив сохранён:\n" + target + "\n\nФайлов: {}    Размер: {}".format(
                len(files), format_size(os.path.getsize(target))
            ),
        )

    def open_moodle(self):
        if not self.current:
            return
        link = self.links.get(self.current["key"])
        if not link:
            messagebox.showinfo("Открыть в Moodle", "Для этой работы ссылка не задана в links.json.")
            return
        webbrowser.open(link)


def main():
    app = Launcher()
    app.mainloop()


if __name__ == "__main__":
    main()
