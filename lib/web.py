import network
from lib.microdot import Microdot, redirect
import usocket as socket
import asyncio

AP_IP = "192.168.0.1"
SSID = 'BeepBoop'

async def start_access_point(ssid: str = SSID):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    while not ap_if.active():
        print("Waiting for access point to turn on")
        ap_if.active(True)
        await asyncio.sleep(1)
    ap_if.ifconfig(
        (AP_IP, "255.255.255.0", AP_IP, AP_IP)
    )
    ap_if.config(essid=ssid, authmode=network.AUTH_OPEN)
    print("AP mode configured:", ap_if.ifconfig())
    return ap_if

async def dns_handler(ip_address: str = AP_IP):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.bind(("0.0.0.0", 53))
    print("DNS server is running on port 53")

    while True:
        try:
            data, addr = sock.recvfrom(512)
            print("Received DNS query from:", addr)

            transaction_id = data[:2]  # Transaction ID (2 bytes)
            flags = b'\x81\x80'  # Standard DNS response flags (no error)
            qdcount = b'\x00\x01'  # Number of questions
            ancount = b'\x00\x01'  # Number of answers

            dns_header = transaction_id + flags + qdcount + ancount + b'\x00\x00' + b'\x00\x00'
            question = data[12:]  # Copy original question

            # Construct DNS response with the specified IP address
            dns_response = dns_header + question
            dns_response += b'\xc0\x0c'  # Pointer to domain name in question
            dns_response += b'\x00\x01'  # Type A record
            dns_response += b'\x00\x01'  # Class IN
            dns_response += b'\x00\x00\x00\x3c'  # TTL (60 seconds)
            dns_response += b'\x00\x04'  # Data length (4 bytes for IPv4)
            dns_response += bytes(map(int, ip_address.split(".")))  # Append IP address

            sock.sendto(dns_response, addr)
            print("Sent DNS response to:", addr)

        except OSError:
            await asyncio.sleep(0.1)  # Short delay to allow other tasks to run

webpage = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control Panel</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-family: Arial, sans-serif;
        }
        button {
            width: 100px;
            height: 50px;
            margin: 10px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>
<body>

    <h1>Control Panel</h1>

    <div>
        <button onclick="sendCommand('forward')">Forward</button>
        <button onclick="sendCommand('reverse')">Reverse</button>
    </div>
    <div>
        <button onclick="sendCommand('left')">Left</button>
        <button onclick="sendCommand('right')">Right</button>
    </div>
    <div>
        <button onclick="sendCommand('stop')">Stop</button>
    </div>

    <script>
        async function sendCommand(command) {
            await fetch(`/command`, {
                method: 'POST', 
                body: JSON.stringify({ 'command': command }),
                headers: {
                    "Content-Type": "application/json"
                }
            })
        }
    </script>
</body>
</html>
"""

app = Microdot()

@app.route('/')
async def index(_request):
    return webpage, 200, {'Content-Type': 'text/html'}


@app.get('/<path:path>')
def catch_all(request, path):
    print("***CATCHALL***\n" + str(request))
    return redirect("http://bot.bot/")