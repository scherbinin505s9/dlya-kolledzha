# Компьютерные сети (ОП.11)

## Модель OSI и TCP/IP

| OSI | TCP/IP | Примеры | Устройства |
|---|---|---|---|
| 7 Прикладной | Прикладной | HTTP, DNS, SSH, FTP | — |
| 6 Представления | Прикладной | TLS, кодировки | — |
| 5 Сеансовый | Прикладной | RPC, сессии | — |
| 4 Транспортный | Транспортный | TCP, UDP | — |
| 3 Сетевой | Межсетевой | IP, ICMP | маршрутизатор |
| 2 Канальный | Доступ к сети | Ethernet, Wi-Fi, ARP | коммутатор |
| 1 Физический | Доступ к сети | кабель, радио | концентратор |

Запомнить: **PDU** — данные (7-5), сегмент (4), пакет (3), кадр (2), биты (1).

## IP-адреса и маски

IPv4 — 32 бита, 4 октета: `192.168.1.10`.

| Маска | Префикс | Устройств в сети |
|---|---|---|
| 255.0.0.0 | /8 | 16 777 214 |
| 255.255.0.0 | /16 | 65 534 |
| 255.255.255.0 | /24 | 254 |
| 255.255.255.192 | /26 | 62 |
| 255.255.255.252 | /30 | 2 |

Частные диапазоны: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
`127.0.0.1` — loopback, `169.254.x.x` — адрес не получен по DHCP.

### Как посчитать подсеть

Для `192.168.10.37/26`:

1. `/26` → маска `255.255.255.192`, шаг 64.
2. Сети: `.0`, `.64`, `.128`, `.192`.
3. `.37` попадает в `.0/26`.
4. Адрес сети `192.168.10.0`, broadcast `192.168.10.63`, хосты `.1–.62`.

Проверка калькулятором: `ipcalc 192.168.10.37/26` (пакет `ipcalc`).

## Порты

| Порт | Служба |
|---|---|
| 20/21 | FTP |
| 22 | SSH |
| 25/587 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 3389 | RDP |

Порты до 1024 — привилегированные, для запуска нужен root.

## DHCP, DNS, NAT

- **DHCP** выдаёт IP, маску, шлюз и DNS автоматически.
- **DNS** переводит имя в IP: `ya.ru` → `77.88.55.88`.
- **NAT** подменяет частные адреса на один публичный при выходе в интернет.
- **Шлюз** (gateway) — адрес, через который идёт трафик в другие сети.

## Настройка сети в Linux

```bash
ip a                      # интерфейсы и адреса
ip r                      # таблица маршрутизации
ip link set eth0 up       # включить интерфейс
sudo ip addr add 192.168.1.50/24 dev eth0
sudo ip route add default via 192.168.1.1
```

Постоянно (NetworkManager):

```bash
nmcli device status
nmcli connection show
sudo nmcli connection modify "Wired connection 1" ipv4.method manual \
  ipv4.addresses 192.168.1.50/24 ipv4.gateway 192.168.1.1 ipv4.dns 8.8.8.8
sudo nmcli connection up "Wired connection 1"
```

Ubuntu Server (netplan) — файл `/etc/netplan/00-installer-config.yaml`:

```yaml
network:
  ethernets:
    eth0:
      dhcp4: false
      addresses: [192.168.1.50/24]
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
  version: 2
```

```bash
sudo netplan apply
```

## Диагностика

```bash
ping -c 4 8.8.8.8              # доступность узла
ping -c 4 ya.ru                # проверка DNS + сети
traceroute ya.ru               # маршрут до узла
dig ya.ru                      # DNS-запрос
nslookup ya.ru
ss -tulpn                      # открытые порты
ss -tnp                        # активные соединения
curl -v https://ya.ru          # HTTP-запрос с деталями
curl -I https://ya.ru          # только заголовки
nc -zv 192.168.1.10 22         # проверить порт
```

Если `ping 8.8.8.8` работает, а `ping ya.ru` нет — проблема в DNS.
Если не работает и то и другое — проблема в шлюзе или кабеле.

## HTTP на пальцах

```bash
curl -X GET https://api.github.com/repos/nodejs/node
curl -X POST -H "Content-Type: application/json" -d '{"a":1}' https://httpbin.org/post
```

| Код | Значение |
|---|---|
| 200 | OK |
| 301/302 | перенаправление |
| 400 | неверный запрос |
| 401/403 | не авторизован / нет прав |
| 404 | не найдено |
| 500 | ошибка сервера |

Методы: `GET` — получить, `POST` — создать, `PUT/PATCH` — изменить, `DELETE` — удалить.

## Практика: мини-лаборатория

Терминал 1 — сервер:

```bash
mkdir site && cd site
echo "<h1>Работает</h1>" > index.html
python3 -m http.server 8000
```

Терминал 2 — клиент:

```bash
curl -v http://127.0.0.1:8000/
ss -tulpn | grep 8000
```

Проверить с другой машины: `http://<IP>:8000/`. Если не открывается — файрвол:

```bash
sudo ufw status
sudo ufw allow 8000
```

## Wireshark и tcpdump

```bash
sudo tcpdump -i any -n port 80
sudo tcpdump -i eth0 -n -w capture.pcap
```

Фильтры Wireshark: `ip.addr == 192.168.1.10`, `tcp.port == 443`, `http`,
`dns`, `arp`, `icmp`.

## Что спросят на защите

- Чем коммутатор отличается от маршрутизатора.
- Что такое маска подсети и зачем она.
- Чем TCP отличается от UDP (надёжность, порядок, скорость).
- Что делает DHCP и как выглядит обмен (DISCOVER → OFFER → REQUEST → ACK).
- Как работает DNS-запрос и что такое рекурсия.
- Что произойдёт, если указать неверный шлюз.

## Частые ошибки

| Проблема | Причина | Проверка |
|---|---|---|
| `Network is unreachable` | нет маршрута/шлюза | `ip r` |
| `Temporary failure in name resolution` | DNS не настроен | `cat /etc/resolv.conf`, `dig` |
| `Connection refused` | порт закрыт или служба не запущена | `ss -tulpn` |
| `Connection timed out` | файрвол или неверный IP | `nc -zv`, `ufw status` |
| `Address already in use` | порт занят | `ss -tulpn \| grep :8000` |
| Пинг есть, сайты не открываются | DNS | `ping 8.8.8.8` vs `ping ya.ru` |
| Свой сервер виден только локально | слушает `127.0.0.1` | запускать на `0.0.0.0` |
