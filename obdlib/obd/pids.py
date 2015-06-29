# Information about OBD-II PIDs
# http://en.wikipedia.org/wiki/OBD-II_PIDs

# PID hex codes
PIDS_SUPPORTED_00_20 = "00"
MONITOR_STATUS_SINCE_DTC_CLEARED = "01"
FREEZE_DTC = "02"
VEHICLE_IDENTIFICATION_NUMBER = "02"
FUEL_SYSTEM_STATUS = "03"
CALCULATED_ENGINE_LOAD = "04"
ENGINE_COOLANT_TEMPERATURE = "05"
SHORT_TERM_FUEL_TRIM_BANK_1 = "06"
LONG_TERM_FUEL_TRIM_BANK_1 = "07"
SHORT_TERM_FUEL_TRIM_BANK_2 = "08"
LONG_TERM_FUEL_TRIM_BANK_2 = "09"
FUEL_PRESSURE = "0A"
ECU_NAME = "0A"
INTAKE_MANIFOLD_PRESSURE = "0B"
ENGINE_RPM = "0C"
VEHICLE_SPEED = "0D"
TIMING_ADVANCE = "0E"
INTAKE_AIR_TEMPERATURE = "0F"
MAF_AIR_FLOW = "10"
THROTTLE_POSITION = "11"

# TODO: Oxygen sensors

AUXILIARY_INPUT_STATUS = "1E"
ENGINE_RUN_TIME_SINCE_START = "1F"
PIDS_SUPPORTED_21_40 = "20"
DISTANCE_TRAVELED_WITH_MIL_ON = "21"

FUEL_RAIL_PRESSURE = "23"

COMMANDED_EGR = "2C"
EGR_ERROR = "2D"
COMMANDED_EVAPORATIVE_PURGE = "2E"
FUEL_LEVEL_INPUT = "2F"
DISTANCE_TRAVELED_SINCE_CODES_CLEARED = "31"
EVAP_SYSTEM_VAPOR_PRESSURE = "32"
BAROMETRIC_PRESSURE = "33"

PIDS_SUPPORTED_41_60 = "40"
CONTROL_MODULE_VOLTAGE = "41"
ABSOLUTE_LOAD_VALUE = "42"
AMBIENT_AIR_TEMPERATURE = "46"

TIME_RUN_WITH_MIL_ON = "4D"
TIME_SINCE_TROUBLE_CODES_CLEARED = "4E"

FUEL_TYPE = "51"
ETHANOL_FUEL_PERCENTAGE = "52"

RELATIVE_ACCELERATOR_PEDAL_POSITION = "5A"
HYBRID_BATTERY_PACK_REMAINING_LIFE = "5B"
ENGINE_OIL_TEMPERATURE = "5C"
FUEL_INJECTION_TIMING = "5D"
ENGINE_FUEL_RATE = "5E"

PIDS_SUPPORTED_61_80 = "60"
ENGINE_PERCENT_TORQUE = "64"

# TODO: remaining PIDs

# Mode 01 PID 51 returns a value for the vehicle's fuel type

FUEL_TYPE_DESCRIPTION = (
    'Not Available',
    'Gasoline',
    'Methanol',
    'Ethanol',
    'Diesel',
    'Liquefied petroleum gas (LPG)',
    'Compressed natural gas (CNG)',
    'Propane',
    'Electric',
    'Bifuel running Gasoline',
    'Bifuel running Methanol',
    'Bifuel running Ethanol',
    'Bifuel running Liquefied petroleum gas (LPG)',
    'Bifuel running Compressed natural gas (CNG)',
    'Bifuel running Propane',
    'Bifuel running Electricity',
    'Bifuel running electric and combustion engine',
    'Hybrid gasoline',
    'Hybrid Ethanol',
    'Hybrid Diesel',
    'Hybrid Electric',
    'Hybrid running electric and combustion engine',
    'Hybrid Regenerative',
    'Bifuel running diesel'
)

# Mode 01 PID 12 returns a single byte of data which describes the secondary air status.
SECONDARY_AIR_STATUS = {
    1: 'Upstream',
    2: 'Downstream of catalytic converter',
    4: 'From the outside atmosphere or off',
    8: 'Pump commanded on for diagnostics',
}

# Mode 01 PID 1C returns a single byte of data which describes which OBD standards.
OBD_STANDARDS = (
    'OBD-II as defined by the CARB',
    'OBD as defined by the EPA',
    'OBD and OBD-II',
    'OBD-I',
    'Not OBD compliant',
    'EOBD (Europe)',
    'EOBD and OBD-II',
    'EOBD and OBD',
    'EOBD, OBD and OBD II',
    'JOBD (Japan)',
    'JOBD and OBD II',
    'JOBD and EOBD',
    'JOBD, EOBD, and OBD II',
    'Reserved',
    'Reserved',
    'Reserved',
    'Engine Manufacturer Diagnostics (EMD)',
    'Engine Manufacturer Diagnostics Enhanced (EMD+)',
    'Heavy Duty On-Board Diagnostics (Child/Partial) (HD OBD-C)',
    'Heavy Duty On-Board Diagnostics (HD OBD)',
    'World Wide Harmonized OBD (WWH OBD)',
    'Reserved',
    'Heavy Duty Euro OBD Stage I without NOx control (HD EOBD-I)',
    'Heavy Duty Euro OBD Stage I with NOx control (HD EOBD-I N)',
    'Heavy Duty Euro OBD Stage II without NOx control (HD EOBD-II)',
    'Heavy Duty Euro OBD Stage II with NOx control (HD EOBD-II N)',
    'Reserved',
    'Brazil OBD Phase 1 (OBDBr-1)',
    'Brazil OBD Phase 2 (OBDBr-2)',
    'Korean OBD (KOBD)',
    'India OBD I (IOBD I)',
    'India OBD II (IOBD II)',
    'Heavy Duty Euro OBD Stage VI (HD EOBD-IV)'
)
