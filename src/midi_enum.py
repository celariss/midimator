from enum import Enum, auto

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

class NRTSysEx(Enum):
    Unknown  = (0x00)
    Sample_Dump_Header       = (0x01)
    Sample_Data_Packet       = (0x02)
    Sample_Dump_Request      = (0x03)
    TimeCode_Special                 = (0x04, 0x00)
    TimeCode_PunchInPoints           = (0x04, 0x01)
    TimeCode_PunchOutPoints          = (0x04, 0x02)
    TimeCode_DeletePunchInPoint      = (0x04, 0x03)
    TimeCode_DeletePunchOutPoint     = (0x04, 0x04)
    TimeCode_EventStartPoint         = (0x04, 0x05)
    TimeCode_EventStopPoint          = (0x04, 0x06)
    TimeCode_EventStartPointsAddInfo = (0x04, 0x07)
    TimeCode_EventStopPointAddInfo   = (0x04, 0x08)
    TimeCode_DeleteEventStartPoint   = (0x04, 0x09)
    TimeCode_DeleteEventStopPoint    = (0x04, 0x0A)
    TimeCode_CuePoints               = (0x04, 0x0B)
    TimeCode_CuePointsAddInfo        = (0x04, 0x0C)
    TimeCode_DeleteCuePoint          = (0x04, 0x0D)
    TimeCode_EventNameAddInfo        = (0x04, 0x0E)
    Sample_LoopPointsTransmission   = (0x05, 0x01)
    Sample_LoopPointsRequest        = (0x05, 0x02)
    Sample_SampleNameTransmission   = (0x05, 0x03)
    Sample_SameNameRequest          = (0x05, 0x04)
    Sample_ExDumpHeader             = (0x05, 0x05)
    Sample_ExLoopPointsTransmission = (0x05, 0x06)
    Sample_ExLoopPointsRequest      = (0x05, 0x07)
    GeneralInfo_IdRequest  = (0x06, 0x01)
    GeneralInfo_IdReply    = (0x06, 0x02)
    FileDump_Header     = (0x07, 0x01)
    FileDump_DataPacket = (0x07, 0x02)
    FileDump_Request    = (0x07, 0x03)
    Tuning_BulkDumpRequest        = (0x08, 0x00)
    Tuning_BulkDumpReply          = (0x08, 0x01)
    Tuning_TuningDumpRequest      = (0x08, 0x03)
    Tuning_KeyBasedTuningDump     = (0x08, 0x04)
    Tuning_ScaleTuningDump_1b     = (0x08, 0x05)
    Tuning_ScaleTuningDump_2b     = (0x08, 0x06)
    Tuning_SingleNoteTuningChange = (0x08, 0x07)
    Tuning_ScaleTuning_1b         = (0x08, 0x08)
    Tuning_ScaleTuning_2b         = (0x08, 0x09)
    General_GeneralMIDI1SystemOn   = (0x09, 0x01)
    General_GeneralMIDISystemOff   = (0x09, 0x02)
    General_GeneralMIDI2SystemOn   = (0x09, 0x03)
    TurnDLSOn            = (0x0A, 0x01)
    TurnDLSOff           = (0x0A, 0x02)
    TurnDLSVoiceAllocOff = (0x0A, 0x03)
    TurnDLSVoiceAllocOn  = (0x0A, 0x04)
    FileRefMsg_OpenFile                  = (0x0B, 0x01)
    FileRefMsg_SelectContents            = (0x0B, 0x02)
    FileRefMsg_OpenFileAndSelectContents = (0x0B, 0x03)
    FileRefMsg_CloseFile                 = (0x0B, 0x04)
    MidiVisualCtrl  = (0x0C, 0xFF) # 00 to 7F
    MidiCapability  = (0x0D, 0xFF) # 00 to 7F
    EndOfFile       = (0x7B)
    Wait      = (0x7C)
    Cancel    = (0x7D)
    NAK       = (0x7E)
    ACK      = (0x7F)

