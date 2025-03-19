import mido
from pythonosc.udp_client import SimpleUDPClient


solo = [0] * 127
mute = [0] * 127
rec = [0] * 127
select = [0] * 127

def send_osc_message(ip, port, osc_address, osc_message):
    # Create a UDP client
    client = SimpleUDPClient(ip, port)

    # Send OSC message
    client.send_message(osc_address, osc_message)
    print(f"Message sent to {ip}:{port} with address {osc_address} and message {osc_message}")


def midi_callback(message):
    ip = "192.168.1.108"  # IP address of the receiver (e.g., localhost)
    port = 8004  # Port number of the receiver
    osc_address = "/example/address"
    if message.type == 'control_change':
        print(f"Channel: {message.channel}")
        print(f"Control: {message.control}")
        print(f"Value: {message.value}")
        print("------------------------")
        val = 0


        v = message.value
        chan = message.channel
        control = message.control
        if(chan == 0):
            #faders
            if(v == 0):
                val = -149
            elif(v > 63):
                val = ((v-63)/3.2)-10
                #val = (-(10-(message.value/12.7)))
            elif(v > 32):
                val = ((v - 32) / 1.058)-40
            elif (v > 0):
                val = ((v) / 0.2939) - 148

            print(val)
            send_osc_message(ip, port, "/Input_Channels/" + str(message.control) + "/fader", val)
        elif(chan == 1):
            #dials
            val = 0



        elif(chan == 2):
            #select
            val = 0

        elif(chan == 3):
            #rec
            val = 0

        elif(chan == 4):
            #solo
            val = 0

            if(v > 1):
                if(solo[control] == 0):
                    solo[control] = 1
                    val = 1
                elif(solo[control] == 1):
                    solo[control] = 0
                    val = 0

                send_osc_message(ip, port, "/Input_Channels/" + str(message.control) + "/solo", val)

        elif(chan == 5):
            #mute
            val = 0
            if (v > 1):
                if (mute[control] == 0):
                    mute[control] = 1
                    val = 1
                elif (mute[control] == 1):
                    mute[control] = 0
                    val = 0

                send_osc_message(ip, port, "/Input_Channels/" + str(message.control) + "/mute", val)
        elif(chan == 6):
            #misc
            val = 0
    else:
        # For other message types, you can print them as they are
        print(f'MIDI message received: {message}')


def list_midi_ports():
    print("Available MIDI input ports:")
    for port in mido.get_input_names():
        print(port)


def main():
    list_midi_ports()

    # Open the first available MIDI input port
    with mido.open_input(mido.get_input_names()[0]) as midi_in:
        print("Listening for MIDI messages...")

        # Receive and process MIDI messages
        for message in midi_in:
            midi_callback(message)


if __name__ == '__main__':
    main()
