import logging

# suppress logging output unless a higher-level logger wants it
logging.getLogger("hass_mqtt").addHandler(logging.NullHandler())
