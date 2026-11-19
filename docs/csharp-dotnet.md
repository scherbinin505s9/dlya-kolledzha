# C# и .NET (МДК.01.01)

Основной язык профессиональных модулей в 09.02.07 — C#. Здесь всё, чтобы запустить
первую лабораторную и не искать по форумам.

## Установка .NET SDK

```bash
# Ubuntu / Debian: официальный скрипт
curl -fsSL https://dot.net/v1/dotnet-install.sh -o dotnet-install.sh
chmod +x dotnet-install.sh
./dotnet-install.sh --channel 10.0          # LTS-ветка на 2026 год
export PATH="$HOME/.dotnet:$PATH"
```

Скрипт репозитория:

```bash
bash scripts/install-dotnet.sh
```

Проверка:

```bash
dotnet --version
dotnet --list-sdks
```

Windows: `winget install Microsoft.DotNet.SDK.10` (или через установщик с dot.net).

> В колледже может стоять .NET 8 — это тоже LTS. Ставь ту версию, которую требует преподаватель:
> `--channel 8.0`. Проекты на .NET 8 открываются в SDK 10, но не наоборот.

## Первый проект

```bash
dotnet new console -o Lab1
cd Lab1
dotnet run
```

Структура:

```
Lab1/
├── Lab1.csproj      # настройки проекта
├── Program.cs       # код
└── obj/ bin/        # сборка, в git не коммитится
```

Основные команды:

```bash
dotnet new console -o Имя       # консольный проект
dotnet new list                 # все шаблоны
dotnet build                    # собрать
dotnet run                      # собрать и запустить
dotnet run -- аргумент          # передать аргументы
dotnet test                     # запустить тесты
dotnet add package Newtonsoft.Json   # добавить NuGet-пакет
dotnet restore                  # восстановить зависимости
dotnet clean                    # очистить сборку
```

## Минимальная программа

```csharp
Console.Write("Введите число: ");
int n = int.Parse(Console.ReadLine()!);

if (n % 2 == 0)
    Console.WriteLine($"{n} — чётное");
else
    Console.WriteLine($"{n} — нечётное");
```

Ввод нужно проверять — на защите спросят про буквы вместо цифр:

```csharp
Console.Write("Введите число: ");
if (!int.TryParse(Console.ReadLine(), out int n))
{
    Console.WriteLine("Это не число");
    return;
}
```

## Синтаксис, который нужен постоянно

```csharp
// массив
int[] a = { 3, 1, 2 };
Array.Sort(a);
Console.WriteLine(string.Join(", ", a));

// список
var list = new List<int> { 1, 2, 3 };
list.Add(4);

// словарь
var ages = new Dictionary<string, int> { ["Аня"] = 19 };
ages["Иван"] = 20;

// строка
string s = "привет";
Console.WriteLine(s.Length);
Console.WriteLine(s.ToUpper());
Console.WriteLine(string.Join("-", s.ToCharArray()));

// цикл
for (int i = 0; i < a.Length; i++) { }
foreach (var x in list) { }

// функция
static int Sum(int[] numbers)
{
    int sum = 0;
    foreach (var x in numbers) sum += x;
    return sum;
}
```

## ООП по программе

```csharp
public class Student
{
    public string Name { get; set; } = "";
    public int Age { get; set; }

    public Student(string name, int age)
    {
        Name = name;
        Age = age;
    }

    public override string ToString() => $"{Name}, {Age}";
}

var s = new Student("Иван", 17);
Console.WriteLine(s);
```

Что обычно требуют: класс, конструктор, свойства, методы, наследование,
переопределение `ToString()`, список объектов, сортировка.

```csharp
var students = new List<Student>
{
    new("Аня", 18),
    new("Иван", 17),
};

foreach (var st in students.OrderBy(x => x.Age))
    Console.WriteLine(st);
```

## Обработка исключений

```csharp
try
{
    int x = int.Parse("не число");
}
catch (FormatException)
{
    Console.WriteLine("Некорректный формат");
}
catch (Exception ex)
{
    Console.WriteLine($"Ошибка: {ex.Message}");
}
finally
{
    Console.WriteLine("Выполнится всегда");
}
```

## Файлы

```csharp
File.WriteAllText("result.txt", "строка");
string text = File.ReadAllText("result.txt");

File.WriteAllLines("lines.txt", new[] { "первая", "вторая" });
var lines = File.ReadAllLines("lines.txt");
```

## Тесты (МДК.01.02)

```bash
dotnet new xunit -o Lab1.Tests
cd Lab1.Tests
dotnet add reference ../Lab1/Lab1.csproj
dotnet test
```

```csharp
public class MathTests
{
    [Fact]
    public void Gcd_ReturnsSix()
    {
        Assert.Equal(6, Program.Gcd(12, 18));
    }

    [Theory]
    [InlineData(2, 4, 2)]
    [InlineData(9, 6, 3)]
    public void Gcd_Works(int a, int b, int expected)
    {
        Assert.Equal(expected, Program.Gcd(a, b));
    }
}
```

## VS Code для C#

Расширения:

```bash
code --install-extension ms-dotnettools.csharp
code --install-extension ms-dotnettools.csdevkit
```

`F5` — отладка с точками останова, `Ctrl+Shift+B` — сборка.

## .gitignore для C#

```
bin/
obj/
*.user
.vs/
```

## Частые ошибки

| Ошибка | Причина | Решение |
|---|---|---|
| `dotnet: command not found` | SDK не в `PATH` | `export PATH="$HOME/.dotnet:$PATH"` |
| `SDK not found` | нет подходящей версии | `dotnet --list-sdks`, поставить нужную |
| `Program does not contain a static 'Main'` | нет точки входа | `Main` или top-level statements в `Program.cs` |
| `NullReferenceException` | обращение к `null` | проверить `if (obj != null)`, `?.` |
| `Input string was not in a correct format` | `int.Parse` на буквах | `int.TryParse` |
| `CS0246 тип не найден` | нет `using` или ссылки | добавить `using`/`dotnet add reference` |
| `Нет доступа к файлу` | запущено два экземпляра | закрыть лишний процесс |
| Проект не собирается после clone | нет пакетов | `dotnet restore` |
