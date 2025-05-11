import datetime
from functools import partial
import signal
import argparse, sys, os
import time
import mido

from helpers import MidiHelpers, Helpers
from midimsg import MidiMsg


class MidiMator:
    def cmd_list_port():
        ports = MidiHelpers.get_midi_ports()
        print('  #| IN|OUT| PORT NAME')
        num = 1
        for port in ports:
            inport = 'X' if 'input_idx' in ports[port] else '-'
            outport = 'X' if 'output_idx' in ports[port] else '-'
            print(str(num).rjust(3)+'| '+inport+' | '+outport+' | '+port)
            num += 1

    def cmd_transfer(input_port, output_port, hexa:bool):
        inport = MidiHelpers.get_or_create_port(input_port, False)
        outport = MidiHelpers.get_or_create_port(output_port, True)

        if inport and outport:
            inport[0].callback = partial(MidiMator.__callback_receive, inport=inport, outport=outport, hexa=hexa)
            # Enter infinite loop (until CTRL+C is pressed)
            signal.signal(signal.SIGINT, MidiMator.__signal_handler)
            while True:
                time.sleep(1)

    def cmd_capture(input_port, hexa:bool):
        inport = MidiHelpers.get_or_create_port(input_port, False)

        if inport:
            inport[0].callback = partial(MidiMator.__callback_receive, inport=inport, hexa=hexa)
            # Enter infinite loop (until CTRL+C is pressed)
            signal.signal(signal.SIGINT, MidiMator.__signal_handler)
            while True:
                time.sleep(1)

    def cmd_send(output_port, msg:list, hexa:bool):
        bytes_msg = []
        for value in msg:
            midivalue = Helpers.str_to_int(value)
            if midivalue==None or midivalue<0 or midivalue>255:
                print('error: invalid value in midi message "'+str(value)+'"', file=sys.stderr)
                return
            bytes_msg.append(midivalue)

        outport = MidiHelpers.get_or_create_port(output_port, True, False)

        if outport:
            MidiHelpers.send_bytes(outport, bytes_msg, hexa)
            outport[0].close()

    def __callback_receive(midimsg:mido.Message, inport, outport = None, hexa = False):
        outstr = ''
        if outport:
            outport[0].send(midimsg)
            outstr = '", to: "'+outport[1]+'"'
        msg:MidiMsg = MidiMsg.from_list(midimsg.bytes())
        msg_str = (msg.to_raw_string(hexa) + ' = ' + msg.to_string(hexa)) if msg else 'INVALID MESSAGE'
        print(Helpers.get_timestr(datetime.datetime.now())+' | '+ msg_str + ' (from: "'+inport[1]+'"'+outstr+')')

    def __signal_handler(signal, frame):
        """Handler for Ctrl-C"""
        sys.exit(0)

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
        MidiMator.cmd_list_port()
    elif args.cmd=='transfer':
        MidiMator.cmd_transfer(args.input_port, args.output_port, args.H)
    elif args.cmd=='capture':
        MidiMator.cmd_capture(args.input_port, args.H)
    elif args.cmd=='send':
        MidiMator.cmd_send(args.output_port, args.value, args.H)

if __name__ == "__main__":
   main(sys.argv[1:])