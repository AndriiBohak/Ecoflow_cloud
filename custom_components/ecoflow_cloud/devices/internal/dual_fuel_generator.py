from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity

from custom_components.ecoflow_cloud.api import EcoflowApiClient
from custom_components.ecoflow_cloud.devices import BaseInternalDevice, const
from custom_components.ecoflow_cloud.sensor import (
    InWattsSensorEntity,
    MiscSensorEntity,
    OutWattsSensorEntity,
    RemainSensorEntity,
    StatusSensorEntity,
    TempSensorEntity,
    MilliVoltSensorEntity,
    QuotaStatusSensorEntity,
)
from custom_components.ecoflow_cloud.switch import EnabledEntity


# Generator System Mode Options
GEN_SYS_MODE_OPTIONS = {
    "Off": 0,
    "Manual": 1,
    "Auto": 2,
}

# Generator Motor State Options
GEN_MOTOR_STATE_OPTIONS = {
    "Stopped": 0,
    "Running": 1,
}

# Generator Type Options
GEN_TYPE_OPTIONS = {
    "Unknown": 0,
    "Gasoline": 1,
    "Dual Fuel": 2,
}


class DualFuelGenerator(BaseInternalDevice):
    """EcoFlow Dual Fuel Generator device."""

    def sensors(self, client: EcoflowApiClient) -> list[SensorEntity]:
        return [
            # Power sensors
            OutWattsSensorEntity(client, self, "pd.acPower", const.AC_OUT_POWER),
            OutWattsSensorEntity(client, self, "pd.dcPower", const.DC_OUT_POWER),
            OutWattsSensorEntity(client, self, "pd.totalPower", const.TOTAL_OUT_POWER),
            
            # Voltage sensors
            MilliVoltSensorEntity(client, self, "pd.acVol", const.AC_OUT_VOLT, False),
            MilliVoltSensorEntity(client, self, "pd.dcVol", const.DC_OUT_VOLTAGE, False),
            
            # Current sensors
            MiscSensorEntity(client, self, "pd.acCur", "AC Out Current", "A"),
            MiscSensorEntity(client, self, "pd.dcCur", "DC Out Current", "A"),
            
            # Temperature
            TempSensorEntity(client, self, "pd.temp", const.TEMPERATURE),
            
            # Time sensors
            RemainSensorEntity(client, self, "pd.remainTime", const.REMAINING_TIME),
            MiscSensorEntity(client, self, "pd.motorUseTime", "Motor Use Time", "min"),
            
            # Status sensors
            MiscSensorEntity(client, self, "pd.oilVal", "Oil Level", "%"),
            MiscSensorEntity(client, self, "pd.oilMaxOutPower", const.GEN_MAX_OUTPUT_POWER, "W"),
            
            # State sensors
            MiscSensorEntity(client, self, "pd.acState", "AC Output State", None),
            MiscSensorEntity(client, self, "pd.dcState", "DC Output State", None),
            MiscSensorEntity(client, self, "pd.motorState", "Motor State", None),
            MiscSensorEntity(client, self, "pd.sysMode", "System Mode", None),
            
            # Misc sensors
            MiscSensorEntity(client, self, "pd.cellId", "Cell ID", None),
            MiscSensorEntity(client, self, "pd.type", "Generator Type", None),
            MiscSensorEntity(client, self, "pd.num", "Unit Number", None),
            MiscSensorEntity(client, self, "pd.errCode", const.ERROR_CODE, None),
            
            # Status sensor
            self._status_sensor(client),
        ]

    def numbers(self, client: EcoflowApiClient) -> list[NumberEntity]:
        return [
            # Add number entities here when control commands are discovered
            # Example:
            # ChargingPowerEntity(
            #     client,
            #     self,
            #     "pd.oilMaxOutPower",
            #     const.GEN_MAX_OUTPUT_POWER,
            #     200,
            #     1800,
            #     lambda value: {
            #         "moduleType": 1,
            #         "operateType": "setMaxPower",
            #         "params": {"maxPower": int(value)}
            #     },
            # ),
        ]

    def switches(self, client: EcoflowApiClient) -> list[SwitchEntity]:
        return [
            EnabledEntity(
                client,
                self,
                "pd.motorState",
                "Generator Motor",
                lambda value: {
                    "moduleType": 2,
                    "operateType": "motorCtrl",
                    "params": {"enable": value}
                },
            ),
        ]

    def selects(self, client: EcoflowApiClient) -> list[SelectEntity]:
        return [
            # Add select entities here when control commands are discovered
            # Example:
            # DictSelectEntity(
            #     client,
            #     self,
            #     "pd.sysMode",
            #     "System Mode",
            #     GEN_SYS_MODE_OPTIONS,
            #     lambda value: {
            #         "moduleType": 1,
            #         "operateType": "sysMode",
            #         "params": {"mode": value}
            #     },
            # ),
        ]

    def _status_sensor(self, client: EcoflowApiClient) -> StatusSensorEntity:
        return QuotaStatusSensorEntity(client, self)
