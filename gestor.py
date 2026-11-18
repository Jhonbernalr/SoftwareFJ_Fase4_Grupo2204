import logging
from entidades import Servicio, Cliente, Reserva
from excepciones import ErrorServicioBase, ParametroInconsistenteError

# Configuración del archivo de log exigido en la rúbrica
logging.basicConfig(
    filename="app_events.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class GestorServicios:
    """Administra el catálogo, reservas, simulaciones y registro de logs."""

    def __init__(self):
        self._catalogo: dict[str, Servicio] = {}
        self._reservas: list[Reserva] = []

    def agregar_servicio(self, servicio: Servicio) -> None:
        self._catalogo[servicio.codigo_servicio] = servicio
        logging.info(f"Catalog updated: added {servicio.codigo_servicio}")

    def obtener_todos(self) -> list[Servicio]:
        return list(self._catalogo.values())

    def buscar_por_codigo(self, codigo: str) -> Servicio:
        try:
            servicio = self._catalogo[codigo]
        except KeyError as err:
            logging.error(f"Lookup failed for service code '{codigo}'")
            raise ParametroInconsistenteError(f"Service code '{codigo}' does not exist.") from err
        else:
            logging.info(f"Service '{codigo}' retrieved successfully.")
            return servicio
        finally:
            logging.debug(f"Finished lookup operation for code '{codigo}'.")

    def registrar_reserva(
        self,
        reserva_id: str,
        cliente: Cliente,
        codigo_servicio: str,
        duracion: float,
        descuento: float = 0.0,
        aplicar_iva: bool = True,
    ) -> Reserva:
        try:
            servicio = self.buscar_por_codigo(codigo_servicio)
            reserva = Reserva(reserva_id, cliente, servicio, duracion, descuento, aplicar_iva)
        except ErrorServicioBase as err:
            logging.error(f"Simulation/Booking FAILED [{reserva_id}]: {err}")
            raise
        else:
            self._reservas.append(reserva)
            logging.info(
                f"Simulation/Booking SUCCESS [{reserva_id}]: Client='{cliente.nombre}', "
                f"Service='{codigo_servicio}', Total=${reserva.total:.2f} USD"
            )
            return reserva
        finally:
            logging.info(f"Audit checkpoint completed for transaction {reserva_id}.")

    def ejecutar_simulaciones_lote(self) -> list[str]:
        """Ejecuta 12 simulaciones (válidas e inválidas) y registra todo en app_events.log."""
        logging.info("=== STARTING 12 BATCH SIMULATIONS ===")
        resultados: list[str] = []

        # Datos de prueba: 12 escenarios variados
        escenarios = [
            ("SIM-01", "CLI-01", "Carlos Mendez", "carlos@mail.com", "SRV-01", 2.0, 10.0, True),
            ("SIM-02", "CLI-02", "Laura Gomez", "laura@mail.com", "SRV-02", 1.5, 0.0, True),
            ("SIM-03", "CLI-03", "Andres Ruiz", "andres@mail.com", "SRV-03", 3.0, 5.0, True),       # Inválida: SRV-03 no disponible
            ("SIM-04", "CLI-04", "Sofia Torres", "sofia@mail.com", "SRV-01", -2.0, 0.0, True),      # Inválida: duración negativa
            ("SIM-05", "CLI-05", "Diana Ardila", "diana@mail.com", "SRV-02", 4.0, 65.0, True),      # Inválida: descuento > 50%
            ("SIM-06", "CLI-06", "Luis Pena", "luis_sin_arroba.com", "SRV-01", 1.0, 0.0, False),    # Inválida: email sin @
            ("SIM-07", "CLI-07", "Francisco Tulcan", "fran@mail.com", "SRV-99", 2.0, 0.0, True),    # Inválida: servicio inexistente
            ("SIM-08", "CLI-08", "Maria Rodriguez", "maria@mail.com", "SRV-01", 3.5, 15.0, True),
            ("SIM-09", "CLI-09", "Jhon Bernal", "jhon@mail.com", "SRV-02", 2.0, 20.0, False),
            ("SIM-10", "CLI-10", "Elena Castro", "elena@mail.com", "SRV-01", 0.0, 0.0, True),       # Inválida: duración 0
            ("SIM-11", "CLI-11", "Pedro Vargas", "pedro@mail.com", "SRV-02", 5.0, 25.0, True),
            ("SIM-12", "CLI-12", "Camila Diaz", "camila@mail.com", "SRV-03", 1.0, 0.0, False),      # Inválida: SRV-03 no disponible
        ]

        for sim_id, c_id, c_nom, c_mail, srv_cod, dur, desc, iva in escenarios:
            try:
                cliente = Cliente(c_id, c_nom, c_mail)
                reserva = self.registrar_reserva(sim_id, cliente, srv_cod, dur, desc, iva)
            except ErrorServicioBase as err:
                resultados.append(f"[FAILED] {sim_id}: {type(err).__name__} -> {err}")
            else:
                resultados.append(f"[OK]     {sim_id}: {cliente.nombre} | {srv_cod} | Total: ${reserva.total:.2f}")
            finally:
                pass

        logging.info("=== FINISHED 12 BATCH SIMULATIONS ===")
        return resultados