import logging
import tkinter as tk
from tkinter import ttk, messagebox
from excepciones import ErrorServicioBase
from entidades import Cliente
from servicios import MantenimientoHardware, SoporteSoftware
from gestor import GestorServicios


class ServiceQuoteApp:
    """Interfaz Gráfica (GUI) en inglés para gestión, cotización y simulaciones."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SoftwareFJ - IT Service Management & Simulation System (Group 2204)")
        self.root.geometry("720x580")
        self.root.resizable(False, False)

        self.gestor = GestorServicios()
        self._cargar_datos_iniciales()
        self._construir_interfaz()

    def _cargar_datos_iniciales(self) -> None:
        self.gestor.agregar_servicio(
            MantenimientoHardware("SRV-01", "Laptop Preventive Maintenance", 45.0, "Laptop", True)
        )
        self.gestor.agregar_servicio(
            SoporteSoftware("SRV-02", "OS & Drivers Installation", 35.0, False, True)
        )
        self.gestor.agregar_servicio(
            MantenimientoHardware("SRV-03", "Server Rack Diagnostics", 80.0, "Server", False)
        )

    def _construir_interfaz(self) -> None:
        header = tk.Label(
            self.root,
            text="IT Service Quoter, Bookings & Simulation Engine",
            font=("Segoe UI", 15, "bold"),
            pady=10,
        )
        header.pack()

        # Frame: Manual Quote & Booking
        frame_form = tk.LabelFrame(self.root, text="Single Service Booking", padx=15, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Client Name:").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_cliente = tk.Entry(frame_form, width=25)
        self.entry_cliente.insert(0, "John Doe")
        self.entry_cliente.grid(row=0, column=1, sticky="w", padx=10)

        tk.Label(frame_form, text="Client Email:").grid(row=0, column=2, sticky="w", pady=4)
        self.entry_email = tk.Entry(frame_form, width=25)
        self.entry_email.insert(0, "john.doe@example.com")
        self.entry_email.grid(row=0, column=3, sticky="w", padx=5)

        tk.Label(frame_form, text="Select Service:").grid(row=1, column=0, sticky="w", pady=4)
        self.combo_servicios = ttk.Combobox(frame_form, width=48, state="readonly")
        self.combo_servicios["values"] = [
            f"{s.codigo_servicio} - {s.describir_servicio()}" for s in self.gestor.obtener_todos()
        ]
        self.combo_servicios.current(0)
        self.combo_servicios.grid(row=1, column=1, columnspan=3, sticky="w", padx=10)

        tk.Label(frame_form, text="Duration (Hours):").grid(row=2, column=0, sticky="w", pady=4)
        self.entry_duracion = tk.Entry(frame_form, width=15)
        self.entry_duracion.insert(0, "2.0")
        self.entry_duracion.grid(row=2, column=1, sticky="w", padx=10)

        tk.Label(frame_form, text="Discount (%):").grid(row=2, column=2, sticky="w", pady=4)
        self.entry_descuento = tk.Entry(frame_form, width=15)
        self.entry_descuento.insert(0, "0")
        self.entry_descuento.grid(row=2, column=3, sticky="w", padx=5)

        self.var_iva = tk.BooleanVar(value=True)
        tk.Checkbutton(frame_form, text="Include VAT / Tax (19%)", variable=self.var_iva).grid(
            row=3, column=1, sticky="w", padx=10, pady=4
        )

        # Action Buttons
        frame_btns = tk.Frame(self.root, pady=8)
        frame_btns.pack()

        tk.Button(
            frame_btns,
            text="Calculate & Book Single Service",
            command=self._procesar_cotizacion,
            bg="#0056b3",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=5,
        ).pack(side="left", padx=10)

        tk.Button(
            frame_btns,
            text="Run 12 Batch Simulations & Generate Log",
            command=self._ejecutar_simulaciones,
            bg="#198754",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=5,
        ).pack(side="left", padx=10)

        # Output Log / Console Box
        frame_res = tk.LabelFrame(self.root, text="Execution Results & Audit Log Output", padx=10, pady=10)
        frame_res.pack(fill="both", expand=True, padx=20, pady=8)

        self.txt_resultado = tk.Text(frame_res, height=13, font=("Consolas", 9), state="disabled")
        self.txt_resultado.pack(fill="both", expand=True)

    def _mostrar_texto(self, contenido: str) -> None:
        self.txt_resultado.config(state="normal")
        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END, contenido)
        self.txt_resultado.config(state="disabled")

    def _procesar_cotizacion(self) -> None:
        try:
            nombre = self.entry_cliente.get().strip()
            email = self.entry_email.get().strip()
            cliente = Cliente("CLI-MANUAL", nombre, email)

            seleccion = self.combo_servicios.get()
            codigo = seleccion.split(" - ")[0]
            duracion = float(self.entry_duracion.get())
            descuento = float(self.entry_descuento.get())
            aplicar_iva = self.var_iva.get()

            reserva = self.gestor.registrar_reserva(
                "RES-MANUAL", cliente, codigo, duracion, descuento, aplicar_iva
            )
        except ValueError as err:
            logging.error(f"Manual input parse error: {err}")
            messagebox.showerror("Input Error", "Duration and Discount must be valid numeric values.")
            self._mostrar_texto("ERROR: Invalid numeric format entered in form.")
        except ErrorServicioBase as err:
            messagebox.showwarning("Business Rule Validation", str(err))
            self._mostrar_texto(f"VALIDATION BLOCKED: {err}\n(Event recorded in app_events.log)")
        else:
            resumen = (
                f"=== BOOKING CONFIRMED ===\n"
                f"Booking ID  : {reserva.reserva_id}\n"
                f"Client      : {cliente}\n"
                f"Service     : {reserva.servicio.describir_servicio()}\n"
                f"Duration    : {duracion} hrs | Discount: {descuento}% | VAT Included: {aplicar_iva}\n"
                f"FINAL TOTAL : ${reserva.total:,.2f} USD\n"
                f"Status      : Saved to app_events.log"
            )
            self._mostrar_texto(resumen)
        finally:
            logging.info("GUI single booking action cycle completed.")

    def _ejecutar_simulaciones(self) -> None:
        resultados = self.gestor.ejecutar_simulaciones_lote()
        salida = "=== 12 BATCH SIMULATIONS REPORT (Saved to app_events.log) ===\n\n" + "\n".join(resultados)
        self._mostrar_texto(salida)
        messagebox.showinfo(
            "Simulations Completed",
            "12 test cases (valid & invalid) executed.\nFull audit trail saved to 'app_events.log'.",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ServiceQuoteApp(root)
    root.mainloop()