class RTSysEx(Enum):
    Unknown  = (0x00)
    TimeCode_FullMessage   = (0x01, 0x01)
    TimeCode_UserBits      = (0x01, 0x02)
    MIDIShowCtrl           = (0x02, 0xFF) # 00 to 7F
    NotationInfo_BarNumber = (0x03, 0x01)
    NotationInfo_TimeSignatureImmediate = (0x03, 0x02)
    NotationInfo_TimeSignatureDelayed   = (0x03, 0x42)
    # TBD

class MsgCategory(Enum):
	CVM = auto() # Channel Voice Message
	CC = auto() # Control Change Message
	CM = auto() # Channel Mode Message
	SCM = auto() # System Common Message
	RTM = auto() # Real-Time Message

class Manufacturer(Enum):
    """ see https://www.amei.or.jp/report/System_ID_e.html
    """
    Unknown                  = (0x00)
    Sequential               = (0x01)
    IDP                      = (0x02)
    Voyetra_Technologies     = (0x03)
    Moog_Music               = (0x04)
    Passport_Designs         = (0x05)
    Lexicon_Inc              = (0x06)
    Kutzweil_Young_Chang     = (0x07)
    Fender                   = (0x08)
    Gulbransen               = (0x09)
    AKG_Acoustics            = (0x0A)
    Voyce_Music              = (0x0B)
    Waveframe_Corp           = (0x0C)
    ADA_Signal_Processors    = (0x0D)
    Garfield_Electronics     = (0x0E)
    Ensoniq_Corp             = (0x0F)
    Oberheim_Gibson_Labs     = (0x10)
    Apple_Computer           = (0x11)
    Grey_Matter_Response     = (0x12)
    Digidesign_Inc           = (0x13)
    Palmtree_Instruments     = (0x14)
    JLCooper_Electronics     = (0x15)
    Lowrey_Organ_Company     = (0x16)
    Adams_Smith              = (0x17)
    Emu_Systems_Inc          = (0x18)
    Harmony_Systems          = (0x19)
    ART                      = (0x1A)
    Baldwin                  = (0x1B)
    Eventide                 = (0x1C)
    Inventronics             = (0x1D)
    Clarity                  = (0x1F)
    Passac                   = (0x20)
    SIEL                     = (0x21)
    Synthaxe_UK              = (0x22)
    Stepp                    = (0x23)
    Hohner                   = (0x24)
    Twister                  = (0x25)
    Solton                   = (0x26)
    Jellinghaus_MS           = (0x27)
    Southworth_Music_Systems = (0x28)
    PPG_Germany              = (0x29)
    JEN                      = (0x2A)
    Solid_State_Logic_Organ_Systems  = (0x2B)
    Audio_Veritrieb_P_Struven        = (0x2C)
    Neve                             = (0x2D)
    Soundtracs_Ltd                   = (0x2E)
    Elka                             = (0x2F)
    Dynacord                         = (0x30)
    Intercontinental_Electronics_SpA = (0x31)
    Drawmer                          = (0x32)
    Clavia_Digital_Instruments       = (0x33)
    Audio_Architecture               = (0x34)
    GeneralMusic_Corp_c_o            = (0x35)
    Cheetah_Marketing                = (0x36)
    C_T_M                            = (0x37)
    Simmons_UK                       = (0x38)
    Soundcraft_Electronics           = (0x39)
    Steinberg_GMBH_c_o               = (0x3A)
    Wersi_Gmbh                       = (0x3B)
    AVAB_Niethammer_AB               = (0x3C)
    Digigram                         = (0x3D)
    Waldorf_Electronics_GmbH         = (0x3E)
    Quasimidi                        = (0x3F)
    KAWAI_MUSICAL_INSTRUMENTS_MFG_CO_LTD  = (0x40)
    ROLAND_CORPORATION                    = (0x41)
    KORG_INC                              = (0x42)
    YAMAHA_CORPORATION                    = (0x43)
    CASIO_COMPUTER_CO_LTD                 = (0x44)
    AKAI_ELECTRIC_CO_LTD                  = (0x47)
    VICTOR_COMPANY_OF_JAPAN_LTD           = (0x48)
    FUJITSU_LIMITED                       = (0x4B)
    SONY_CORPORATION                      = (0x4C)
    TEAC_CORPORATION                      = (0x4E)
    MATSUSHITA_ELECTRIC_INDUSTRIAL_CO_LTD = (0x50)
    FOSTEX_CORPORATION                    = (0x51)
    ZOOM_CORPORATION                      = (0x52)
    MATSUSHITA_COMMUNICATION_INDUSTRIAL_CO_LTD = (0x54)
    SUZUKI_MUSICAL_INSTRUMENTS_MFG_CO_LTD      = (0x55)
    FUJI_SOUND_CORPORATION_LTD        = (0x56)
    ACOUSTIC_TECHNICAL_LABORATORY_INC = (0x57)
    FAITH_INC                         = (0x59)
    INTERNET_CORPORATION              = (0x5A)
    SEEKERS_CO_LTD                    = (0x5C)
    SD_CARD_ASSOCIATION               = (0x5F)
    Time_Warner_Interactive     = (0x00, 0x00, 0x01)
    Advanced_Gravis_Comp        = (0x00, 0x00, 0x02)
    Media_Vision                = (0x00, 0x00, 0x03)
    Dornes_Research_Group       = (0x00, 0x00, 0x04)
    K_Muse                      = (0x00, 0x00, 0x05)
    Stypher                     = (0x00, 0x00, 0x06)
    Digital_Music_Corp          = (0x00, 0x00, 0x07)
    IOTA_Systems                = (0x00, 0x00, 0x08)
    New_England_Digital         = (0x00, 0x00, 0x09)
    Artisyn                     = (0x00, 0x00, 0x0A)
    IVL_Technologies            = (0x00, 0x00, 0x0B)
    Southern_Music_Systems      = (0x00, 0x00, 0x0C)
    Lake_Butler_Sound_Co        = (0x00, 0x00, 0x0D)
    Alesis_Studio_Electronics   = (0x00, 0x00, 0x0E)
    Sound_Creation              = (0x00, 0x00, 0x0F)
    DOD_Electronics_Corp        = (0x00, 0x00, 0x10)
    Studer_Editech              = (0x00, 0x00, 0x11)
    Sonus                       = (0x00, 0x00, 0x12)
    Temporal_Acuity_Products    = (0x00, 0x00, 0x13)
    Perfect_Fretworks           = (0x00, 0x00, 0x14)
    KAT_Inc                     = (0x00, 0x00, 0x15)
    Opcode_Systems              = (0x00, 0x00, 0x16)
    Rane_Corporation            = (0x00, 0x00, 0x17)
    Anadi_Electronique          = (0x00, 0x00, 0x18)
    KMX                         = (0x00, 0x00, 0x19)
    Allen_Heath_Brenell         = (0x00, 0x00, 0x1A)
    Peavey_Electronics          = (0x00, 0x00, 0x1B)
    _360_System                 = (0x00, 0x00, 0x1C)
    Spectrum_Design             = (0x00, 0x00, 0x1D)
    Marquis_Music               = (0x00, 0x00, 0x1E)
    Zeta_Systems                = (0x00, 0x00, 0x1F)
    Axxes                       = (0x00, 0x00, 0x20)
    Orban                       = (0x00, 0x00, 0x21)
    Indian_Valley_Mfg           = (0x00, 0x00, 0x22)
    Triton                      = (0x00, 0x00, 0x23)
    KTI                         = (0x00, 0x00, 0x24)
    Breakaway_Technologies      = (0x00, 0x00, 0x25)
    CAE_Inc                     = (0x00, 0x00, 0x26)
    Harrison_Systems_Inc        = (0x00, 0x00, 0x27)
    Future_Lab_Mark_Kuo         = (0x00, 0x00, 0x28)
    Rocktron_Corporation        = (0x00, 0x00, 0x29)
    PianoDisc                   = (0x00, 0x00, 0x2A)
    Cannon_Research_Group       = (0x00, 0x00, 0x2B)
    Rodgers_Instrument_Corp     = (0x00, 0x00, 0x2D)
    Blue_Sky_Logic              = (0x00, 0x00, 0x2E)
    Encore_Electronics          = (0x00, 0x00, 0x2F)
    Uptown                      = (0x00, 0x00, 0x30)
    Voce                        = (0x00, 0x00, 0x31)
    CTI_Audio                   = (0x00, 0x00, 0x32)
    S_S_Research                = (0x00, 0x00, 0x33)
    Broderbund_Software         = (0x00, 0x00, 0x34)
    Allen_Organ_Co              = (0x00, 0x00, 0x35)
    Music_Quest                 = (0x00, 0x00, 0x37)
    Aphex                       = (0x00, 0x00, 0x38)
    Gallien_Krueger             = (0x00, 0x00, 0x39)
    IBM                         = (0x00, 0x00, 0x3A)
    Mark_of_the_Unicorn         = (0x00, 0x00, 0x3B)
    Hotz_Instruments            = (0x00, 0x00, 0x3C)
    ETA_Lighting                = (0x00, 0x00, 0x3D)
    NSI_Corporation             = (0x00, 0x00, 0x3E)
    Ad_Lib                      = (0x00, 0x00, 0x3F)
    Richmond_Sound_Design       = (0x00, 0x00, 0x40)
    Microsoft_Corp              = (0x00, 0x00, 0x41)
    Software_Toolworks          = (0x00, 0x00, 0x42)
    Russ_Jones_Niche            = (0x00, 0x00, 0x43)
    Intone                      = (0x00, 0x00, 0x44)
    Advanced_Remote_Tech        = (0x00, 0x00, 0x45)
    GT_Electronics              = (0x00, 0x00, 0x47)
    Timeline_Vista              = (0x00, 0x00, 0x49)
    Mesa_Boogie_Ltd             = (0x00, 0x00, 0x4A)
    Sequoia_Development         = (0x00, 0x00, 0x4C)
    Studio_Electronics          = (0x00, 0x00, 0x4D)
    Euphonix                    = (0x00, 0x00, 0x4E)
    InterMIDI                   = (0x00, 0x00, 0x4F)
    MIDI_Solutions_Inc          = (0x00, 0x00, 0x50)
    _3DO_Company                = (0x00, 0x00, 0x51)
    Lightwave_Research          = (0x00, 0x00, 0x52)
    Micro_W_Corporation         = (0x00, 0x00, 0x53)
    Spectral_Synthesis          = (0x00, 0x00, 0x54)
    Lone_Wolf                   = (0x00, 0x00, 0x55)
    Studio_Technologies_Inc     = (0x00, 0x00, 0x56)
    Peterson_Electro_Musical    = (0x00, 0x00, 0x57)
    Atari_Corporation           = (0x00, 0x00, 0x58)
    Marion_Systems              = (0x00, 0x00, 0x59)
    Design_Event                = (0x00, 0x00, 0x5A)
    Winjammer_Software          = (0x00, 0x00, 0x5B)
    ATT_Bell_Laboratories       = (0x00, 0x00, 0x5C)
    Symetrix                    = (0x00, 0x00, 0x5E)
    MIDI_the_World              = (0x00, 0x00, 0x5F)
    Desper_Products             = (0x00, 0x00, 0x60)
    Micros_N_MIDI               = (0x00, 0x00, 0x61)
    Accordians_International    = (0x00, 0x00, 0x62)
    EuPhonics                   = (0x00, 0x00, 0x63)
    Musonix                     = (0x00, 0x00, 0x64)
    Turtle_Beach_Systems        = (0x00, 0x00, 0x65)
    Mackie_Designs              = (0x00, 0x00, 0x66)
    Compuserve                  = (0x00, 0x00, 0x67)
    BEC_Technologies            = (0x00, 0x00, 0x68)
    QRS_Music_Rolls_Inc         = (0x00, 0x00, 0x69)
    P_G_Music                   = (0x00, 0x00, 0x6A)
    Sierra_Semiconductor        = (0x00, 0x00, 0x6B)
    EpiGraf_Audio_Visual        = (0x00, 0x00, 0x6C)
    Electronics_Diversified_Inc = (0x00, 0x00, 0x6D)
    Tune_1000                   = (0x00, 0x00, 0x6E)
    Advanced_Micro_Devices      = (0x00, 0x00, 0x6F)
    Mediamation                 = (0x00, 0x00, 0x70)
    Sabine_Musical_Mfg_Co       = (0x00, 0x00, 0x71)
    Woog_Labs                   = (0x00, 0x00, 0x72)
    Micropolis_Corp             = (0x00, 0x00, 0x73)
    Ta_Horng_Musical_Instr      = (0x00, 0x00, 0x74)
    Forte_Technologies          = (0x00, 0x00, 0x75)
    Electro_Voice               = (0x00, 0x00, 0x76)
    Midisoft_Corporation        = (0x00, 0x00, 0x77)
    Q_Sound_Labs                = (0x00, 0x00, 0x78)
    Westrex                     = (0x00, 0x00, 0x79)
    NVidia                      = (0x00, 0x00, 0x7A)
    ESS_Technology              = (0x00, 0x00, 0x7B)
    MediaTrix_Peripherals       = (0x00, 0x00, 0x7C)
    Brooktree_Corp              = (0x00, 0x00, 0x7D)
    Otari_Corp                  = (0x00, 0x00, 0x7E)
    Key_Electronics_Inc         = (0x00, 0x00, 0x7F)
    Shure_Brothers_Inc          = (0x00, 0x01, 0x00)
    Crystalake_Multimedia       = (0x00, 0x01, 0x01)
    Crystal_Semiconductor       = (0x00, 0x01, 0x02)
    Rockwell_Semiconductor      = (0x00, 0x01, 0x03)
    Silicon_Graphics            = (0x00, 0x01, 0x04)
    Midiman                     = (0x00, 0x01, 0x05)
    PreSonus                    = (0x00, 0x01, 0x06)
    Topaz_Enterprises           = (0x00, 0x01, 0x08)
    Cast_Lighting               = (0x00, 0x01, 0x09)
    Microsoft_Consumer_Division = (0x00, 0x01, 0x0A)
    Fast_Forward_Designs        = (0x00, 0x01, 0x0C)
    lgors_Software_Laboratories = (0x00, 0x01, 0x0D)
    Van_Koevering_Company       = (0x00, 0x01, 0x0E)
    Altech_Systems              = (0x00, 0x01, 0x0F)
    S_S_Research_2              = (0x00, 0x01, 0x10)
    VLSI_Technology             = (0x00, 0x01, 0x11)
    Chromatic_Research          = (0x00, 0x01, 0x12)
    Sapphire                    = (0x00, 0x01, 0x13)
    IDRC                        = (0x00, 0x01, 0x14)
    Justonic_Tuning             = (0x00, 0x01, 0x15)
    TorComp                     = (0x00, 0x01, 0x16)
    Newtek_Inc                  = (0x00, 0x01, 0x17)
    Sound_Sculpture             = (0x00, 0x01, 0x18)
    Walker_Technical            = (0x00, 0x01, 0x19)
    PAVO                        = (0x00, 0x01, 0x1A)
    InVision_Interactive        = (0x00, 0x01, 0x1B)
    T_Square_Design             = (0x00, 0x01, 0x1C)
    Nemesys_Music_Technology    = (0x00, 0x01, 0x1D)
    DBX_Professional_Harman_Intl = (0x00, 0x01, 0x1E)
    Syndyne_Corporation         = (0x00, 0x01, 0x1F)
    Bitheadz                    = (0x00, 0x01, 0x20)
    Cakewalk_Music_Software     = (0x00, 0x01, 0x21)
    Analog_Devices_Staccato_Systems = (0x00, 0x01, 0x22)
    National_Semiconductor          = (0x00, 0x01, 0x23)
    Boom_Theory_Adinolfi_Alt_Perc   = (0x00, 0x01, 0x24)
    Virtual_DSP_Corporation         = (0x00, 0x01, 0x25)
    Antares_Systems                 = (0x00, 0x01, 0x26)
    Angel_Software                  = (0x00, 0x01, 0x27)
    St_Louis_Music                  = (0x00, 0x01, 0x28)
    Lyrrus_dba_G_VOX                = (0x00, 0x01, 0x29)
    Ashley_Audio_Inc                = (0x00, 0x01, 0x2A)
    Vari_Lite_Inc                   = (0x00, 0x01, 0x2B)
    Summit_Audio_Inc                = (0x00, 0x01, 0x2C)
    Aureal_Semiconductor_Inc        = (0x00, 0x01, 0x2D)
    SeaSound_LLC                    = (0x00, 0x01, 0x2E)
    U_S_Robotics                    = (0x00, 0x01, 0x2F)
    Aurisis_Research                = (0x00, 0x01, 0x30)
    Nearfield_Multimedia            = (0x00, 0x01, 0x31)
    FM7_Inc                         = (0x00, 0x01, 0x32)
    Swivel_Systems                  = (0x00, 0x01, 0x33)
    Hyperactive_Audio_Systems       = (0x00, 0x01, 0x34)
    MidiLite_Castle_Studios_Prods   = (0x00, 0x01, 0x35)
    Radikal_Technologies            = (0x00, 0x01, 0x36)
    Roger_Linn_Design               = (0x00, 0x01, 0x37)
    TC_Helicon_Vocal_Technologies   = (0x00, 0x01, 0x38)
    Event_Electronics               = (0x00, 0x01, 0x39)
    Sonic_Network_Sonic_Implants    = (0x00, 0x01, 0x3A)
    Realtime_Music_Solutions        = (0x00, 0x01, 0x3B)
    Apogee_Digital                  = (0x00, 0x01, 0x3C)
    Classical_Organs_Inc            = (0x00, 0x01, 0x3D)
    Microtools_Inc                  = (0x00, 0x01, 0x3E)
    Numark_Industries               = (0x00, 0x01, 0x3F)
    Frontier_Design_Group_LLC       = (0x00, 0x01, 0x40)
    Recordare_LLC                   = (0x00, 0x01, 0x41)
    Star_Labs                       = (0x00, 0x01, 0x42)
    Voyager_Sound_Inc               = (0x00, 0x01, 0x43)
    Manifold_Labs                   = (0x00, 0x01, 0x44)
    Aviom_Inc                       = (0x00, 0x01, 0x45)
    Mixmeister_Technology           = (0x00, 0x01, 0x46)
    Notation_Software               = (0x00, 0x01, 0x47)
    Mercurial_Communications        = (0x00, 0x01, 0x48)
    Wave_Arts_Inc                   = (0x00, 0x01, 0x49)
    Logic_Sequencing_Devices_Inc    = (0x00, 0x01, 0x4A)
    Axess_Electronics               = (0x00, 0x01, 0x4B)
    Muse_Reasearch                  = (0x00, 0x01, 0x4C)
    Open_Labs                       = (0x00, 0x01, 0x4D)
    Guillemot_RD_Inc                = (0x00, 0x01, 0x4E)
    Samson_Technologies             = (0x00, 0x01, 0x4F)
    Electoronic_Theatre_Controls    = (0x00, 0x01, 0x50)
    Research_In_Motion              = (0x00, 0x01, 0x51)
    Mobileer                        = (0x00, 0x01, 0x52)
    Synthogy                        = (0x00, 0x01, 0x53)
    Lynx_Studio_Technology_Inc      = (0x00, 0x01, 0x54)
    Damage_Control_Engineering_LLC  = (0x00, 0x01, 0x55)
    Yost_Engineering_Inc            = (0x00, 0x01, 0x56)
    Brooks_Forsman_Designs_LLC      = (0x00, 0x01, 0x57)
    Magnekey                        = (0x00, 0x01, 0x58)
    Garritan_Corp                   = (0x00, 0x01, 0x59)
    Plogue_Art_et_Technology_Inc    = (0x00, 0x01, 0x5A)
    RJM_Music_Technology            = (0x00, 0x01, 0x5B)
    Custom_Solutions_Software       = (0x00, 0x01, 0x5C)
    Sonarcana_LLC                   = (0x00, 0x01, 0x5D)
    Centrance                       = (0x00, 0x01, 0x5E)
    Dream                           = (0x00, 0x20, 0x00)
    Strand_Lighting                 = (0x00, 0x20, 0x01)
    Amek_Systems                    = (0x00, 0x20, 0x02)
    Casa_Di_Risparmio_Di_Loreto     = (0x00, 0x20, 0x03)
    Bohm_electronic_GmbH            = (0x00, 0x20, 0x04)
    Syntec_Digital_Audio            = (0x00, 0x20, 0x05)
    Trident_Audio_Developments      = (0x00, 0x20, 0x06)
    Real_World_Studio               = (0x00, 0x20, 0x07)
    Evolution_Synthesis             = (0x00, 0x20, 0x08)
    Yes_Technology                  = (0x00, 0x20, 0x09)
    Audiomatica                     = (0x00, 0x20, 0x0A)
    Bontempi_Farfisa_COMUS          = (0x00, 0x20, 0x0B)
    F_B_T_Elettronica_SpA           = (0x00, 0x20, 0x0C)
    MidiTemp_GmbH                   = (0x00, 0x20, 0x0D)
    LA_Audio_Larking_Audio          = (0x00, 0x20, 0x0E)
    Zero_88_Lighting_Limited        = (0x00, 0x20, 0x0F)
    Micon_Audio_Electronics_GmbH    = (0x00, 0x20, 0x10)
    Forefront_Technology            = (0x00, 0x20, 0x11)
    Studio_Audio_and_Video_Ltd      = (0x00, 0x20, 0x12)
    Kenton_Electronics              = (0x00, 0x20, 0x13)
    Celco_Division_of_Electrosonic  = (0x00, 0x20, 0x14)
    ADB                             = (0x00, 0x20, 0x15)
    Marshall_Products_Limited       = (0x00, 0x20, 0x16)
    DDA                             = (0x00, 0x20, 0x17)
    BSS_Audio_Ltd                   = (0x00, 0x20, 0x18)
    MA_Lighting_Technology          = (0x00, 0x20, 0x19)
    Fatar_SRL_c_o_Music_Industries  = (0x00, 0x20, 0x1A)
    Artisan_Clasic_Organ_Inc        = (0x00, 0x20, 0x1C)
    Orla_Spa                        = (0x00, 0x20, 0x1D)
    Pinnacle_Audio_Klark_Teknik     = (0x00, 0x20, 0x1E)
    TC_Electronics                  = (0x00, 0x20, 0x1F)
    Doepfer_Musikelektronik_GmbH    = (0x00, 0x20, 0x20)
    Creative_Technology_Pte_Ltd_c_o = (0x00, 0x20, 0x21)
    Seiyddo_Minami                  = (0x00, 0x20, 0x22)
    Goldstar_Co_Ltd                 = (0x00, 0x20, 0x23)
    Midisoft_s_a_s_di_M_Cima_C      = (0x00, 0x20, 0x24)
    Samick_Musical_Inst_Co_Ltd      = (0x00, 0x20, 0x25)
    Penny_and_Giles                 = (0x00, 0x20, 0x26)
    Acorn_Computer                  = (0x00, 0x20, 0x27)
    LSC_Electronics_Pty_Ltd         = (0x00, 0x20, 0x28)
    Novation_EMS                    = (0x00, 0x20, 0x29)
    Samkyung_Mechatronics           = (0x00, 0x20, 0x2A)
    Medeli_Electronics_Co           = (0x00, 0x20, 0x2B)
    Charlie_Lab_SRL                 = (0x00, 0x20, 0x2C)
    Blue_Chip_Music_Technology      = (0x00, 0x20, 0x2D)
    BEE_OH_Corp                     = (0x00, 0x20, 0x2E)
    LG_Semiconductor                = (0x00, 0x20, 0x2F)
    TESI                            = (0x00, 0x20, 0x30)
    EMAGIC                          = (0x00, 0x20, 0x31)
    Behringer_GmbH                  = (0x00, 0x20, 0x32)
    Access                          = (0x00, 0x20, 0x33)
    Synoptic                        = (0x00, 0x20, 0x34)
    Hanmesoft_Corp                  = (0x00, 0x20, 0x35)
    Terratec_Electronic_GmbH        = (0x00, 0x20, 0x36)
    Proel_SpA                       = (0x00, 0x20, 0x37)
    IBK_MIDI                        = (0x00, 0x20, 0x38)
    IRCAM                           = (0x00, 0x20, 0x39)
    Propellerhead_Software          = (0x00, 0x20, 0x3A)
    Red_Sound_Systems_Ltd           = (0x00, 0x20, 0x3B)
    Elektron_ESI_AB                 = (0x00, 0x20, 0x3C)
    Sintefex_Audio                  = (0x00, 0x20, 0x3D)
    MAM_Music_and_More              = (0x00, 0x20, 0x3E)
    Amsaro_GmbH                     = (0x00, 0x20, 0x3F)
    CDS_Advanced_Technology_BV      = (0x00, 0x20, 0x40)
    Touched_By_Sound_GmbH           = (0x00, 0x20, 0x41)
    DSP_Arts                        = (0x00, 0x20, 0x42)
    Phil_Rees_Music_Tech            = (0x00, 0x20, 0x43)
    Stamer_Musikanlagen_GmbH        = (0x00, 0x20, 0x44)
    Soundart_Musical_Muntaner       = (0x00, 0x20, 0x45)
    C_Mexx_Software                 = (0x00, 0x20, 0x46)
    Klavis_Technologies             = (0x00, 0x20, 0x47)
    Noteheads_AB                    = (0x00, 0x20, 0x48)
    Algorithmix                     = (0x00, 0x20, 0x49)
    Skrydstrup_RD                   = (0x00, 0x20, 0x4A)
    Professional_Audio_Company      = (0x00, 0x20, 0x4B)
    DBTECH                          = (0x00, 0x20, 0x4C)
    Vermona                         = (0x00, 0x20, 0x4D)
    Nokia                           = (0x00, 0x20, 0x4E)
    Wave_Idea                       = (0x00, 0x20, 0x4F)
    Hartmann_GmbH                   = (0x00, 0x20, 0x50)
    Lions_Tracs                     = (0x00, 0x20, 0x51)
    Analogue_Systems                = (0x00, 0x20, 0x52)
    Focal_JMlab                     = (0x00, 0x20, 0x53)
    Ringway_Electronics_Chang_Zhou  = (0x00, 0x20, 0x54)
    Faith_Technologies_Digiplug     = (0x00, 0x20, 0x55)
    Showwork                        = (0x00, 0x20, 0x56)
    Manikin_Electoronic             = (0x00, 0x20, 0x57)
    _1_Come_Tech                    = (0x00, 0x20, 0x58)
    Phonic_Corp                     = (0x00, 0x20, 0x59)
    Lake_Technology                 = (0x00, 0x20, 0x5A)
    Silansys_Technologies           = (0x00, 0x20, 0x5B)
    Winbond_Electronics             = (0x00, 0x20, 0x5C)
    Cinetix_Medien_und_Interface_GmbH = (0x00, 0x20, 0x5D)
    AG_Soluzioni_Digitali             = (0x00, 0x20, 0x5E)
    Sequentix_Music_Systems           = (0x00, 0x20, 0x5F)
    Oram_Pro_Audio                    = (0x00, 0x20, 0x60)
    Be4_Ltd                           = (0x00, 0x20, 0x61)
    Infection_Music                   = (0x00, 0x20, 0x62)
    Central_Music_Co_CME              = (0x00, 0x20, 0x63)
    GenoQs_Machines                   = (0x00, 0x20, 0x64)
    Medialon                          = (0x00, 0x20, 0x65)
    Waves_Audio_Ltd                   = (0x00, 0x20, 0x66)
    Jerash_Labs                       = (0x00, 0x20, 0x67)
    Da_Fact                           = (0x00, 0x20, 0x68)
    Elby_Designs                      = (0x00, 0x20, 0x69)
    Spectral_Audio                    = (0x00, 0x20, 0x6A)
    Arturia                           = (0x00, 0x20, 0x6B)
    Vixid                             = (0x00, 0x20, 0x6C)
    C_Thru_Music                      = (0x00, 0x20, 0x6D)
    CRIMSON_TECHNOLOGY_INC            = (0x00, 0x40, 0x00)
    SOFTBANK_MOBILE_CORP              = (0x00, 0x40, 0x01)
    DM_HOLDINGS_INC                   = (0x00, 0x40, 0x03)
    XING_INC                          = (0x00, 0x40, 0x04)
    Pioneer_DJ_Corporation            = (0x00, 0x40, 0x05)
