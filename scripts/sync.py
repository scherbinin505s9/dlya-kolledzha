import json
import os
import sys
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_FILE = os.path.join(BASE, "docs", "assignments.json")

SECTIONS = (
    ("Готово к отправлению", "Готово к отправке"),
    ("Отправленные задания", "Отправлено"),
)

REQUIRED_FIELDS = (
    "Предмет",
    "Раздел курса",
    "Задание",
    "Дата работы",
    "Дата сдачи",
    "Статус",
    "Оценка",
    "Архив",
)

START_MARKER = "<!-- начало списка -->"
END_MARKER = "<!-- конец списка -->"

errors = []
warnings = []


def read_text(path):
    with open(path, encoding="utf-8") as file:
        return file.read()


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        file.write(text)


def parse_card(path):
    text = read_text(path)
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


def check_date(value):
    if value in ("", "—"):
        return True
    try:
        datetime.strptime(value, "%d.%m.%Y")
    except ValueError:
        return False
    return True


def check_work(work):
    card = parse_card(work["readme"])
    for field in REQUIRED_FIELDS:
        if field not in card:
            errors.append("{}: в README нет поля «{}»".format(work["label"], field))
        elif not card[field]:
            errors.append("{}: поле «{}» пустое".format(work["label"], field))
    for field in ("Дата работы", "Дата сдачи"):
        value = card.get(field, "")
        if value and not check_date(value):
            errors.append("{}: поле «{}» не в формате ДД.ММ.ГГГГ".format(work["label"], field))
    status = card.get("Статус", "")
    if work["section_status"] == "Готово к отправке" and "Отправлено" in status:
        warnings.append("{}: работа в «Готово к отправлению», но статус «{}»".format(work["label"], status))
    if work["section_status"] == "Отправлено" and ("не отправлено" in status or "Готово к отправке" in status):
        warnings.append("{}: работа в «Отправленные задания», но статус «{}»".format(work["label"], status))
    if work["section_status"] == "Отправлено" and card.get("Дата сдачи") in ("", "—"):
        warnings.append("{}: не указана дата сдачи".format(work["label"]))
    archive = card.get("Архив", "")
    if archive and archive != "—" and not archive.lower().endswith(".zip"):
        warnings.append("{}: имя архива должно заканчиваться на .zip".format(work["label"]))
    if work["section_status"] == "Готово к отправке" and archive in ("", "—"):
        warnings.append("{}: не указано имя архива".format(work["label"]))
    return card


def check_files(work):
    manifest = work["files_file"]
    if not os.path.isfile(manifest):
        errors.append("{}: нет files.txt".format(work["label"]))
        return
    lines = [line.strip() for line in read_text(manifest).splitlines() if line.strip()]
    if not lines:
        errors.append("{}: files.txt пустой".format(work["label"]))
        return
    for line in lines:
        normalized = line.replace("\\", "/")
        if ".." in normalized.split("/"):
            errors.append("{}: недопустимый путь в files.txt — {}".format(work["label"], line))
            continue
        if os.path.basename(normalized).lower() in ("readme.md",) or normalized.lower().endswith(".zip"):
            warnings.append("{}: в files.txt лишний файл — {}".format(work["label"], line))
        parts = [part for part in normalized.rstrip("/").split("/") if part]
        path = os.path.join(work["path"], *parts)
        if normalized.endswith("/"):
            if not os.path.isdir(path):
                errors.append("{}: в files.txt нет папки — {}".format(work["label"], line))
        elif os.path.isdir(path):
            warnings.append("{}: папку лучше указывать со слешем — {}".format(work["label"], line))
        elif not os.path.isfile(path):
            errors.append("{}: в files.txt нет файла — {}".format(work["label"], line))


