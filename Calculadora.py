import tkinter as tk
from tkinter import messagebox
import ipaddress
import math


def calculate_network_details():
    ip_input = ip_entry.get()
    try:
        # Convertir la entrada en un objeto IPv4Interface
        ip_obj = ipaddress.IPv4Interface(ip_input)
        
        if ip_obj.ip == ip_obj.network.network_address:
            # Si es una IP de red
            host_message.set("La dirección es una red.")
        else:
            # Si es una IP de host
            host_message.set("La dirección es un host.")
        
        # Actualizar los datos calculados
        network_label_value.set(f"{ip_obj.network.network_address}/{ip_obj.network.prefixlen}")  # Agregar el sufijo de subred
        mask_label_value.set(ip_obj.network.netmask)
        hosts_label_value.set(ip_obj.network.num_addresses - 2)
        range_label_value.set(f"{list(ip_obj.network.hosts())[0]} - {list(ip_obj.network.hosts())[-1]}")
        broadcast_label_value.set(ip_obj.network.broadcast_address)

        # Limpiar los resultados de subredes previas
        for widget in subnets_results_frame.winfo_children():
            widget.destroy()

    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce una dirección IP válida en formato CIDR (e.g., 192.168.1.1/24)")


def calculate_subnets():
    ip_input = ip_entry.get()
    subnets_input = subnets_entry.get()

    try:
        ip_obj = ipaddress.IPv4Interface(ip_input)

        if subnets_input:
            subnets = int(subnets_input)
            # Calcular la máscara de subred que se necesita para el número de subredes
            prefix_length = int(math.ceil(math.log(subnets, 2)))
            new_network = ip_obj.network.prefixlen + prefix_length
            subnet_mask = ipaddress.IPv4Network(f'0.0.0.0/{new_network}').netmask
            subnet_hosts = (2 ** (32 - new_network)) - 2  # Excluir la dirección de red y broadcast

            # Mostrar los resultados de la red principal
            hosts_label_value.set(subnet_hosts)
            mask_label_value.set(subnet_mask)

            # Mostrar las subredes
            subnets_result = list(ip_obj.network.subnets(new_prefix=new_network))

            # Limpiar cualquier subred anterior
            for widget in subnets_results_frame.winfo_children():
                widget.destroy()

            # Agregar cada subred en su propio bloque
            for idx, subnet in enumerate(subnets_result, 1):
                subnet_frame = tk.Frame(subnets_results_frame, bg="#DDD6CC", pady=10)
                subnet_frame.pack(fill="x", padx=10, pady=5)

                # ID de subred
                subnet_label = tk.Label(subnet_frame, text=f"Subred {idx}: {subnet.network_address}/{subnet.prefixlen}",
                                        font=("Serif", 16), fg="#19222B", bg="#DDD6CC")
                subnet_label.pack(side="top", padx=10)

                # Rango de host y host disponibles
                subnet_range = f"{list(subnet.hosts())[0]} - {list(subnet.hosts())[-1]}"
                subnet_hosts_available = subnet.num_addresses - 2

                subnet_range_label = tk.Label(subnet_frame, text=f"Rango de Hosts: {subnet_range}", font=("Serif", 16),
                                              fg="#19222B", bg="#DDD6CC")
                subnet_range_label.pack(side="top", padx=10)

                subnet_hosts_label = tk.Label(subnet_frame, text=f"Hosts Disponibles: {subnet_hosts_available}",
                                              font=("Serif", 16), fg="#19222B", bg="#DDD6CC")
                subnet_hosts_label.pack(side="top", padx=10)

                # Dirección de broadcast
                subnet_broadcast_label = tk.Label(subnet_frame, text=f"Broadcast: {subnet.broadcast_address}",
                                                  font=("Serif", 16), fg="#19222B", bg="#DDD6CC")
                subnet_broadcast_label.pack(side="top", padx=10)

        else:
            messagebox.showerror("Error", "Por favor ingresa un número de subredes.")

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa una IP válida.")


# Crear ventana principal
window = tk.Tk()
window.title("Calculadora de Redes IPv4")
window.geometry("900x800")
window.configure(bg="#19222B")

