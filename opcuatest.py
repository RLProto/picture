import time
from opcua import Client, ua

server_url = 'opc.tcp://10.18.12.185:49324'
tag_path = "ns=2;s=PROCESSO.PLC.MACERACAO.TEMPERATURA_SUPERIOR_M2"

class SubHandler(object):
    """
    Subscription Handler class to handle events for a subscription.
    """
    def datachange_notification(self, node, val, data):
        """
        Called when a subscribed variable changes value.
        """
        print(f"Data change on {node}: New value = {val}")

def main():
    client = Client(server_url)
    try:
        client.connect()
        print(f"Connected to {server_url}")

        # Setting up a subscription
        handler = SubHandler()
        sub = client.create_subscription(1000, handler)  # 1000 milliseconds update rate

        # Subscribing to a variable node
        tag_node = client.get_node(tag_path)
        sub.subscribe_data_change(tag_node)

        print("Subscription setup complete. Monitoring changes, press Ctrl+C to exit.")
        while True:
            time.sleep(1)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.disconnect()
        print("Client disconnected.")

if __name__ == "__main__":
    main()
