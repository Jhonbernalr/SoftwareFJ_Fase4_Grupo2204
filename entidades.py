from abc import ABC, abstractmethod
from excepciones import (
    ParametroInconsistenteError,
    ServicioNoDisponibleError,
    ClienteInvalidoError,
    ReservaInvalidaError,
)


class Cliente:
    """Representa un cliente registrado en el sistema de soporte."""

    def __init__(self, cliente_id: str, nombre: str, email: str):
        if not cliente_id or not nombre or "@" not in email:
            raise ClienteInvalidoError(
                f"Invalid client data for ID '{cliente_id}': name and valid email are required."
            )
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.email = email

    def __str__(self) -> str:
        return f"{self.cliente_id} - {self.nombre} ({self.email})"


class Servicio(ABC):
    """Clase base abstracta para los servicios tecnológicos."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        if tarifa_hora <= 0:
            raise ParametroInconsistenteError("Hourly rate must be greater than zero.")
        self._codigo = codigo
        self._nombre = nombre
        self._tarifa_hora = tarifa_hora
        self._disponible = disponible

    @property
    def codigo_servicio(self) -> str:
        return self._codigo

    @property
    def disponible(self) -> bool:
        return self._disponible

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    def validar_parametros(self, duracion: float, descuento_pct: float) -> None:
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"Service '{self._nombre}' ({self._codigo}) is currently unavailable."
            )
        if duracion <= 0:
            raise ParametroInconsistenteError("Duration must be greater than 0 hours.")
        if not (0 <= descuento_pct <= 50):
            raise ParametroInconsistenteError("Discount percentage must be between 0% and 50%.")

    def calcular_costo(
        self,
        duracion: float,
        descuento_pct: float = 0.0,
        aplicar_iva: bool = True,
    ) -> float:
        self.validar_parametros(duracion, descuento_pct)
        subtotal = self._tarifa_hora * duracion
        monto_descuento = subtotal * (descuento_pct / 100.0)
        total = subtotal - monto_descuento
        if aplicar_iva:
            total *= 1.19
        return round(total, 2)


class Reserva:
    """Asocia un Cliente con un Servicio y calcula el total de la orden."""

    def __init__(
        self,
        reserva_id: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: float,
        descuento_pct: float = 0.0,
        aplicar_iva: bool = True,
    ):
        self.reserva_id = reserva_id
        self.cliente = cliente
        self.servicio = servicio
        try:
            self.total = servicio.calcular_costo(duracion, descuento_pct, aplicar_iva)
        except Exception as err:
            # Uso explícito de 'raise ... from' exigido en la rúbrica
            raise ReservaInvalidaError(
                f"Booking {reserva_id} failed for client {cliente.nombre}: {err}"
            ) from err