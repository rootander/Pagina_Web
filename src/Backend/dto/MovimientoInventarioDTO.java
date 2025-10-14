package Backend.dto;

import lombok.Data;

@Data
public class MovimientoInventarioDTO {
    private Long productoTallaId;
    private Integer usuarioId;
    private Integer cantidad;
    private String tipo;     
    private String descripcion;
}
