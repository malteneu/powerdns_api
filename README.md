# PowerDNS Api

The Class will help you create Templates and quickly add, edit and remove Zones and Records

# Usage

Follow instructions these Instruczions to enable your API:
https://doc.powerdns.com/authoritative/http-api/index.html#enabling-the-api 

Also add the default SOA Record Values in your PDNS Config file (the create_soa_record functions is not being parsed correctly at the moment)

Add your API Endpoint and your Secret Key when Initliazing PowerDnsClient and edit Zones and Records as you wish!

Server ID will most likely be localhost
Always hand over FQDN into functions (with an extra . at the end)
