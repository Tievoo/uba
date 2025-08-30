## Ejercicio 1.1
Una compañía de seguros de automóviles tiene clientes que pueden poseer uno o más vehículos cada uno. Cada vehículo tiene asociado cero a cualquier número de accidentes registrados. Cada póliza de seguro cubre uno o más vehículos, y tiene uno o más pagos de las primas asociadas con ella. Cada pago es por un período de tiempo determinado , y tiene una fecha de vencimiento asociada, y la fecha en que se recibió el pago. Discuta diferentes alternativas de vinculación entre póliza y vehículo.


![alt text](fotos/ej1.1.png)

### Pasaje a MR
**Cliente**(<u>idCliente</u>)<br>
PK=CK={idCliente}

**Vehiculo**(<u>idVehiculo</u>, idCliente, accidentes)<br>
PK = CK = {idVehiculo}<br>
FK = {idCliente}

**Póliza**(<u>idPoliza</u>)<br>
PK=CK={idPoliza}

**VehiculoPoliza (cubierto por)**(<u>idPoliza,idVehiculo</u>)<br>
PK=CK={(idPoliza,idVehiculo)}<br>
FK={idPoliza, idVehiculo}

**PagoPrima**(<u>idPago</u>, fecha_recibido, fecha_vencimiento, <span style='border-bottom: 1px dotted white'>idPoliza</span>)<br>
PK=CK={idPago}
FK={idPoliza}

