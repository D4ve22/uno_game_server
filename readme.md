# Uno GameServer – Client API & WebSocket Dokumentation

Diese Dokumentation beschreibt, wie ein Client mit dem Uno-GameServer kommunizieren kann. Sie umfasst sowohl die **REST-API** (z. B. Karten abfragen, spielen, ziehen) als auch die **WebSocket-Schnittstelle** für Events wie `"your_turn"`, `"card_played"` etc.

---

## Überblick

- Pro Spiel gibt es genau **zwei Spieler**
- Der Server verwaltet **genau ein Spiel zurzeit**
- Kommunikation erfolgt über:
  - **REST-API**: Spieleraktionen (Karte spielen, ziehen, Hand anzeigen)
  - **WebSocket**: Asynchrone Benachrichtigungen und Spielfluss

---

## WebSocket: `/ws/{player_name}`

### Verbindung herstellen

```
URL:       ws://<host>/ws/{player_name}
Methode:   WebSocket
```

| Parameter     | Typ     | Beschreibung                     |
|---------------|---------|----------------------------------|
| `player_name` | string  | Gewünschter Name des Spielers    |

> **Hinweis**: Der Spieler erhält eine eindeutige ID per Event `"join_success"`.

---

### WebSocket-Events (vom Server gesendet)

| Event-Name        | Beschreibung                                        | Datenformat (`data`)                                 |
|-------------------|-----------------------------------------------------|-------------------------------------------------------|
| `join_success`    | Spieler erfolgreich beigetreten                     | `{ "id": "<player_id>" }`                            |
| `name_already_in_use` | Spielername ist bereits vergeben              | `{}`                                                  |
| `join_failed_game_full` | Es sind bereits 2 Spieler verbunden          | `{}`                                                  |
| `player_joined`   | Anderer Spieler ist dem Spiel beigetreten          | `{ "player_name": "<name>" }`                         |
| `game_started`    | Das Spiel wurde gestartet                           | `{}`                                                  |
| `your_turn`       | Du bist am Zug                                      | `{ "action": null | "+2" | "+4" | "skip" }`          |
| `card_played`     | Ein Spieler hat eine Karte gespielt                 | `{ "player": "<name>", "card": { "color": "...", "value": "..." }}` |
| `card_drawn`      | Ein Spieler hat eine Karte gezogen                  | `{ "player": "<name>" }`                              |
| `uno_called`      | Ein Spieler hat nur noch eine Karte                 | `{ "player": "<name>" }`                              |
| `game_won`        | Ein Spieler hat gewonnen                            | `{ "winner": "<name>" }`                              |
| `player_left`     | Ein Spieler hat das Spiel verlassen                 | `{ "player_id": "<id>" }`                             |

> Alle Events werden als JSON gesendet:  
```json
{
  "event": "event_name",
  "data": { ... }
}
```

---

## REST API

Base-URL: `http://<host>/`

### 1. Handkarten abfragen

```
GET /hand/{player_id}
```

| Parameter    | Typ     | Beschreibung          |
|--------------|---------|-----------------------|
| `player_id`  | string  | Spieler-ID (aus WebSocket) |

#### Antwort:
```json
{
  "hand": [
    { "color": "red", "value": "7" },
    { "color": "blue", "value": "+2" },
    ...
  ]
}
```

#### Fehler:
```json
{ "error": "player_not_found" }
```

---

### 2. Karte spielen

```
GET /play/{player_id}/{color}/{value}
```

| Parameter    | Typ     | Beschreibung                    |
|--------------|---------|---------------------------------|
| `player_id`  | string  | Spieler-ID                      |
| `color`      | string  | Kartfarbe (z. B. `"red"`)       |
| `value`      | string  | Kartenwert (z. B. `"7"`, `"+2"`, `"skip"`) |

#### Antwort:
```json
{ "status": "Card played" }
```

#### Fehler:
```json
{ "error": "not_your_turn" }
{ "error": "invalid_move" }
{ "error": "card_not_valid" }
```

---

### 3. Karte ziehen

```
GET /draw/{player_id}
```

| Parameter    | Typ     | Beschreibung     |
|--------------|---------|------------------|
| `player_id`  | string  | Spieler-ID       |

#### Antwort:
```json
{
  "card": { "color": "yellow", "value": "5" }
}
```

#### Fehler:
```json
{ "error": "not_your_turn" }
{ "error": "no_card_drawn" }
```

---

### 4. Spielzustand abfragen

```
GET /state
```

#### Beispielantwort:
```json
{
  "players": ["Alice", "Bob"],
  "current_player": "Alice",
  "discard_top": { "color": "green", "value": "9" },
  "started": true
}
```

---

## Kartenformate

- Farben (`color`): `"red"`, `"blue"`, `"green"`, `"yellow"`, `"black"`
- Werte (`value`): `"0"` – `"9"`, `"skip"`, `"+2"`, `"+4"`

> **Hinweis**: `"black"` ist für Karten wie `+4`, falls später `"wild"` etc. unterstützt werden.

---

## Hinweise für Client-Entwickler

- Nach erfolgreicher WebSocket-Verbindung immer auf `join_success` warten, um die Spieler-ID zu speichern.
- WebSocket ist **verbindlich**, um über den Spielverlauf informiert zu bleiben (z. B. `"your_turn"`, `"card_played"`).
- Alle Spielaktionen laufen über die **REST-API**, nicht über den WebSocket.
- Das Spiel startet automatisch, wenn zwei Spieler beigetreten sind.
- Wenn ein Spieler das Spiel verlässt, gewinnt der verbleibende Spieler automatisch.

---

## Beispielablauf

1. **Client A**: Verbindet sich mit `/ws/Alice`
2. **Client B**: Verbindet sich mit `/ws/Bob`
3. Server sendet `join_success` an beide + `game_started`
4. `your_turn` wird an den ersten Spieler gesendet
5. Spieler ruft `/hand/{id}` auf
6. Spielzug: `/play/{id}/red/5`
7. WebSocket-Broadcast: `card_played`, ggf. `your_turn` an Gegner