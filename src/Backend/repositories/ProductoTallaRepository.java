package Backend.repositories;

import com.inventario.sistema.entities.ProductoTalla;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ProductoTallaRepository extends JpaRepository<ProductoTalla, Long> {
    List<ProductoTalla> findByProductoId(Long productoId);
    List<ProductoTalla> findByTallaId(Long tallaId);
    boolean existsByProductoIdAndTallaId(Long productoId, Long tallaId);
}
