import pika
import subprocess
import traceback

# RabbitMQ connection parameters
rabbitmq_credentials = pika.PlainCredentials('RajaMpHcm', 'Fathi&27')
rabbitmq_parameters = pika.ConnectionParameters('192.168.1.60', credentials=rabbitmq_credentials)
queue_name = 'autoexe'


def execute_powershell_command(command):
    try:
        print(f"Executing PowerShell command: {command}")

        completed_process = subprocess.run(["powershell.exe", "-Command", command], capture_output=True, text=True)
        if completed_process.returncode == 0:
            print("PowerShell command executed successfully.")
            print("Command output:")
            print(completed_process.stdout)
        else:
            print("PowerShell command failed.")
            print("Error output:")
            print(completed_process.stderr)

    except Exception as e:
        print(f"An error occurred during PowerShell execution: {e}")
        traceback.print_exc()

def callback(ch, method, properties, body):
    print(f" [x] Received message")

    try:
        powershell_command = body.decode('utf-8')
        print(f"Received PowerShell Command: {powershell_command}")

        if powershell_command.strip():
            print("Executing PowerShell command...")
            execute_powershell_command(powershell_command)
        else:
            print("Received PowerShell command is empty.")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


def consume_messages():
    try:
        connection = pika.BlockingConnection(rabbitmq_parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f' [*] Waiting for messages on queue "{queue_name}". To exit, press CTRL+C')
        channel.start_consuming()

    except KeyboardInterrupt:
        print(" [*] Exiting. Keyboard interrupt received.")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    finally:
        if connection is not None and connection.is_open:
            connection.close()


if __name__ == '__main__':
    consume_messages()
