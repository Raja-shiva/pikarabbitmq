import pika
import subprocess
import time

rabbitmq_credentials = pika.PlainCredentials('RajaMpHcm', 'Fathi&27')
rabbitmq_parameters = pika.ConnectionParameters('192.168.1.60', credentials=rabbitmq_credentials)

def send_data_to_rabbitmq(powershell_script, queue_name='autoexe'):
    # Remaining code for sending data to RabbitMQ remains unchanged
    connection = None

    try:
        connection = pika.BlockingConnection(rabbitmq_parameters)
        channel = connection.channel()

        channel.queue_declare(queue=queue_name)

        body = powershell_script.encode('utf-8')

        channel.basic_publish(exchange='', routing_key=queue_name, body=body)

        print("Data sent to the queue")

    except pika.exceptions.AMQPError as amqp_error:
        print(f"AMQP Error: {amqp_error}")
    finally:
        if connection is not None:
            connection.close()


# def simulate_progress():
#     for i in range(1, 21):
#         print(f"Downloading... {i * 5}%")
#         time.sleep(1)  # Simulating download progress
#
#     for i in range(1, 21):
#         print(f"Installing... {i * 5}%")
#         time.sleep(1)  # Simulating installation progress
#

def prepare_and_send_script():
    # Define the desired installation path
    installation_path = r"C:\Path\To"

    # Insert the URL directly
    url = "https://win.desktop.evernote.com/builds/Evernote-latest.exe"

    # Form the PowerShell script with the installation command
    powershell_script = f'''
    $url = "{url}"
    $installerPath = "{installation_path}\\Evernote-latest.exe"
    $installArgs = "/S"  # or "/VERYSILENT" depending on the Evernote installer

    Write-Host "Downloading Evernote..."
    Start-BitsTransfer -Source $url -Destination $installerPath  # Download using BITS transfer

    Write-Host "Installing Evernote silently..."
    Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait  # Run the installer silently
    '''

    # Print PowerShell commands and URL
    print(f"Powershell Script:\n{powershell_script}\n")
    print(f"URL: {url}\n")

    # Sending the script to RabbitMQ
    send_data_to_rabbitmq(powershell_script)

    # Simulate download and installation progress
    # simulate_progress()

if __name__ == '__main__':
    prepare_and_send_script()
