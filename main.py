from flask import Flask, request, jsonify
from flask_cors import CORS
from scapy.all import sendp, Ether, ARP

CHANNEL_ID = bytes([149])
event_id = 0

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Network interface configuration
interface = None  # Change to match your actual network interface

def send_arp_with_extra_data(custom_data):
    global event_id
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
    arp = ARP(op=1, hwsrc=ether.src, psrc="0.0.0.0", hwdst="00:00:00:00:00:00", pdst="0.0.0.0")
    event_id_buf = bytes([event_id])
    extra_data = CHANNEL_ID + event_id_buf + custom_data.encode('utf-8')
    packet = ether / arp / extra_data
    event_id = (event_id + 1) % 256

    # Send packet out on specified interface
    sendp(packet, iface=interface)
    print(f"Sent ARP packet with extra data: {custom_data}")

# Define the API endpoint
@app.route('/', methods=['POST'])
def handle_broadcast():
    data = request.data.decode('utf-8')  # Get raw data from request
    if not data:
        return jsonify({"error": "No data provided in request body"}), 400

    try:
        send_arp_with_extra_data(data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": e}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5031, debug=True)
