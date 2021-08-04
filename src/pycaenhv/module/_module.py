from typing import Any
from ..wrappers import get_crate_map, init_system, deinit_system
from ..enums import CAENHV_SYSTEM_TYPE, LinkType
from ._board import CaenHVBoard


class CaenHVModule:
    """ CAEN Crate module
    """
    def __init__(self):
        self.handle: int = -1
        self.boards = dict()
        self.connected: bool = False

    def __del__(self):
        self.disconnect()

    def is_connected(self) -> bool:
        """ Connection status
        """
        return self.connected

    def connect(self,
                system: str,
                link: str,
                argument: Any,
                user: str = '',
                password: str = '') -> None:
        """ Connect to CAEN HV/LV Module
        """
        system_ = CAENHV_SYSTEM_TYPE[system.upper()]
        link_ = LinkType[link.upper()]
        self.handle = init_system(system_type=system_,
                                  link_type=link_,
                                  argument=argument,
                                  username=user,
                                  password=password)
        # Get crate mapping
        self.mapping = get_crate_map(self.handle)
        for slot, ch_num in enumerate(self.mapping['channels']):
            if ch_num:
                self.boards[slot] = CaenHVBoard(
                    self,
                    slot=slot,
                    num_channels=ch_num,
                    model=self.mapping['models'][slot],
                    serial_number=self.mapping['serial_numbers'][slot],
                    description=self.mapping['descriptions'][slot],
                    firmware_release=self.mapping['firmware_releases'][slot])

        self.connected = True

    def disconnect(self) -> None:
        """ Terminate connection
        """
        if self.connected:
            deinit_system(self.handle)
            self.connected = False