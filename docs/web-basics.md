# Основы веб-разработки (ОП.14)

## Минимальная страница

`index.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Лабораторная 1</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <h1>Мой сайт</h1>
    <nav>
      <a href="#about">О себе</a>
      <a href="#contacts">Контакты</a>
    </nav>
  </header>

  <main>
    <section id="about">
      <h2>О себе</h2>
      <p>Студент колледжа АлтГУ, специальность 09.02.07.</p>
      <img src="photo.jpg" alt="Фотография" width="200">
    </section>

    <section id="contacts">
      <h2>Контакты</h2>
      <ul>
        <li>Email: <a href="mailto:student@example.com">student@example.com</a></li>
      </ul>
    </section>
  </main>

  <footer>
    <p>© 2026</p>
  </footer>

  <script src="script.js"></script>
</body>
</html>
```

Запуск без установки чего-либо:

```bash
python3 -m http.server 8000
# открыть http://127.0.0.1:8000
```

Или через Node.js:

```bash
npx --yes serve .
```

> Открывать `index.html` двойным щелчком можно, но тогда не работают модули JS,
> `fetch` и относительные пути. Для лабораторных всегда поднимайте локальный сервер.

## CSS: минимум для сдачи

`style.css`:

```css
* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  line-height: 1.5;
  color: #222;
}

header, main, footer {
  max-width: 900px;
  margin: 0 auto;
  padding: 16px;
}

nav a {
  margin-right: 12px;
  color: #0a58ca;
  text-decoration: none;
}

nav a:hover { text-decoration: underline; }

section { margin-bottom: 32px; }

img { max-width: 100%; height: auto; border-radius: 8px; }
```

### Flexbox

```css
.row {
  display: flex;
  gap: 16px;
  justify-content: space-between;   /* по главной оси */
  align-items: center;              /* по поперечной */
  flex-wrap: wrap;
}
```

### Grid

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}
```

### Адаптивность

```css
@media (max-width: 600px) {
  header, main, footer { padding: 12px; }
  h1 { font-size: 24px; }
}
```

Основы: `margin` — снаружи, `padding` — внутри, `border` — рамка.
`box-sizing: border-box` избавляет от неожиданных размеров.

## JavaScript

```html
<button id="add">Добавить</button>
<ul id="list"></ul>
<input id="task" placeholder="Новая задача">
```

```javascript
const list = document.getElementById("list");
const input = document.getElementById("task");

document.getElementById("add").addEventListener("click", () => {
  const text = input.value.trim();
  if (!text) return;

  const li = document.createElement("li");
  li.textContent = text;
  li.addEventListener("click", () => li.remove());
  list.appendChild(li);
  input.value = "";
});
```

Что требуется знать: переменные (`let`, `const`), функции, массивы и объекты,
`for...of`, шаблонные строки, `addEventListener`, `querySelector`, `classList`.

## fetch: запрос к API

```javascript
async function loadUsers() {
  const response = await fetch("https://jsonplaceholder.typicode.com/users");
  if (!response.ok) {
    console.error("Ошибка:", response.status);
    return;
  }
  const users = await response.json();
  console.log(users.map(u => u.name));
}
loadUsers();
```

## Форма с проверкой

```html
<form id="form">
  <input name="email" type="email" required>
  <button>Отправить</button>
  <p id="msg"></p>
</form>
```

```javascript
document.getElementById("form").addEventListener("submit", (e) => {
  e.preventDefault();
  const email = e.target.email.value;
  const msg = document.getElementById("msg");

  if (!email.includes("@")) {
    msg.textContent = "Некорректный email";
    return;
  }
  msg.textContent = "Отправлено";
  e.target.reset();
});
```

## Инструменты разработчика

`F12` или `Ctrl+Shift+I`:

- **Elements** — HTML и стили, можно менять на лету;
- **Console** — ошибки JS и `console.log`;
- **Network** — запросы, коды ответов, время;
- **Application** — localStorage, cookie.

Проверка вёрстки: уменьшить окно до 375 px и убедиться, что ничего не вылезает.

## Git и GitHub Pages

```bash
git init
git add .
git commit -m "сайт"
gh repo create site --public --source . --push
```

Включить Pages: репозиторий → **Settings → Pages** → Branch `main` / root.
Через минуту сайт доступен по адресу `https://<логин>.github.io/site/`.

## Структура проекта

```
site/
├── index.html
├── css/style.css
├── js/script.js
├── img/
└── README.md
```

Ссылки в HTML тогда будут `css/style.css`, `js/script.js`, `img/photo.jpg`.

## Figma и Tilda

По «Основам веб-технологий» часть работ делают не кодом, а в редакторах.
Требования методички важнее любых советов ниже.

### Figma

- макет под десктоп: фрейм `1440×900`, мобильный — `375×812`;
- сетка: 12 колонок, отступ 24 px;
- компоненты: кнопка, карточка, поле ввода — один раз, потом копии;
- прототип: выделить кнопку → **Prototype** → стрелка на нужный экран;
- сдача: ссылка «Поделиться» с доступом «Все, у кого есть ссылка, могут просматривать».

Что обычно проверяют: выравнивание, единые отступы, читаемый контраст,
адаптивная версия, работающие ссылки в прототипе.

### Tilda

1. Создать проект → выбрать шаблон под задачу.
2. Блоки: обложка, текст, галерея, форма, футер.
3. Настроить шрифты и цвета в **Настройки сайта**.
4. Проверить на телефоне: кнопка предпросмотра.
5. Опубликовать и приложить ссылку + скриншоты.

Для индивидуального проекта чаще требуют не «красиво», а структуру:
цель, актуальность, обзор, практическая часть, выводы. Текст готовьте
заранее — в Tilda его только оформляют.

## Частые ошибки

| Симптом | Причина | Решение |
|---|---|---|
| Стили не применяются | неверный путь или кэш | проверить Network, `Ctrl+F5` |
| `Uncaught TypeError: null` | элемент не найден | скрипт в конце `body` или `DOMContentLoaded` |
| Русский текст «кракозябрами» | нет `<meta charset="UTF-8">` | добавить в `head` |
| `CORS policy` | запрос на чужой домен | использовать API с CORS или свой сервер |
| Картинка не грузится | регистр в имени файла | `Photo.JPG` ≠ `photo.jpg` |
| Всё «съехало» на телефоне | нет `viewport` | `<meta name="viewport" ...>` |
| `fetch` в файле `file://` | ограничение браузера | запускать через локальный сервер |
