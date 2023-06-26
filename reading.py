from dataclasses import dataclass 

@dataclass(slots=True)
class Readings:
    dev_serial: str
    custom_name: str
    ch_num: str
    ch_type: str
    subch_type: str
    data_value: str
    units: str
    hardware_name: str = None
    installation_id: str = None
    received_datetime: str = None
    posted: str = None


    def __post_init__(self) -> None: 
        """create the hardware_name fields by mapping all the numbers to 
        their equivalent current value in the SQL"""
        
        if self.ch_num == "S11":
            self.hardware_name = "Sensor (S11)"
        elif self.ch_num == "S12":
            self.hardware_name = "Sensor Temperature (S12)"
        elif self.ch_num == "S21":
            self.hardware_name = "Sensor (S21)"
        elif self.ch_num == "S22":
            self.hardware_name = "Sensor Temperature (S22)"
        elif self.ch_num == "D1":
            if self.subch_type == "TOTAL":
                self.hardware_name = "FlowMeter Total (D1)"
            else:
                self.hardware_name = "FlowMeter Rate (D1)"
        elif self.ch_num == "D2":
            self.hardware_name = "Generic (D3)"
        elif self.ch_num == "D3":
            if self.subch_type == "TOTAL":
                self.hardware_name = "FlowMaster Total (D2)"
            else:
                self.hardware_name = "FlowMaster Rate (D2)"
        elif self.ch_num == "D4":
            self.hardware_name = "Generic (D4)"

    
    def set_install_id(self, installation_id) -> None:
        """Set the installation ID for the dataclass"""
        self.installation_id = installation_id


    def set_received_datetime(self, time) -> None:
        self.received_datetime = time

    def set_posted(self, time) -> None:
        self.posted = time 
