#pragma once
#include <Arduino.h>

// ---- Comunicación ----
constexpr uint32_t SERIAL_BAUD = 115200;

// ---- Pines ----
constexpr uint8_t PIN_SSR_CALEFACTOR = 8;   // relé de estado sólido
constexpr uint8_t PIN_TERMOPAR_CS    = 10;  // MAX31855 (SPI)
constexpr uint8_t PIN_MOTOR_STEP     = 4;
constexpr uint8_t PIN_MOTOR_DIR      = 5;
constexpr uint8_t PIN_MOTOR_ENABLE   = 6;
constexpr uint8_t PIN_PARO_EMERGENCIA = 2;  // interrupción externa

// ---- Límites de seguridad ----
constexpr float T_MAX_SEGURA_C   = 200.0f;  // corte por sobretemperatura
constexpr float T_CONSIGNA_C     = 155.0f;  // ventana de conformado del PMMA
constexpr uint32_t T_TIMEOUT_MS  = 600000;  // 10 min sin alcanzar consigna -> falla

// ---- Especificaciones objetivo ----
constexpr float ESPESOR_MIN_MM   = 3.0f;
constexpr float ESPESOR_MAX_MM   = 6.0f;
constexpr float ANGULO_MAX_DEG   = 120.0f;
constexpr float LONGITUD_MAX_MM  = 250.0f;
