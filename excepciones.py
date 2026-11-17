class ErrorServicioBase(Exception):
    """Excepción base para todas las reglas de negocio del sistema."""
    pass


class ParametroInconsistenteError(ErrorServicioBase):
    """Se lanza cuando los parámetros de entrada (horas, descuento, datos de cliente) son inválidos."""
    pass


class ServicioNoDisponibleError(ErrorServicioBase):
    """Se lanza cuando un servicio está inactivo o no disponible para reserva."""
    pass


class ClienteInvalidoError(ErrorServicioBase):
    """Se lanza cuando los datos del cliente están incompletos o el correo no es válido."""
    pass


class ReservaInvalidaError(ErrorServicioBase):
    """Se lanza cuando falla la creación o validación de una reserva."""
    pass