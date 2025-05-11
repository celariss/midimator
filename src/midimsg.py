import datetime
from enum import Enum, auto
from typing import Self
from helpers import Helpers


# source : https://midi.org/spec-detail
# MIDI 1.0 message format :
#	[Status, Data1, Data2, ...]
# A message can be either :
# - a channel message (see ChannelMsg below),
# - a system Common or Real-Time Messages (see SystemCommonMsg below),
# (depending on the "Status" : first byte)

# Channel Voice/Mode messages enumeration
# Status byte :
#	Bits 7-4 : Event (see enumeration values below)
#	Bits 3-0 : Channel (0-15)
class ChannelMsg(Enum):
    # Data1 : 7=0, [6-0] key note number
    # Data2 : 7=0, [6-0] velocity
    NoteOff = 0x8
    # Data1 : 7=0, [6-0] key note number
    # Data2 : 7=0, [6-0] velocity
    NoteOn  = 0x9
    # Data1 : 7=0, [6-0] key note number
    # Data2 : 7=0, [6-0] velocity
    PolyphonicKeyPressure = 0x0A
    # Data1 : 7=0, [6-0] controller number
    # Data2 : 7=0, [6-0] controller value
    # if controller number < 120, it's a ControlChange message :
    #   This message is sent when a controller value changes
    #   Controllers include devices such as pedals and levers
    #   Compare Data1 to ControlChange enum to get exact message
    # if controller number is in [120,127], it's a Channel Mode Message :
    #   Compare Data1 to ChannelMode enum to get exact message
    CtrlChangeOrChannelMode = 0X0B
    # This message sent when the patch number changes
    # Data1 : 7=0, [6-0] new program number
    ProgramChange = 0x0C
    # Channel Pressure (After-touch). This message is most often sent by pressing down on the key after it “bottoms out”.
    # This message is different from polyphonic after-touch.
    # Use this message to send the single greatest pressure value (of all the current depressed keys).
    # Data1 : 7=0, [6-0] pressure value
    ChannelPressure = 0x0D
    # This message is sent to indicate a change in the pitch bender (wheel or lever, typically).
    # The pitch bender is measured by a fourteen bit value. Center (no pitch change) is 2000H.
    # Sensitivity is a function of the receiver, but may be set using RPN 0
    # Data1 : 7=0, [6-0] least significant 7 bits
    # Data2 : 7=0, [6-0] most significant 7 bits
    PitchBendChange = 0x0E

