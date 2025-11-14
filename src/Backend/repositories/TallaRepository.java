package Backend.repositories;

import com.inventario.sistema.entities.Talla;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TallaRepository extends JpaRepository<Talla, Long> {
    boolean existsByNombre(String nombre);
}
