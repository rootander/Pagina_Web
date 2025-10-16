package Backend.repositories;

import com.inventario.sistema.entities.MovimientoInventario;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDateTime;
import java.util.List;

public interface MovimientoInventarioRepository extends JpaRepository<MovimientoInventario, Long> {
    List<MovimientoInventario> findByProductoTalla_Producto_Id(Long productoId);
    List<MovimientoInventario> findByProductoTalla_Id(Long productoTallaId);
    List<MovimientoInventario> findByFechaAfter(LocalDateTime fecha);

}
