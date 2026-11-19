# Инструменты Playwright MCP

Все инструменты появляются после подключения сервера `playwright`.
В OpenCode они доступны через Code Mode: `tools.playwright.<имя>`.

## Навигация

| Инструмент | Что делает |
|---|---|
| `browser_navigate` | открыть URL |
| `browser_navigate_back` | назад по истории |
| `browser_tabs` | список вкладок, новая, закрыть, переключиться |
| `browser_wait_for` | ждать текст, исчезновение текста или время |

## Чтение страницы

| Инструмент | Что делает |
|---|---|
| `browser_snapshot` | дерево доступности с `ref` для кликов — основной способ |
| `browser_find` | поиск по тексту/regex в snapshot, возвращает совпадения |
| `browser_evaluate` | выполнить JS на странице и вернуть результат |
| `browser_take_screenshot` | PNG текущего экрана или элемента |
| `browser_console_messages` | ошибки и логи консоли |
| `browser_network_requests` | список запросов страницы |
| `browser_network_request` | детали одного запроса: заголовки, тело |

## Действия

| Инструмент | Что делает |
|---|---|
| `browser_click` | клик по `ref` или селектору |
| `browser_type` | ввод текста в поле |
| `browser_fill_form` | заполнить сразу несколько полей |
| `browser_select_option` | выбрать пункт в `<select>` |
| `browser_press_key` | нажать клавишу (`Enter`, `Escape`, `PageDown`) |
| `browser_hover` | навести курсор |
| `browser_drag` | перетащить элемент на элемент |
| `browser_drop` | бросить файл или данные в элемент |
| `browser_file_upload` | загрузить файл в `<input type="file">` |
| `browser_handle_dialog` | принять или отклонить `alert`/`confirm` |

## Оформление и отладка

| Инструмент | Что делает |
|---|---|
| `browser_resize` | задать размер окна, удобно для проверки адаптивности |
| `browser_emulate_media` | тёмная тема, `prefers-reduced-motion` |
| `browser_run_code_unsafe` | произвольный код Playwright (осторожно) |

## Завершение

| Инструмент | Что делает |
|---|---|
| `browser_close` | закрыть браузер и вкладки |

## Правила работы с `ref`

1. `browser_snapshot` выдаёт ссылки вида `[ref=e42]`.
2. `browser_click` принимает `target: "e42"` и `element: "кнопка Войти"`.
3. После навигации или перерисовки страницы `ref` устаревают.
4. Если элемент не найден — сделайте новый snapshot, не угадывайте селектор.

## Что не делает Playwright MCP

- не управляет другими приложениями Windows;
- не работает с файлами вне рабочей папки без специального флага;
- не обходит авторизацию и CAPTCHA;
- не заменяет ручную проверку вёрстки на реальном телефоне.
