import signal
import argparse, sys, os
import time
import rtmidi

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
    
    def msg_to_string(midimsg:list):
        return '[' + ', '.join('0x%02X' % x for x in midimsg) + ']'

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

def receive_callback(value, outport):
    """Function called when MIDI data is received"""
    midimsg = value[0]
    print('received message : '+MidiHelpers.msg_to_string(midimsg))
    if outport:
        outport.send_message(midimsg)

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
    port = str_to_int(port)
    if port != None:
        if port>0 and port<=len(ports):
            port_name = list(ports.keys())[port-1]
        else:
            print('error: given number ('+str(port)+') for midi port is out of range', file=sys.stderr)
            return None
    
    if port_name:
        if out:
            if not 'output_idx' in ports[port_name]:
                print('error: "'+port_name+'" is not an outport port', file=sys.stderr)
                return None
            port_idx = ports[port_name]['output_idx']
        else:
            if not 'input_idx' in ports[port_name]:
                print('error: "'+port_name+'" is not an input port', file=sys.stderr)
                return None
            port_idx = ports[port_name]['input_idx']
    
    if out:
        midi = rtmidi.MidiOut()
    else:
        midi = rtmidi.MidiIn()

    if port_name:
        midi.open_port(port_idx)
    elif create_port_if_needed:
        # create a virtual port
        midi.open_virtual_port(port)
        port_name = port
    else:
        del midi
        return None
    
    return (midi, port_name)

def cmd_transfer(input_port, output_port):
    inport = get_or_create_port(input_port, False)
    outport = get_or_create_port(output_port, True)

    if inport and outport:
        inport[0].set_callback(receive_callback, outport)
        inport[0].ignore_types(False, False, False)
        # Enter infinite loop (until CTRL+C is pressed)
        signal.signal(signal.SIGINT, signal_handler)
        while True:
            time.sleep(1)

def cmd_capture(input_port):
    inport = get_or_create_port(input_port, False)

    if inport:
        inport[0].set_callback(receive_callback, None)
        inport[0].ignore_types(False, False, False)
        # Enter infinite loop (until CTRL+C is pressed)
        signal.signal(signal.SIGINT, signal_handler)
        while True:
            time.sleep(1)

def cmd_send(output_port, msg:list):
    outport = get_or_create_port(output_port, True, False)

    if outport:
        midimsg = []
        for value in msg:
            midivalue = str_to_int(value)
            if midivalue==None:
                print('error: invalid value in midi message "'+str(value)+'"', file=sys.stderr)
                return
            midimsg.append(midivalue)
        print('sending message '+MidiHelpers.msg_to_string(midimsg)+' to "'+outport[1]+'"')
        if len(midimsg)>3:
            midimsg.insert(0, 0xF0)
        outport[0].send_message(midimsg)
        outport = outport[0]
        del outport

def main(argv):
    argParser = argparse.ArgumentParser(description="Midimator can transfer midi messages from one interface to another")
    subparsers = argParser.add_subparsers(title="commands", dest="cmd", description="use -h argument after command name to get help", required=True)

    parser_list_cmd = subparsers.add_parser('list', help='print the list of MIDI ports available on this system', argument_default="test")

    parser_transfer_cmd = subparsers.add_parser('transfer', help='transfer midi messages from one port to another')
    parser_transfer_cmd.add_argument('input_port', help="name (or number) of the midi port to read messages from. If the given port does not exists, a virtual port is created", type=str)
    parser_transfer_cmd.add_argument('output_port', help="name (or number) of the midi port to write messages to. If the given port does not exists, a virtual port is created", type=str)

    parser_transfer_cmd = subparsers.add_parser('capture', help='capture and print received midi messages')
    parser_transfer_cmd.add_argument('input_port', help="name (or number) of the midi port to read messages from. If the given port does not exists, a virtual port is created", type=str)

    parser_transfer_cmd = subparsers.add_parser('send', help='send a midi message')
    parser_transfer_cmd.add_argument('output_port', help="name (or number) of the midi port to write the message to", type=str)
    parser_transfer_cmd.add_argument('value', help="Integer value to add to the MIDI message, that may be represented as an hex value (like 0x80)", type=str, nargs='+')

    args = argParser.parse_args()

    if args.cmd=='list':
        cmd_list_port()
    elif args.cmd=='transfer':
        cmd_transfer(args.input_port, args.output_port)
    elif args.cmd=='capture':
        cmd_capture(args.input_port)
    elif args.cmd=='send':
        cmd_send(args.output_port, args.value)

if __name__ == "__main__":
   main(sys.argv[1:])