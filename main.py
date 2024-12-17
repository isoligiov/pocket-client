from flask import Flask, request, jsonify
from flask_cors import CORS
from scapy.all import sendp, Ether, ARP, conf

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Network interface configuration
interface = None  # Change to match your actual network interface

def list_interfaces():
    # This will print all available network interfaces
    print("Available network interfaces:")
    print(conf.ifaces)

def send_arp_with_extra_data(custom_data):
    # Construct Ethernet frame
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address

    # Construct ARP packet
    arp = ARP(op=1, hwsrc=ether.src, psrc="0.0.0.0", hwdst="00:00:00:00:00:00", pdst="0.0.0.0")

    # Custom data payload
    extra_data = custom_data.encode('utf-8')

    # Final packet combining Ethernet, ARP, and extra_data
    packet = ether / arp / extra_data

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
        return jsonify({"status": "Data broadcasted via ARP!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5030, debug=True)