# Control Change Messages
#   => when Status == ChannelMsg.CtrlChangeOrChannelMode and Data1<120 (0x78)
# Data1 : event type, see values of the enumeration below
# Data2 : value associated with the event type
class ControlChange(Enum):
    BankSelect     = 0x00
    ModulationWheelOrLever = 0x01
    BreathController = 0x02
    Undefined_03   = 0x03
    FootController = 0x04
    PortamentoTime = 0x05
    DataEntry      = 0x06
    ChannelVolume  = 0x07
    Balance        = 0x08
    Undefined_09   = 0x09
    Pan            = 0x0A
    ExpressionController = 0x0B
    EffectControl1 = 0x0C
    EffectControl2 = 0x0D
    Undefined_0E   = 0x0E
    Undefined_0F   = 0x0F
    GeneralPurposeController1 = 0x10
    GeneralPurposeController2 = 0x11
    GeneralPurposeController3 = 0x12
    GeneralPurposeController4 = 0x13

    Undefined_14   = 0x14
    Undefined_15   = 0x15
    Undefined_16   = 0x16
    Undefined_17   = 0x17
    Undefined_18   = 0x18
    Undefined_19   = 0x19
    Undefined_1A   = 0x1A
    Undefined_1B   = 0x1B
    Undefined_1C   = 0x1C
    Undefined_1D   = 0x1D
    Undefined_1E   = 0x1E
    Undefined_1F   = 0x1F
    
    LSBforBankSelect = 0x20
    LSBForModulationWheelOrLever = 0x21
    LSBForBreathController = 0x22
    LSBForControl3         = 0x23
    LSBForFootController   = 0x24
    LSBForPortamentoTime   = 0x25
    LSBForDataEntry        = 0x26
    LSBForChannelVolume    = 0x27
    LSBForBalance          = 0x28
    LSBForControl9         = 0x29
    LSBForPan              = 0x2A
    LSBForExpressionController = 0x2B
    LSBForEffectControl1    = 0x2C
    LSBForEffectControl2    = 0x2D
    LSBForControl14         = 0x2E
    LSBForControl15         = 0x2F
    LSBForGeneralPurposeController1 = 0x30
    LSBForGeneralPurposeController2 = 0x31
    LSBForGeneralPurposeController3 = 0x32
    LSBForGeneralPurposeController4 = 0x33

    LSBForControl20         = 0x34
    LSBForControl21         = 0x35
    LSBForControl22         = 0x36
    LSBForControl23         = 0x37
    LSBForControl24         = 0x38
    LSBForControl25         = 0x39
    LSBForControl26         = 0x3A
    LSBForControl27         = 0x3B
    LSBForControl28         = 0x3C
    LSBForControl29         = 0x3D
    LSBForControl30         = 0x3E
    LSBForControl31         = 0x3F
    
    # Data2  : ≤63 off, ≥64 on
    DamperPedalOnOff = 0x40
    # Data2  : ≤63 off, ≥64 on
    PortamentoOnOff  = 0x41
    # Data2  : ≤63 off, ≥64 on
    SostenutoOnOff   = 0x42
    # Data2  : ≤63 off, ≥64 on
    SoftPedalOnOff   = 0x43
    # Data2  : ≤63 normal, ≥64 legato
    LegatoFootswitch = 0x44
    # Data2  : ≤63 off, ≥64 on
    Hold2            = 0x45
    SoundController1  = 0x46
    SoundController2  = 0x47
    SoundController3  = 0x48
    SoundController4  = 0x49
    SoundController5  = 0x4A
    SoundController6  = 0x4B
    SoundController7  = 0x4C
    SoundController8  = 0x4D
    SoundController9  = 0x4E
    SoundController10 = 0x4F
    GeneralPurposeController5 = 0x50
    GeneralPurposeController6 = 0x51
    GeneralPurposeController7 = 0x52
    GeneralPurposeController8 = 0x53
    PortamentoControl = 0x54
    Undefined_55   = 0x55
    Undefined_56   = 0x56
    Undefined_57   = 0x57
    HighResolutionVelocityPrefix = 0x58
    Undefined_59   = 0x59
    Undefined_5A   = 0x5A
    
    Effects1Depth = 0x5B
    Effects2Depth = 0x5C
    Effects3Depth = 0x5D
    Effects4Depth = 0x5E
    Effects5Depth = 0x5F

    DataIncrement = 0x60
    DataDecrement = 0x61

    # Non-Registered Parameter Number
    NRPN_LSB = 0x62
    NRPN_MSB = 0x63

    # Registered Parameter Number
    RPN_LSB = 0x64
    RPN_MSB = 0x65

    Undefined_66   = 0x66
    Undefined_67   = 0x67
    Undefined_68   = 0x68
    Undefined_69   = 0x69
    Undefined_6A   = 0x6A
    Undefined_6B   = 0x6B
    Undefined_6C   = 0x6C
    Undefined_6D   = 0x6D
    Undefined_6E   = 0x6E
    Undefined_6F   = 0x6F
    Undefined_70   = 0x70
    Undefined_71   = 0x71
    Undefined_72   = 0x72
    Undefined_73   = 0x73
    Undefined_74   = 0x74
    Undefined_75   = 0x75
    Undefined_76   = 0x76
    Undefined_77   = 0x77
    
# Channel Mode Messages
#   => when Status == ChannelMsg.CtrlChangeOrChannelMode and Data1 in [120,127] ([0x78, 0x7F])
# Data1 : value of the enumeration below
class ChannelMode(Enum):
    # When All Sound Off is received all oscillators will turn off, 
    # and their volume envelopes are set to zero as soon as possible
    # Data2 = 0
    AllSoundOff = 0x78
    # When Reset All Controllers is received, all controller values are reset to their default values
    # (See specific Recommended Practices for defaults)
    # Data2 = 0, unless otherwise allowed in a specific Recommended Practice
    ResetAllControllers = 0x79
    # When Local Control is Off, all devices on a given channel will respond only to data received over MIDI.
    # Played data, etc. will be ignored. Local Control On restores the functions of the normal controllers.
    # Data2 = 0 : LocalControlOff
    # Data2 = 1 : LocalControlOn
    LocalControl = 0x7A
    # When an All Notes Off is received, all oscillators will turn off
    # Data2 = 0
    AllNotesOff = 0x7B
    # Omni Mode Off (also causes AllNotesOff)
    # Data2 = 0
    OmniModeOff = 0x7C
    # Omni Mode On (also causes AllNotesOff)
    # Data2 = 0
    OmniModeOn = 0x7D
    # Mono Mode On (also causes AllNotesOff and Poly Mode Off)
    # Data2 = number of channels (if Omni Off) or 0 (if Omni On)
    MonoModeOn = 0x7E
    # Poly Mode On (also causes AllNotesOff and Mono Mode Off)
    # Data2 = 0
    PolyModeOn = 0x7F
    
	
