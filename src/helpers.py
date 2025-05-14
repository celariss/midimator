import datetime, sys
from enum import Enum
import mido

class Helpers:
    def get_timestr(time:datetime.datetime)->str:
        return time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    
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
    
    def int_to_str(value:int, hexa:bool)->str:
        if hexa:
            return Helpers.hex_to_str(value)
        else:
            return str(value)
        
    def hex_to_str(value:int, pref:str = "0x", suff:str = '')->str:
        return pref+('%02X' % value) + suff

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
    
    def send_bytes(outport, bytes_msg:list, hexa:bool)->bool:
        if len(bytes_msg)>3 and bytes_msg[0] != 0xF0:
            bytes_msg.insert(0, 0xF0)
        try:
            midimsg:mido.Message = mido.Message.from_bytes(bytes_msg)
        except:
            print('error: Invalid midi message '+MidiHelpers.bytes_to_raw_string(bytes_msg,hexa), file=sys.stderr)
            return False
        print(Helpers.get_timestr(datetime.datetime.now())+' | '+MidiHelpers.msg_to_string(midimsg,hexa)+ ' (to: "'+outport[1]+'")')
        outport[0].send(midimsg)
        return True
    
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

        port_ = Helpers.str_to_int(port)
        if port_ != None:
            if port_>0 and port_<=len(ports):
                port_name = list(ports.keys())[port_-1]
            else:
                print('error: given number ('+str(port_)+') for midi port is out of range', file=sys.stderr)
                return None
        elif port in ports:
            port_name = port
        
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
    