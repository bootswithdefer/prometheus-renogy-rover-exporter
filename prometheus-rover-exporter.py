#!/usr/bin/python3
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from prometheus_client import start_http_server, Gauge
import time

g_state_of_charge = Gauge("renogy_rover_state_of_charge", "Percent state of charge")
g_battery_voltage = Gauge("renogy_rover_battery_voltage", "")

g_solar_voltage = Gauge("renogy_rover_solar_voltage", "Solar volage")
g_solar_power = Gauge("renogy_rover_solar_power", "Solar power in watts")
g_solar_current = Gauge("renogy_rover_solar_current", "Solar current in amps")

g_charge_power = Gauge("renogy_rover_charge_power", "Charge power in watts")
g_charge_current = Gauge("renogy_rover_charge_current", "Charge current in amps")
g_charging_state = Gauge("renogy_rover_charging_state", "Charging state")


def get_rover_metrics():
    client = ModbusClient(
        method="rtu",
        port="/dev/ttyUSB0",
        baudrate=9600,
        stopbits=1,
        bytesize=8,
        parity="N",
        retries=15,
    )
    client.connect()

    SOC = client.read_holding_registers(0x100, 2, unit=1)
    g_state_of_charge.set(SOC.registers[0])

    BatVolt = client.read_holding_registers(0x101, 1, unit=1)
    g_battery_voltage.set(float(BatVolt.registers[0] * 0.1))

    # Temps = client.read_holding_registers(0x103, 2, unit=1)
    # controllerTemp = Temps.registers[0]
    # batteryTemp = Temps.registers[1]

    PanelVolt = client.read_holding_registers(0x107, 1, unit=1)
    g_solar_voltage.set(float(PanelVolt.registers[0] * 0.1))

    PanelCurrent = client.read_holding_registers(0x108, 1, unit=1)
    g_solar_current.set(float(PanelCurrent.registers[0] * 0.01))

    ChargeWatts = client.read_holding_registers(0x109, 1, unit=1)
    g_charge_power.set(ChargeWatts.registers[0])

    ChargeCurrent = client.read_holding_registers(0x102, 1, unit=1)
    g_charge_current.set(float(ChargeCurrent.registers[0] * 0.01))

    PanelWatts = client.read_holding_registers(0x109, 1, unit=1)
    g_solar_power.set(PanelWatts.registers[0])

    ChargingState = client.read_holding_registers(0x120, 1, unit=1)
    g_charging_state.set(ChargingState.registers[0])


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(9732)
    # Generate some requests.
    while True:
        get_rover_metrics()
        time.sleep(10)
