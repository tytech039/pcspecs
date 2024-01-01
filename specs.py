import platform
import psutil
import socket
import cpuinfo
import os
import GPUtil  # Importing GPUtil for GPU information

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_data = {
            "GPU Name": gpu.name,
            "GPU ID": gpu.id,
            "GPU Load": f"{gpu.load * 100}%",
            "GPU Free Memory": f"{gpu.memoryFree} MB",
            "GPU Used Memory": f"{gpu.memoryUsed} MB",
            "GPU Total Memory": f"{gpu.memoryTotal} MB",
            "GPU Temperature": f"{gpu.temperature} °C"
        }
        gpu_info.append(gpu_data)
    return gpu_info

def get_system_specs(include_network_info=False):
    try:
        # Getting detailed CPU information
        cpu_info = cpuinfo.get_cpu_info()

        # System specifications
        specs = {
            "Processor Name": cpu_info['brand_raw'],
            "Processor": platform.processor(),
            "Architecture": platform.machine(),
            "Platform": platform.system(),
            "Platform Version": platform.version(),
            "Platform Release": platform.release(),
            "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3))} GB",
            "GPUs (NVDIA)": get_gpu_info()  # Adding GPU information
        }

        # Adding network information if requested
        if include_network_info:
            specs["Hostname"] = socket.gethostname()
            specs["IP Address"] = socket.gethostbyname(socket.gethostname())

        return specs
    except Exception as e:
        return {"Error": str(e)}

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        for key, value in data.items():
            if isinstance(value, list):
                file.write(f"{key}:\n")
                for item in value:
                    for subkey, subvalue in item.items():
                        file.write(f"    {subkey}: {subvalue}\n")
            else:
                file.write(f"{key}: {value}\n")

def ask_user_network_info():
    response = input("Include hostname and IP address? (Y/N): ")
    return response.strip().lower() == 'y'

def main():
    include_network = ask_user_network_info()
    system_specs = get_system_specs(include_network)
    write_to_file("pcspecs.txt", system_specs)

    # Printing to console
    for key, value in system_specs.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                for subkey, subvalue in item.items():
                    print(f"    {subkey}: {subvalue}")
        else:
            print(f"{key}: {value}")

    # Pause with a "Press any key to continue" prompt
    input("Press ENTER to continue...")

if __name__ == "__main__":
    main()
