# Firmware

Código de Arduino de la dobladora. Se compila con [arduino-cli](https://arduino.github.io/arduino-cli/)
para no depender del IDE y poder versionar todo en el repositorio.

```powershell
winget install ArduinoSA.CLI
arduino-cli config init
arduino-cli core update-index
arduino-cli core install arduino:avr

# Compilar y cargar (ajusta el puerto)
arduino-cli compile --fqbn arduino:avr:mega firmware/dobladora
arduino-cli upload  --fqbn arduino:avr:mega -p COM3 firmware/dobladora
```

| Archivo | Contenido |
|---|---|
| `dobladora/dobladora.ino` | Máquina de estados principal |
| `dobladora/config.h` | Pines, consignas y límites de seguridad |

Las constantes de seguridad (`T_MAX_SEGURA_C`, `T_TIMEOUT_MS`) deben quedar
documentadas en el informe final: son parte del argumento de seguridad del equipo.
