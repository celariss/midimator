import datetime
from enum import Enum
import sys
import mido

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
    #   Compare Data1 to ControlChangeMsg enum to get exact message
    # if controller number is in [120,127], it's a Channel Mode Message :
    #   Compare Data1 to ChannelModeMsg enum to get exact message
    CtrlChangeOrChannelModeMsg = 0X0B
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
#   => when Status == ChannelMsg.CtrlChangeOrChannelModeMsg and Data1<120 (0x78)
# Data1 : event type, see values of the enumeration below
# Data2 : value associated with the event type
class ControlChangeMsg(Enum):
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
#   => when Status == ChannelMsg.CtrlChangeOrChannelModeMsg and Data1 in [120,127] ([0x78, 0x7F])
# Data1 : value of the enumeration below
class ChannelModeMsg(Enum):
    # When All Sound Off is received all oscillators will turn off, 
    # and their volume envelopes are set to zero as soon as possible
    # Data2 = 0
    AllSoundOff = 120
    # When Reset All Controllers is received, all controller values are reset to their default values
    # (See specific Recommended Practices for defaults)
    # Data2 = 0, unless otherwise allowed in a specific Recommended Practice
    ResetAllControllers = 121
    # When Local Control is Off, all devices on a given channel will respond only to data received over MIDI.
    # Played data, etc. will be ignored. Local Control On restores the functions of the normal controllers.
    # Data2 = 0 : LocalControlOff
    # Data2 = 1 : LocalControlOn
    LocalControl = 122
    # When an All Notes Off is received, all oscillators will turn off
    # Data2 = 0
    AllNotesOff = 123
    # Omni Mode Off (also causes AllNotesOff)
    # Data2 = 0
    OmniModeOff = 124
    # Omni Mode On (also causes AllNotesOff)
    # Data2 = 0
    OmniModeOn = 125
    # Mono Mode On (also causes AllNotesOff and Poly Mode Off)
    # Data2 = number of channels (if Omni Off) or 0 (if Omni On)
    MonoModeOn = 126
    # Poly Mode On (also causes AllNotesOff and Mono Mode Off)
    # Data2 = 0
    PolyModeOn = 127
    
	
# System Common and Real-Time Messages
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

def get_timestr(time:datetime.datetime)->str:
    return time.strftime("%Y-%m-%dT%H:%M:%S.%f")

def int_to_str(value:int, hexa:bool):
    if hexa:
        return hex(value)
    else:
        return str(value)

class MidiHelpers:
    def get_midi_ports()->dict:
        """Return a list of all midi ports available on the current system

        Returns:
            dict: key item is the port name
        """
        available_ports = {}
        idx = 0
        for port in mido.get_input_names():
            available_ports[port] = {'input_idx':idx}
            idx += 1
        
        idx = 0
        for port in mido.get_output_names():
            value = available_ports[port] if port in available_ports else {}
            value['output_idx'] = idx
            available_ports[port] = value
            idx += 1

        return available_ports
    
    def msg_to_string(midimsg:mido.Message, hexa:bool = False)->str:
        return MidiHelpers.msg_to_raw_string(midimsg,hexa) + ' = ' + MidiHelpers.msg_to_friendly_string(midimsg,hexa)
    
    def msg_to_raw_string(midimsg:mido.Message, hexa:bool = False)->str:
        return MidiHelpers.bytes_to_raw_string(midimsg.bytes(), hexa)
    
    def bytes_to_raw_string(midimsg:list, hexa:bool = False)->str:
        return '[' + ', '.join(int_to_str(x,hexa) for x in midimsg) + ']'
    
    def msg_to_friendly_string(msg:mido.Message, hexa:bool = False)->str:
        msg = msg.bytes()
        size = len(msg)
        data_str = []
        invalid_data = True
        if size>0:
            MSB = (msg[0]>>4)&0xF
            LSB = msg[0]&0xF
            if MidiHelpers._has_value(ChannelMsg, MSB):
                status = ChannelMsg(MSB)
                channel = LSB
                data_str.append('channel:' + int_to_str(channel+1, hexa))
                
                if status==ChannelMsg.NoteOff or status==ChannelMsg.NoteOn or status==ChannelMsg.PolyphonicKeyPressure:
                    if size==3:
                        data_str.insert(0, MidiHelpers._enum2str(status,hexa))
                        data_str.append('note:'+MidiHelpers._note_to_string(msg[1])+'('+int_to_str(msg[1],hexa)+')')
                        data_str.append('velocity:' + int_to_str(msg[2],hexa))
                        invalid_data = False
                
                elif status==ChannelMsg.CtrlChangeOrChannelModeMsg:
                    if size==3:
                        if msg[1]<120 and msg[1] in ControlChangeMsg:
                            data_str.insert(0, 'CC.'+MidiHelpers._enum2str(ControlChangeMsg(msg[1]),hexa))
                            if msg[2]<128:
                                data_str.append(int_to_str(msg[2],hexa))
                                invalid_data = False
                        elif msg[1]>=120 and msg[1] in ChannelModeMsg:
                            data_str.insert(0, 'CM.'+MidiHelpers._enum2str(ChannelModeMsg(msg[1]),hexa))
                            if msg[2]<128:
                                data_str.append(int_to_str(msg[2],hexa))
                                invalid_data = False
                                
                elif status==ChannelMsg.ProgramChange or status==ChannelMsg.ChannelPressure:
                    if size==2:
                        data_str.insert(0, MidiHelpers._enum2str(status,hexa))
                        data_str.append(int_to_str(msg[1],hexa))
                        invalid_data = False
                        
                elif status==ChannelMsg.PitchBendChange:
                    if size==3:
                        data_str.insert(0, MidiHelpers._enum2str(status,hexa))
                        data_str.append('LSB='+int_to_str(msg[1],hexa))
                        data_str.append('MSB='+int_to_str(msg[2],hexa))
                        invalid_data = False
                
            elif MidiHelpers._has_value(SystemCommonMsg, msg[0]):
                status = SystemCommonMsg(msg[0])
                data_str.insert(0, MidiHelpers._enum2str(status,hexa))
                invalid_data = False
                # TBD
            else:
                return 'Unknown message'
        else:
            return 'empty message'
            
        if invalid_data:
            data_str.append('invalid data')
        return '['+', '.join(data_str)+']'

    _notes_str = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    def _note_to_string(value:int)->str:
        if value>127:
            return 'invalid note'
        note = value%12
        octave = value//12
        return MidiHelpers._notes_str[note]+str(octave+1)
    
    def send_bytes(outport, bytes_msg:list, hexa:bool)->bool:
        if len(bytes_msg)>3 and bytes_msg[0] != 0xF0:
            bytes_msg.insert(0, 0xF0)
        try:
            midimsg:mido.Message = mido.Message.from_bytes(bytes_msg)
        except:
            print('error: Invalid midi message '+MidiHelpers.bytes_to_raw_string(bytes_msg,hexa), file=sys.stderr)
            return False
        print(get_timestr(datetime.datetime.now())+' | '+MidiHelpers.msg_to_string(midimsg,hexa)+ ' (to: "'+outport[1]+'")')
        outport[0].send(midimsg)
        return True
    
    def _has_value(enum, value)->bool:
        return value in enum._value2member_map_ 
    
    def _enum2str(enumvalue, hexa:bool)->str:
        return str(enumvalue).split('.')[1]+'('+int_to_str(enumvalue.value,hexa)+')'