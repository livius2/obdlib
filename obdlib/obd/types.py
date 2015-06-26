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