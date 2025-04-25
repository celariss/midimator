from enum import Enum
import rtmidi

# source : https://midi.org/spec-detail
# MIDI 1.0 message format :
#	[Status, Data1, Data2, ...]
# A message canb be either a Channel message (see ChannelMsg below),
# a System Common or Real-Time Messages (see SystemCommonMsg below),
# depending on the first byte (Status).

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
#   => when Status == ChannelMsg.CtrlChangeOrChannelModeMsg and Data1<120
# Data1 : event type, see values of the enumeration below
# Data2 : value associated with the event type
class ControlChangeMsg(Enum):
    BankSelect     = 0x00
    ModulationWheelOrLever = 0x01
    BreathController = 0x02
    FootController = 0x04
    PortamentoTime = 0x05
    DataEntry      = 0x06
    ChannelVolume  = 0x07
    Balance        = 0x08
    Pan            = 0x0A
    ExpressionController = 0x0B
    EffectControl1 = 0x0C
    EffectControl2 = 0x0D
    GeneralPurposeController1 = 0x10
    GeneralPurposeController2 = 0x11
    GeneralPurposeController3 = 0x12
    GeneralPurposeController4 = 0x13
    
    LSBforBankSelect = 0x20
    LSBForModulationWheelOrLever = 0x21
    LSBForBreathController = 0x22
    LSBForFootController   = 0x24
    LSBForPortamentoTime   = 0x25
    LSBForDataEntry        = 0x26
    LSBForChannelVolume    = 0x27
    LSBForBalance          = 0x28
    LSBForPan              = 0x2A
    LSBForExpressionController = 0x2B
    LSBForEffectControl1   = 0x2C
    LSBForEffectControl2   = 0x2D
    LSBForGeneralPurposeController1 = 0x30
    LSBForGeneralPurposeController2 = 0x31
    LSBForGeneralPurposeController3 = 0x32
    LSBForGeneralPurposeController4 = 0x33
    
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
    HighResolutionVelocityPrefix = 0x58
    
    Effects1Depth = 0x5B
    Effects2Depth = 0x5C
    Effects3Depth = 0x5D
    Effects4Depth = 0x5E
    Effects5Depth = 0x5F
    
# Channel Mode Messages
#   => when Status == ChannelMsg.CtrlChangeOrChannelModeMsg and Data1 in [120,127]
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

class MidiHelpers:
    def get_midi_ports()->dict:
        available_ports = {}
        midiin = rtmidi.MidiIn()
        idx = 0
        for port in midiin.get_ports():
            available_ports[port] = {'input_idx':idx}
            idx += 1
        del midiin
        
        midiout = rtmidi.MidiOut()
        idx = 0
        for port in midiout.get_ports():
            value = available_ports[port] if port in available_ports else {}
            value['output_idx'] = idx
            available_ports[port] = value
            idx += 1
        del midiout

        return available_ports
    
    def msg_to_string(midimsg:list)->str:
        return MidiHelpers.msg_to_raw_string(midimsg) + ' = ' + MidiHelpers.msg_to_friendly_string(midimsg)
    
    def msg_to_raw_string(midimsg:list)->str:
        return '[' + ', '.join('0x%02X' % x for x in midimsg) + ']'
    
    def msg_to_friendly_string(msg:list)->str:
        size = len(msg)
        data_str = []
        invalid_data = True
        if size>0:
            MSB = (msg[0]>>4)&0xF
            LSB = msg[0]&0xF
            if MidiHelpers._has_value(ChannelMsg, MSB):
                status = ChannelMsg(MSB)
                channel = LSB
                data_str.append('channel:' + str(LSB+1))
                if status==ChannelMsg.NoteOff or status==ChannelMsg.NoteOn or status==ChannelMsg.PolyphonicKeyPressure:
                    if size==3:
                        data_str.append('note:'+MidiHelpers._note_to_string(msg[1]))
                        data_str.append('velocity:' + str(msg[2]))
                        invalid_data = False
                
                elif status==ChannelMsg.CtrlChangeOrChannelModeMsg:
                    if size==3:
                        if msg[1]<120 and msg[1] in ControlChangeMsg:
                            data_str.append(str(ControlChangeMsg(msg[1])))
                            if msg[2]<128:
                                data_str.append(int(msg[2]))
                                invalid_data = False
                        elif msg[1]>=120 and msg[1] in ChannelModeMsg:
                            data_str.append(str(ChannelModeMsg(msg[1])))
                            if msg[2]<128:
                                data_str.append(int(msg[2]))
                                invalid_data = False
                                
                elif status==ChannelMsg.ProgramChange or status==ChannelMsg.ChannelPressure:
                    if size==2:
                        data_str.append(int(msg[1]))
                        invalid_data = False
                        
                elif status==ChannelMsg.PitchBendChange:
                    if size==3:
                        data_str.append('LSB='+str(msg[1]))
                        data_str.append('MSB='+str(msg[2]))
                        invalid_data = False
                
            elif MidiHelpers._has_value(SystemCommonMsg, msg[0]):
                status = SystemCommonMsg(msg[0])
                invalid_data = False
                # TBD
            else:
                return 'Unknown message'
        else:
            return 'empty message'
            
        data_str.insert(0, str(status))
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
    
    def _has_value(enum, value):
        return value in enum._value2member_map_ 

