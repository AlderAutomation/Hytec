from dataclasses import dataclass 

@dataclass(slots=True)
class Readings:
    dev_serial: int
    custom_name: str
    ch_num: str
    ch_type: str
    subch_type: str
    data_value: str
    units: str

    """ 
    TODO need to create the hardware_name fields by mapping all the numbers to 
    their equivalent current value in the SQL

    """