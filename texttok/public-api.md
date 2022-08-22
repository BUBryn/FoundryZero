# texttok - Public API

## Actions

### Get recent IDs

Returns the ID of a recent tox that you might like

### Get tox

Return the tox specified by an ID

### Rate tox

Thumbs up or thumbs down on a specified tox

## Protocol

The texttok protocol uses binary data over a TCP socket. All values are little-endian.

--- 
### Client request: Get recent Tox ID

| Component | Description | Size in bytes |
| --- | --- | -- |
| Message type | The value 1 | 1 |

---
### Server response: Recent Tox ID

| Component | Description | Size in bytes |
| --- | --- | -- |
| Message type | The value 64 | 1 |
| Tox ID | ID of a recent Tox | 4 |

---
### Client request: Get tox

| Component | Description | Size in bytes |
| --- | --- | -- |
| Message type | The value 2 | 1 |
| Tox ID | The ID of the tox to retrieve | 4 |

---
### Server response: Tox

| Component | Description | Size in bytes |
| --- | --- | -- |
| Message type | The value 65 | 1 |
| Tox size | Size in bytes of the Tox data | 4 |
| Tox data | The contents of the Tox, encoded as UTF-8 | Tox size |

---
### Client request: Rate tox

| Component | Description | Size in bytes |
| --- | --- | -- |
| Message type | The value 3 | 1 |
| Tox ID | The ID of the tox to rate | 4 |
| Rating | Give the Tox a thumbs up (1) or thumbs down (255) | 1 |

---
### Server response: Tox rating confirmation

| Component | Description | Size in bytes |
| --- | --- | -- |
| Message type | The value 66 | 1 |
| Tox rating | The new rating of the Tox | 4 |

---
### Server response: Error

| Component | Description | Size in bytes |
| --- | --- | -- |
| Message type | The value 255 | 1 |