# Título principal
title_label = tk.Label(window, text="Calculadora de Redes IPv4", font=("Serif", 28, "bold"), fg="#BD9240", bg="#19222B")
title_label.pack(pady=20)

# Entrada de datos
entry_frame = tk.Frame(window, bg="#19222B", pady=20)
entry_frame.pack(pady=10)

ip_label = tk.Label(entry_frame, text="Introduce una IP (ej. 192.168.1.0/24):", font=("Serif", 16), fg="#DDD6CC", bg="#19222B")
ip_label.grid(row=0, column=0, padx=10, pady=5)

ip_entry = tk.Entry(entry_frame, font=("Arial", 14), width=25, bg="#DDD6CC", fg="#19222B", relief="flat")
ip_entry.grid(row=0, column=1, padx=10, pady=5)

calculate_button = tk.Button(entry_frame, text="Calcular", font=("Arial", 14, "bold"), bg="#B84357", fg="#DDD6CC",
                             activebackground="#BD9240", activeforeground="#19222B", relief="flat",
                             command=calculate_network_details)
calculate_button.grid(row=0, column=2, padx=10, pady=5)

# Entrada para el número de subredes
subnet_frame = tk.Frame(window, bg="#19222B", pady=10)
subnet_frame.pack(pady=10)

subnets_label = tk.Label(subnet_frame, text="Introduce el número de subredes:", font=("Serif", 16), fg="#DDD6CC", bg="#19222B")
subnets_label.grid(row=0, column=0, padx=10, pady=5)

subnets_entry = tk.Entry(subnet_frame, font=("Arial", 14), width=25, bg="#DDD6CC", fg="#19222B", relief="flat")
subnets_entry.grid(row=0, column=1, padx=10, pady=5)

calculate_button_subnets = tk.Button(subnet_frame, text="Calcular Subredes", font=("Arial", 14, "bold"), bg="#B84357", fg="#DDD6CC",
                                     activebackground="#BD9240", activeforeground="#19222B", relief="flat", command=calculate_subnets)
calculate_button_subnets.grid(row=0, column=2, padx=10, pady=5)

# Botón para abrir el cálculo de subredes
# (Este botón ya no es necesario, ya que ahora la entrada está en la interfaz principal)

# Mensaje de red o host
host_message = tk.StringVar()
host_message_label = tk.Label(window, textvariable=host_message, font=("Serif", 16), fg="#BD9240", bg="#19222B")
host_message_label.pack(pady=10)

# Resultados principales
results_frame = tk.Frame(window, bg="#DDD6CC", bd=2, relief="ridge", padx=20, pady=20)
results_frame.pack(fill="x", padx=20, pady=20)

fields = [
    ("IP de Red", "network_label_value"),
    ("Máscara de Red", "mask_label_value"),
    ("Hosts Disponibles", "hosts_label_value"),
    ("Rango de Hosts", "range_label_value"),
    ("Broadcast", "broadcast_label_value"),
]

variables = {}
for i, (label_text, var_name) in enumerate(fields):
    variables[var_name] = tk.StringVar()
    
    field_frame = tk.Frame(results_frame, bg="#DDD6CC", pady=10)
    field_frame.pack(fill="x", padx=10)

    label = tk.Label(field_frame, text=label_text + ":", font=("Serif", 16), fg="#19222B", bg="#DDD6CC")
    label.pack(side="left", padx=10)
    
    value_label = tk.Label(field_frame, textvariable=variables[var_name], font=("Serif", 16, "bold"), fg="#B84357", bg="#DDD6CC")
    value_label.pack(side="right", padx=10)

# Variables asignadas a las etiquetas dinámicas
network_label_value = variables["network_label_value"]
mask_label_value = variables["mask_label_value"]
hosts_label_value = variables["hosts_label_value"]
range_label_value = variables["range_label_value"]
broadcast_label_value = variables["broadcast_label_value"]

# Resultados de Subredes
subnets_results_frame = tk.Frame(window, bg="#19222B")
subnets_results_frame.pack(fill="both", padx=20, pady=20)

# Iniciar la aplicación
window.mainloop()