def scan_works():
    works = []
    for folder, section_status in SECTIONS:
        root = os.path.join(BASE, folder)
        if not os.path.isdir(root):
            continue
        for subject in sorted(os.listdir(root)):
            subject_path = os.path.join(root, subject)
            if not os.path.isdir(subject_path):
                continue
            for name in sorted(os.listdir(subject_path)):
                path = os.path.join(subject_path, name)
                if not os.path.isdir(path):
                    continue
                readme = os.path.join(path, "README.md")
                if not os.path.isfile(readme):
                    warnings.append("Папка без README.md: {}".format(os.path.relpath(path, BASE)))
                    continue
                works.append({
                    "subject": subject,
                    "name": name,
                    "path": path,
                    "readme": readme,
                    "files_file": os.path.join(path, "files.txt"),
                    "section": folder,
                    "section_status": section_status,
                    "label": subject + "/" + name,
                })
    return works


def load_catalog():
    if not os.path.isfile(CATALOG_FILE):
        errors.append("Нет файла docs/assignments.json")
        return {}
    try:
        data = json.loads(read_text(CATALOG_FILE))
    except ValueError as error:
        errors.append("docs/assignments.json: " + str(error))
        return {}
    entries = {}
    for subject, course in data.items():
        if not isinstance(course, dict):
            warnings.append("assignments.json: предмет «{}» должен быть объектом".format(subject))
            continue
        works = course.get("works", [])
        if not isinstance(works, list):
            warnings.append("assignments.json: у предмета «{}» список работ должен быть массивом".format(subject))
            continue
        for work in works:
            if not isinstance(work, dict) or not work.get("name"):
                warnings.append("assignments.json: у предмета «{}» есть запись без названия".format(subject))
                continue
            key = (subject, work["name"])
            if key in entries:
                warnings.append("assignments.json: повторяется работа «{}»".format(work["name"]))
                continue
            entries[key] = work
            if not work.get("url"):
                warnings.append("assignments.json: у работы «{}» нет ссылки".format(work["name"]))
            deadline = work.get("deadline", "")
            if deadline and not check_date(deadline):
                warnings.append("assignments.json: у работы «{}» срок не в формате ДД.ММ.ГГГГ".format(work["name"]))
    return entries


def build_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def work_link(work):
    path = work["subject"] + "/" + work["name"] + "/README.md"
    return path.replace(" ", "%20").replace("(", "%28").replace(")", "%29")


def update_section(folder, headers, rows):
    path = os.path.join(BASE, folder, "README.md")
    if not os.path.isfile(path):
        errors.append("Нет файла {}".format(os.path.relpath(path, BASE)))
        return
    text = read_text(path)
    if START_MARKER not in text or END_MARKER not in text:
        errors.append("{}: нет маркеров списка".format(os.path.relpath(path, BASE)))
        return
    start = text.index(START_MARKER) + len(START_MARKER)
    end = text.index(END_MARKER)
    if end < start:
        errors.append("{}: маркеры списка стоят не по порядку".format(os.path.relpath(path, BASE)))
        return
    table = build_table(headers, rows)
    write_text(path, text[:start] + "\n" + table + "\n" + text[end:])
    print("Обновлено: {}".format(os.path.relpath(path, BASE)))


def main():
    errors.clear()
    warnings.clear()
    works = scan_works()
    catalog = load_catalog()
    cards = {}
    for work in works:
        cards[work["label"]] = check_work(work)
        check_files(work)
        if (work["subject"], work["name"]) not in catalog:
            warnings.append("{}: нет ссылки в docs/assignments.json".format(work["label"]))

    ready_rows = []
    sent_rows = []
    for work in works:
        card = cards.get(work["label"], {})
        status = card.get("Статус") or work["section_status"]
        link = "[{}]({})".format(work["name"], work_link(work))
        if work["section_status"] == "Готово к отправке":
            ready_rows.append([work["subject"], link, status])
        else:
            sent_rows.append([work["subject"], link, card.get("Дата сдачи") or "—", status])

    ready_rows.sort(key=lambda row: (row[0], row[1]))
    sent_rows.sort(key=lambda row: (row[0], row[1]))

    update_section("Готово к отправлению", ["Предмет", "Работа", "Статус"], ready_rows)
    update_section("Отправленные задания", ["Предмет", "Работа", "Дата сдачи", "Статус"], sent_rows)

    for warning in warnings:
        print("Предупреждение: " + warning)
    for error in errors:
        print("Ошибка: " + error)
    print("Проверено работ: {}".format(len(works)))
    print("Ошибок: {}    Предупреждений: {}".format(len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
