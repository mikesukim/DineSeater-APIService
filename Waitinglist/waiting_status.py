from enum import Enum
class WaitingStatus(Enum):
    WAITING = 'waiting'
    TEXT_SENT = 'text_sent'
    ARRIVED = 'arrived'
    MISSED = 'missed'
