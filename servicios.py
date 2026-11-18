from entidades import Servicio


class MantenimientoHardware(Servicio):
    """Servicio concreto para mantenimiento preventivo/correctivo de hardware."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_hora: float,
        tipo_equipo: str,
        disponible: bool = True,
    ):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        self.tipo_equipo = tipo_equipo

    def describir_servicio(self) -> str:
        estado = "Available" if self._disponible else "Unavailable"
        return f"[Hardware - {self.tipo_equipo}] {self._nombre} (${self._tarifa_hora:.2f}/hr) - {estado}"


class SoporteSoftware(Servicio):
    """Servicio concreto para instalación, configuración y diagnóstico de software."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_hora: float,
        remoto: bool = True,
        disponible: bool = True,
    ):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        self.remoto = remoto

    def describir_servicio(self) -> str:
        modalidad = "Remote" if self.remoto else "On-Site"
        estado = "Available" if self._disponible else "Unavailable"
        return f"[Software - {modalidad}] {self._nombre} (${self._tarifa_hora:.2f}/hr) - {estado}"