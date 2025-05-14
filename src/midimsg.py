import datetime
from enum import Enum, auto
from typing import Self
from helpers import Helpers
from midi_enum import *


class MidiMsg:
    """ Category |        msg type          |        parameters
        CVM      | NoteOff                  | channel, note, velocity
        CVM      | NoteOn                   | channel, note, velocity
        CVM      | PolyphonicKeyPressure    | channel, note, velocity
        CC       | CtrlChangeOrChannelMode  | channel, control_change, value
        CM       | CtrlChangeOrChannelMode  | channel, channel_mode, value
        CVM      | ProgramChange            | channel, value
        CVM      | ChannelPressure          | channel, value
        CVM      | PitchBendChange          | channel, value
        SCM      | SystemExclusive          | sys_ex_type, sys_ex_data
                                            | if Non real-time : sys_ex_dev_id, sys_ex_type_data, sys_ex_nrt
                                            | if Real-time     : sys_ex_dev_id, sys_ex_type_data, sys_ex_rt
                                            | if Specific      : sys_ex_manufacturer
        SCM      | MidiTimeCodeQuarterFrame | value
        SCM      | SongPositionPointer      | value
        SCM      | SongSelect               | value
        SCM      | TuneRequest              | 
        RTM      | TimingClock              | 
        RTM      | Start                    | 
        RTM      | Continue                 | 
        RTM      | Stop                     | 
        RTM      | ActiveSensing            | 
    """
    def __init__(self):
        self.bytes:list[int] = []
        self.category:MsgCategory = None
        self.type:(ChannelMsg | SystemCommonMsg | RealTimeMsg) = None
        self.note:int = -1
        self.channel:int = -1
        self.velocity:int = -1
        self.control_change:ControlChange = None
        self.channel_mode:ControlChange = None
        self.value:int = -1
        self.sys_ex_type:str = ''
        self.sys_ex_data:int = []
        self.sys_ex_type_data = None
        self.sys_ex_manufacturer:Manufacturer = None
        self.sys_ex_dev_id:int = -1
        self.sys_ex_nrt:NRTSysEx = None
        self.sys_ex_rt:RTSysEx = None

    def from_list(msg:list[int])->Self:
        res:MidiMsg = MidiMsg()
        size = len(msg)
        invalid_data = True
        if size>0:
            res.bytes = msg
            MSB = (msg[0]>>4)&0xF
            LSB = msg[0]&0xF
            if MidiMsg.__has_value(ChannelMsg, MSB):
                res.category = MsgCategory.CVM
                res.type = ChannelMsg(MSB)
                res.channel = LSB                
                if res.type==ChannelMsg.NoteOff or res.type==ChannelMsg.NoteOn or res.type==ChannelMsg.PolyphonicKeyPressure:
                    if size==3:
                        res.note = msg[1]
                        res.velocity = msg[2]
                        invalid_data = False
                
                elif res.type==ChannelMsg.CtrlChangeOrChannelMode:
                    if size==3:
                        if msg[1]<120 and msg[1] in ControlChange:
                            res.category = MsgCategory.CC
                            res.control_change = ControlChange(msg[1])
                            if msg[2]<128:
                                res.value = msg[2]
                                invalid_data = False
                        elif msg[1]>=120 and msg[1] in ChannelMode:
                            res.category = MsgCategory.CM
                            res.channel_mode = ChannelMode(msg[1])
                            if msg[2]<128:
                                res.value = msg[2]
                                invalid_data = False
                                
                elif res.type==ChannelMsg.ProgramChange or res.type==ChannelMsg.ChannelPressure:
                    if size==2:
                        res.value = msg[1]
                        invalid_data = False
                        
                elif res.type==ChannelMsg.PitchBendChange:
                    if size==3:
                        res.value = (msg[2]<<7)+msg[1]
                        invalid_data = False
                
            elif MidiMsg.__has_value(SystemCommonMsg, msg[0]):
                res.category = MsgCategory.SCM
                res.type = SystemCommonMsg(msg[0])
                if res.type==SystemCommonMsg.SystemExclusive:
                    if size>2 and (msg[len(msg)-1] == SystemCommonMsg.EndOfExclusive.value):
                        # url : https://encyclopedia.pub/entry/34593
                        # Start of SysEx is followed by either a Manufacturer ID byte, or three Manufacturer ID bytes when the first byte is zero:
                        # F0 <ID number> <data Bytes>... F7
                        # F0 00 <ID number> <ID number> <data Bytes>... F7
                        # ID number and data bytes use 7-bit values and their high bit is always set to 0.
                        # Universal System Exclusive messages are formed from Manufacturer ID number 0x7E for non-realtime and 0x7F for realtime messages, a SysEx 'Device ID' (SysEx 'channel' set in each instrument's settings) or 0x7F to broadcast to all devices, then one or two Sub-ID bytes to indicate function then data bytes:
                        # F0 <7E or 7F> <device ID> <sub ID#1> ... <data Bytes> ... F7

                        id = None
                        pos = 2
                        if msg[1]==0:
                            id = (0, msg[2], msg[3])
                            pos = 4
                        elif msg[1] != 0x7E and msg[1] != 0x7F:
                            id = (msg[1])
                        if id:
                            if id in Manufacturer:
                                res.sys_ex_manufacturer = Manufacturer(id)
                            else:
                                res.sys_ex_manufacturer = Manufacturer.Unknown
                        
                        if msg[1] == 0x7E or msg[1] == 0x7F:
                            if size>4:
                                res.sys_ex_dev_id = msg[2]
                                sub_id1 = msg[3]
                                pos = 4
                                if msg[1] == 0x7E: # Non real-time message
                                    res.sys_ex_type = 'NRT'
                                    if (sub_id1) in NRTSysEx:
                                        res.sys_ex_nrt = NRTSysEx((sub_id1))
                                        res.sys_ex_type_data = (sub_id1)
                                    elif (sub_id1, msg[4]) in NRTSysEx:
                                        res.sys_ex_nrt = NRTSysEx((sub_id1, msg[4]))
                                        res.sys_ex_type_data = (sub_id1, msg[4])
                                        pos = 5
                                    elif (sub_id1, 0xFF) in NRTSysEx:
                                        res.sys_ex_nrt = NRTSysEx((sub_id1, 0xFF))
                                        res.sys_ex_type_data = (sub_id1, msg[4])
                                        pos = 5
                                    else:
                                        res.sys_ex_nrt = NRTSysEx.Unknown
                                        res.sys_ex_type_data = (sub_id1)
                                if msg[1] == 0x7F: # Real-time message
                                    res.sys_ex_type = 'RT'
                                    if (sub_id1) in RTSysEx:
                                        res.sys_ex_nrt = RTSysEx((sub_id1))
                                        res.sys_ex_type_data = (sub_id1)
                                    elif (sub_id1, msg[4]) in RTSysEx:
                                        res.sys_ex_nrt = RTSysEx((sub_id1, msg[4]))
                                        res.sys_ex_type_data = (sub_id1, msg[4])
                                        pos = 5
                                    elif (sub_id1, 0xFF) in RTSysEx:
                                        res.sys_ex_nrt = RTSysEx((sub_id1, 0xFF))
                                        res.sys_ex_type_data = (sub_id1, msg[4])
                                        pos = 5
                                    else:
                                        res.sys_ex_nrt = RTSysEx.Unknown
                                        res.sys_ex_type_data = (sub_id1)
                                invalid_data = False
                        else:
                            # Manufacturer specific message
                            res.sys_ex_type = 'MS'
                            invalid_data = False
                        res.sys_ex_data = msg[pos:len(msg)-1]
                        
                elif size>1 and res.type==SystemCommonMsg.MidiTimeCodeQuarterFrame:
                    # Spec is unclear ... TBD
                    res.value = msg[1]
                    invalid_data = False
                elif size==3 and res.type==SystemCommonMsg.SongPositionPointer:
                    res.value = (msg[2]<<7)+msg[1]
                    invalid_data = False
                elif size==2 and res.type==SystemCommonMsg.SongSelect:
                    res.value = msg[1]
                    invalid_data = False
                elif size==1 and res.type==SystemCommonMsg.TuneRequest:
                    invalid_data = False

            elif MidiMsg.__has_value(RealTimeMsg, msg[0]):
                res.category = MsgCategory.RTM
                res.type = RealTimeMsg(msg[0])
                if size==1 and (
                    res.type==RealTimeMsg.TimingClock or
                    res.type==RealTimeMsg.Start or
                    res.type==RealTimeMsg.Continue or
                    res.type==RealTimeMsg.Stop or
                    res.type==RealTimeMsg.ActiveSensing or
                    res.type==RealTimeMsg.Reset):
                    invalid_data = False
            
            else:
                return None
    
        if invalid_data:
            return None

        return res
    
    def to_raw_string(self, hexa:bool = False)->str:
        return '[' + ', '.join(Helpers.int_to_str(x,hexa) for x in self.bytes) + ']'
    
    def to_string(self, hexa:bool = False)->str:
        data_str:list = []
        
        if isinstance(self.type, ChannelMsg):
            data_str.append(MidiMsg.__enum2str(ChannelMsg(self.type),hexa))
            data_str.append('channel:' + Helpers.int_to_str(self.channel+1, hexa))
            if self.type==ChannelMsg.NoteOff or self.type==ChannelMsg.NoteOn or self.type==ChannelMsg.PolyphonicKeyPressure:
                data_str.append('note:'+MidiMsg.note_to_string(self.note)+'('+Helpers.int_to_str(self.note,hexa)+')')
                data_str.append('velocity:' + Helpers.int_to_str(self.velocity,hexa))
            elif self.type==ChannelMsg.CtrlChangeOrChannelMode:
                if self.control_change:
                    data_str[0] = MidiMsg.__enum2str(ControlChange(self.control_change),hexa)
                    data_str.append(Helpers.int_to_str(self.value,hexa))
                elif self.channel_mode:
                    data_str[0] = MidiMsg.__enum2str(ChannelMode(self.channel_mode),hexa)
                    data_str.append(Helpers.int_to_str(self.value,hexa))
            elif self.type==ChannelMsg.ProgramChange or self.type==ChannelMsg.ChannelPressure or self.type==ChannelMsg.PitchBendChange:
                data_str.append(Helpers.int_to_str(self.value,hexa))
        
        elif isinstance(self.type, SystemCommonMsg):
            data_str.append(MidiMsg.__enum2str(SystemCommonMsg(self.type),hexa))
            if self.type==SystemCommonMsg.SystemExclusive:
                if self.sys_ex_type=='MS':
                    manufacturer = ''.join([Helpers.hex_to_str(i,pref='',suff='') for i in self.sys_ex_manufacturer.value])
                    data_str.append('manufacturer:'+MidiMsg.__enum2str(self.sys_ex_manufacturer,hexa,False)+'("'+manufacturer+'")')
                else:
                    data_str.append(self.sys_ex_type)
                    data_str.append('device:'+('ALL' if self.sys_ex_dev_id==0x7F else Helpers.int_to_str(self.sys_ex_dev_id,hexa)))
                    if self.sys_ex_type=='NRT':
                        data_str.append(MidiMsg.__enum2str(self.sys_ex_nrt,hexa,False)+'('+','.join([Helpers.int_to_str(i,hexa) for i in self.sys_ex_type_data])+')')
                    elif self.sys_ex_type=='RT':
                        data_str.append(MidiMsg.__enum2str(self.sys_ex_rt,hexa,False)+'('+','.join([Helpers.int_to_str(i,hexa) for i in self.sys_ex_type_data])+')')
                data_str.append('data:'+'['+','.join([Helpers.int_to_str(i,hexa) for i in self.sys_ex_data])+']')
            else:
                data_str.append('value:'+Helpers.int_to_str(self.value,hexa))
        
        elif isinstance(self.type, RealTimeMsg):
             data_str.append(MidiMsg.__enum2str(RealTimeMsg(self.type),hexa))
        
        data_str[0] = MidiMsg.__enum2str(MsgCategory(self.category),hexa,False) + '.' + data_str[0]
        return '['+', '.join(data_str)+']'
    
    __notes_str = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    def note_to_string(value:int, err_str:str = 'invalid note')->str:
            if value>127:
                return err_str
            note = value%12
            octave = value//12
            return MidiMsg.__notes_str[note]+str(octave+1)
    
    def __has_value(enum, value)->bool:
        return value in enum._value2member_map_     
    def __enum2str(enumvalue, hexa:bool,add_value:bool=True)->str:
        if add_value:
            return str(enumvalue).split('.')[1]+'('+Helpers.int_to_str(enumvalue.value,hexa)+')'
        else:
            return str(enumvalue).split('.')[1]



class Filter:
    def __init__(self):
        self.inclusive:bool = True
        self.types:list = []
        self.velocity_min:int = 0
        self.velocity_max:int = 127		
        self.channel_min:int = 0
        self.channel_max:int = 15

class Rule:
    def __init__(self):
        self.inports = []
        self.filters:list[list[Filter]] = []