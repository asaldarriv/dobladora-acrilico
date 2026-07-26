/*
 * Dobladora automática de acrílico — firmware principal
 * Trabajo de grado, Ingeniería Física, Universidad EAFIT
 *
 * Compilar y cargar con arduino-cli (ver firmware/README.md):
 *   arduino-cli compile --fqbn arduino:avr:mega firmware/dobladora
 *   arduino-cli upload  --fqbn arduino:avr:mega -p COM3 firmware/dobladora
 */

#include "config.h"

enum class Estado : uint8_t {
  REPOSO,
  CALENTANDO,
  SOSTENIENDO,
  PLEGANDO,
  ENFRIANDO,
  FALLA
};

static Estado estado = Estado::REPOSO;

void setup() {
  Serial.begin(SERIAL_BAUD);
  pinMode(PIN_SSR_CALEFACTOR, OUTPUT);
  digitalWrite(PIN_SSR_CALEFACTOR, LOW);
  // TODO: inicializar termopar (MAX31855), driver del motor y pantalla HMI.
}

void loop() {
  switch (estado) {
    case Estado::REPOSO:      /* TODO: esperar parámetros desde la HMI */ break;
    case Estado::CALENTANDO:  /* TODO: lazo PID hasta la consigna      */ break;
    case Estado::SOSTENIENDO: /* TODO: mantener t_sostenimiento        */ break;
    case Estado::PLEGANDO:    /* TODO: ángulo objetivo + springback    */ break;
    case Estado::ENFRIANDO:   /* TODO: enfriar bajo restricción        */ break;
    case Estado::FALLA:       /* TODO: cortar potencia y avisar        */ break;
  }
}
