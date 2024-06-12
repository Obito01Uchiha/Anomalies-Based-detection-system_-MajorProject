from flask import Flask, render_template
from scapy.all import sniff
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

# Define a callback function to process each packet
def packet_callback(packet):
    data = [
        'Ether' in packet,
        'IP' in packet,
        'TCP' in packet,
        'UDP' in packet,
        'ICMP' in packet,
        'SRC' in packet and packet['SRC'],
        'DST' in packet and packet['DST'],
        'LEN' in packet and len(packet),
    ]
    features.append(data)

features = []

# Define a route to start capturing packets
@app.route('/')
def capture_packets():
    global features
    features = []
    # Start sniffing packets on the network interface
    sniff(prn=packet_callback, count=10000)  # Capture 1000 packets

    # Preprocess the data
    df = pd.DataFrame(features, columns=[
        'Ether', 'IP', 'TCP', 'UDP', 'ICMP', 'SRC', 'DST', 'LEN'
    ])

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Convert SRC and DST columns to numerical values
    df['SRC'] = df['SRC'].apply(lambda x: 1 if x else 0)
    df['DST'] = df['DST'].apply(lambda x: 1 if x else 0)

    # Save the preprocessed data to a file
    df.to_csv('packet_data.csv', index=False)

    return 'Packet capture and preprocessing completed!'

if __name__ == '__main__':
    app.run(debug=True)