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
CATALOG_FILE = os.path.join(BASE, "docs", "assignments.json")

SECTIONS = (
    ("Готово к отправлению", "Готово к отправке"),
    ("Отправленные задания", "Отправлено"),
)


def load_catalog():
    try:
        with open(CATALOG_FILE, encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, ValueError):
        return {}
    entries = {}
    for subject, course in data.items():
        if not isinstance(course, dict):
            continue
        for work in course.get("works", []):
            if isinstance(work, dict) and work.get("name"):
                entries[subject + "/" + work["name"]] = work
    return entries


def parse_card(path):
    try:
        with open(path, encoding="utf-8") as file:
            text = file.read()
    except OSError:
        return {}
    intro = text.split("\n## ", 1)[0]
    fields = {}
    for line in intro.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) != 2:
            continue
        key, value = parts
        if not key or set(key) <= {"-", ":"}:
            continue
        fields[key] = value
    return fields


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
                readme = os.path.join(path, "README.md")
                if os.path.isdir(path) and os.path.isfile(readme):
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
    manifest = os.path.join(folder, "files.txt")
    files = []
    seen = set()

    def add(path):
        if path not in seen:
            seen.add(path)
            files.append(path)

    if os.path.isfile(manifest):
        missing = []
        with open(manifest, encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
        for line in lines:
            normalized = line.replace("\\", "/")
            if ".." in normalized.split("/"):
                missing.append(line)
                continue
            parts = [part for part in normalized.rstrip("/").split("/") if part]
            path = os.path.join(folder, *parts)
            if os.path.isdir(path):
                for root, dirs, names in os.walk(path):
                    dirs[:] = [name for name in dirs if not name.startswith(".")]
                    for name in names:
                        add(os.path.join(root, name))
            elif os.path.isfile(path):
                add(path)
            else:
                missing.append(line)
        if missing:
            raise ValueError("В files.txt указаны отсутствующие пути:\n" + "\n".join(missing))
        return files, True

    for root, dirs, names in os.walk(folder):
        dirs[:] = [name for name in dirs if not name.startswith(".")]
        for name in names:
            lower = name.lower()
            if lower == "readme.md" or lower.endswith(".zip"):
                continue
            add(os.path.join(root, name))
    return files, False


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
        self.minsize(780, 560)
        self.works = []
        self.catalog = load_catalog()
        self.current = None
        self.card = {}
        self.build_ui()
        self.refresh()
        self.place_window()

    def place_window(self):
        width = 940
        height = 660
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
        self.meta_label.pack(anchor="w", pady=(2, 4))
        self.info_label = ttk.Label(details, text="", foreground="#555555", justify="left")
        self.info_label.pack(anchor="w", pady=(0, 4))
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
        self.info_label.configure(wraplength=width)
        self.path_label.configure(wraplength=width)

    def refresh(self):
        selected_key = self.current["key"] if self.current else None
        self.works = scan_works()
        self.catalog = load_catalog()
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
        self.card = {}
        self.title_label.configure(text="Выберите работу в списке")
        self.meta_label.configure(text="")
        self.info_label.configure(text="")
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
        self.card = parse_card(os.path.join(work["path"], "README.md"))
        entry = self.catalog.get(work["key"], {})
        self.title_label.configure(text=work["name"])
        self.meta_label.configure(text=work["subject"] + " · " + work["status"])

        details = []
        status = self.card.get("Статус", "")
        if status and status != work["status"]:
            details.append("Статус: " + status)
        grade = self.card.get("Оценка", "")
        if grade and grade != "—":
            details.append("Оценка: " + grade)
        sent_date = self.card.get("Дата сдачи", "")
        if sent_date and sent_date != "—":
            details.append("Сдано: " + sent_date)
        else:
            work_date = self.card.get("Дата работы", "")
            if work_date:
                details.append("Дата работы: " + work_date)
        deadline = entry.get("deadline", "")
        details.append("Срок сдачи: " + (deadline if deadline else "не указан"))
        archive = self.card.get("Архив", "")
        if archive and archive != "—":
            details.append("Архив: " + archive)
        self.info_label.configure(text=" · ".join(details))

        self.path_label.configure(text=work["path"])
        has_readme = os.path.isfile(os.path.join(work["path"], "README.md"))
        has_link = bool(entry.get("url"))
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
        try:
            files, has_manifest = collect_files(work["path"])
        except ValueError as error:
            messagebox.showerror("Собрать ZIP", str(error))
            return
        if not files:
            messagebox.showwarning("Собрать ZIP", "В папке работы нет файлов для архива.")
            return
        if not has_manifest:
            question = (
                "Файл files.txt не найден. В архив попадут все файлы работы, "
                "кроме README.md и архивов. Продолжить?"
            )
            if not messagebox.askyesno("Собрать ZIP", question):
                return
        archive_name = self.card.get("Архив", "")
        if not archive_name or archive_name == "—" or not archive_name.lower().endswith(".zip"):
            archive_name = work["name"] + ".zip"
        target = filedialog.asksaveasfilename(
            parent=self,
            title="Сохранить архив",
            initialdir=work["path"],
            initialfile=archive_name,
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
        link = self.catalog.get(self.current["key"], {}).get("url", "")
        if not link:
            messagebox.showinfo("Открыть в Moodle", "Для этой работы нет ссылки в docs/assignments.json.")
            return
        webbrowser.open(link)


def main():
    app = Launcher()
    app.mainloop()


if __name__ == "__main__":
    main()
