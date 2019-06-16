# cdp_interface_populate
Populates CDP information on interface for IOS

This script has not current logic applied so it might freak out when it finds multiple entries on a single interface (in rare scenarios I suppose...)

## How to use

main.py [IP] [USERNAME] [PASSWORD] [SECRET]

Example:
main.py 10.198.211.34 someUser somePassword someEnableSecret

### Output Example:

Found CDP Entry: FLAT-RTR01.W17BS.co.uk on interface GigabitEthernet1/0/12
FLAT-SW01(config)#interface GigabitEthernet1/0/12
FLAT-SW01(config-if)#description ** Link to FLAT-RTR01.W17BS.co.uk (GigabitEthernet0/0) **

Found CDP Entry: FLAT-RTR01.W17BS.co.uk on interface GigabitEthernet1/0/13
FLAT-SW01(config)#interface GigabitEthernet1/0/13
FLAT-SW01(config-if)#description ** Link to FLAT-RTR01.W17BS.co.uk (GigabitEthernet0/1) **

Found CDP Entry: w17bsise01 on interface GigabitEthernet1/0/14
FLAT-SW01(config)#interface GigabitEthernet1/0/14
FLAT-SW01(config-if)#description ** Link to w17bsise01 (eth0) **