# System Common Messages
# Status byte : see enumeration values below
# Data byte(s) : bit #7 of all data bytes is set to 0
class SystemCommonMsg(Enum):
    # This message type allows manufacturers to create their own messages
    # with unlimited number of Data bytes.
    # The 1 to 3 first data bytes contain the manufacturer ID
    # Note : Must be followed by an EndOfExclusive MIDI message
    SystemExclusive = 0xF0
    # Data1 : [7]=0, [6-4] Message Type, [3-0] Values
    MidiTimeCodeQuarterFrame = 0xF1
    # This is an internal 14 bit register that holds the number of MIDI beats
    # (1 beat= six MIDI clocks) since the start of the song.
    # Data1 is the LSB, Data2 the MSB
    SongPositionPointer = 0xF2
    # Data1 : song number
    SongSelect = 0xF3
    # Upon receiving a Tune Request, all analog synthesizers should tune their oscillators
    TuneRequest = 0xF6
    # Used to terminate a System Exclusive message (see above)
    EndOfExclusive = 0xF7

# Real-Time Messages
# Status byte : see enumeration values below
# Data byte(s) : bit #7 of all data bytes is set to 0
class RealTimeMsg(Enum):
    # Sent 24 times per quarter note when synchronization is required
    TimingClock = 0xF8
    # Start the current sequence playing.
    # (This message will be followed with Timing Clocks)
    Start = 0xFA
    # Continue at the point the sequence was Stopped
    Continue = 0xFB
    # Stop the current sequence
    Stop = 0xFC
    # This message is intended to be sent repeatedly to tell the receiver that a connection is alive.
    # Use of this message is optional. When initially received, the receiver will expect to receive 
    # another Active Sensing message each 300ms (max), and if it does not then it will assume that the 
    # connection has been terminated. At termination, the receiver will turn off all voices and return
    # to normal (non6 active sensing) operation.
    ActiveSensing = 0xFE
    # Reset all receivers in the system to power-up status. This should be used sparingly, 
    # preferably under manual control. In particular, it should not be sent on power-up.
    Reset = 0xFF


class MsgCategory(Enum):
	CVM = auto() # Channel Voice Message
	CC = auto() # Control Change Message
	CM = auto() # Channel Mode Message
	SCM = auto() # System Common Message
	RTM = auto() # Real-Time Message
     
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
        SCM      | SystemExclusive          | sys_ex_data
        SCM      | MidiTimeCodeQuarterFrame | 
        SCM      | SongPositionPointer      | 
        SCM      | SongSelect               | 
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
                        # Is it a universal system exclusive message ?
                        if res.bytes[1] == 0x7E:
                            if size>3:
                                # Non real-time message
                                res.sys_ex_type = 'NRTM'
                                invalid_data = False
                        if res.bytes[1] == 0x7F:
                            if size>3:
                                # Real-time message
                                res.sys_ex_type = 'RTM'
                                invalid_data = False
                        else:
                            # Manufacturer specific message
                            res.sys_ex_type = 'MSM'
                            invalid_data = False
                        
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
                data_str.append(self.sys_ex_type)
            """ elif self.type==SystemCommonMsg.MidiTimeCodeQuarterFrame:
            elif self.type==SystemCommonMsg.SongPositionPointer:
            elif self.type==SystemCommonMsg.SongSelect:
            elif self.type==SystemCommonMsg.TuneRequest: """
        
        elif isinstance(self.type, RealTimeMsg):
             data_str.append(MidiMsg.__enum2str(RealTimeMsg(self.type),hexa))
             #TBD
        
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