import datetime
from functools import partial
import signal
import argparse, sys, os
import time
import mido

from midihelpers import MidiHelpers, get_timestr


def str_to_int(value:str, default:int = None)->int:
    """convert a string to an integer
    The string can contain an hexadecimal representation (i.e. 0x80)
    returns default value in case of conversion error
    """
    try:
        if value.startswith('0x'):
            result = int(value[2:], base=16)
        else:
            result = int(value)
    except:
        return default
    return result

def signal_handler(signal, frame):
    """Handler for Ctrl-C"""
    sys.exit(0)

def callback_receive(midimsg, inport, outport = None, hexa = False):
    outstr = ''
    if outport:
        outport[0].send(midimsg)
        outstr = '", to: "'+outport[1]+'"'
    print(get_timestr(datetime.datetime.now())+' | '+MidiHelpers.msg_to_string(midimsg,hexa)+ ' (from: "'+inport[1]+'"'+outstr+')')
    
def cmd_list_port():
    ports = MidiHelpers.get_midi_ports()
    print('  #| IN|OUT| PORT NAME')
    num = 1
    for port in ports:
        inport = 'X' if 'input_idx' in ports[port] else '-'
        outport = 'X' if 'output_idx' in ports[port] else '-'
        print(str(num).rjust(3)+'| '+inport+' | '+outport+' | '+port)
        num += 1

def get_or_create_port(port, out, create_port_if_needed = True):
    """ return a rtmidi.MidiIn or rtmidi.MidiOut that must be deleted with del keyword

    Args:
        port (_type_): _description_
        out (bool, optional): _description_. Defaults to False.

    Returns:
        any|None: _description_
    """
    port_name = None
    ports:dict = MidiHelpers.get_midi_ports()
    port_ = str_to_int(port)
    if port_ != None:
        if port_>0 and port_<=len(ports):
            port_name = list(ports.keys())[port_-1]
        else:
            print('error: given number ('+str(port_)+') for midi port is out of range', file=sys.stderr)
            return None
    
    virtual = False
    if port_name:
        if out:
            if not 'output_idx' in ports[port_name]:
                print('error: "'+port_name+'" is not an outport port', file=sys.stderr)
                return None
        else:
            if not 'input_idx' in ports[port_name]:
                print('error: "'+port_name+'" is not an input port', file=sys.stderr)
                return None
    elif create_port_if_needed:
        port_name = port
        virtual = True
    else:
        return None
    
    if out:
        midi = mido.open_output(port_name, virtual=virtual)
    else:
        midi = mido.open_input(port_name, virtual=virtual)
    
    return (midi, port_name)

def cmd_transfer(input_port, output_port, hexa:bool):
    inport = get_or_create_port(input_port, False)
    outport = get_or_create_port(output_port, True)

    if inport and outport:
        inport[0].callback = partial(callback_receive, inport=inport, outport=outport, hexa=hexa)
        # Enter infinite loop (until CTRL+C is pressed)
        signal.signal(signal.SIGINT, signal_handler)
        while True:
            time.sleep(1)

def cmd_capture(input_port, hexa:bool):
    inport = get_or_create_port(input_port, False)

    if inport:
        inport[0].callback = partial(callback_receive, inport=inport, hexa=hexa)
        # Enter infinite loop (until CTRL+C is pressed)
        signal.signal(signal.SIGINT, signal_handler)
        while True:
            time.sleep(1)

def cmd_send(output_port, msg:list, hexa:bool):
    bytes_msg = []
    for value in msg:
        midivalue = str_to_int(value)
        if midivalue==None or midivalue<0 or midivalue>255:
            print('error: invalid value in midi message "'+str(value)+'"', file=sys.stderr)
            return
        bytes_msg.append(midivalue)

    outport = get_or_create_port(output_port, True, False)

    if outport:
        MidiHelpers.send_bytes(outport, bytes_msg, hexa)
        outport[0].close()

def main(argv):
    argParser = argparse.ArgumentParser(description="Midimator can transfer midi messages from one interface to another")
    subparsers = argParser.add_subparsers(title="commands", dest="cmd", description="use -h argument after command name to get help", required=True)

    parser_list_cmd = subparsers.add_parser('list', help='print the list of MIDI ports available on this system', argument_default="test")

    parser = subparsers.add_parser('transfer', help='transfer midi messages from one port to another')
    parser.add_argument('input_port', help="name (or number) of the midi port to read messages from. If the given port does not exists, a virtual port is created", type=str)
    parser.add_argument('output_port', help="name (or number) of the midi port to write messages to. If the given port does not exists, a virtual port is created", type=str)
    parser.add_argument('-H', help='integer values are logged in hexa format', action='store_true')

    parser = subparsers.add_parser('capture', help='capture and print received midi messages')
    parser.add_argument('input_port', help="name (or number) of the midi port to read messages from. If the given port does not exists, a virtual port is created", type=str)
    parser.add_argument('-H', help='integer values are logged in hexa format', action='store_true')

    parser = subparsers.add_parser('send', help='send a midi message')
    parser.add_argument('output_port', help="name (or number) of the midi port to write the message to", type=str)
    parser.add_argument('value', help="Integer value to add to the MIDI message, that may be represented as an hex value (like 0x80)", type=str, nargs='+')
    parser.add_argument('-H', help='integer values are logged in hexa format', action='store_true')

    args = argParser.parse_args()

    if args.cmd=='list':
        cmd_list_port()
    elif args.cmd=='transfer':
        cmd_transfer(args.input_port, args.output_port, args.H)
    elif args.cmd=='capture':
        cmd_capture(args.input_port, args.H)
    elif args.cmd=='send':
        cmd_send(args.output_port, args.value, args.H)

if __name__ == "__main__":
   main(sys.argv[1:])