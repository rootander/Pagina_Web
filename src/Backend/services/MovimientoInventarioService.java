package com.inventario.sistema.services;

import com.inventario.sistema.entities.MovimientoInventario;
import com.inventario.sistema.entities.ProductoTalla;
import com.inventario.sistema.entities.Usuario;
import com.inventario.sistema.repositories.MovimientoInventarioRepository;
import com.inventario.sistema.repositories.ProductoTallaRepository;
import com.inventario.sistema.repositories.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class MovimientoInventarioService {

    private final MovimientoInventarioRepository movimientoRepo;
    private final ProductoTallaRepository productoTallaRepo;
    private final UsuarioRepository usuarioRepo;

    public List<MovimientoInventario> listarTodos() {
        return movimientoRepo.findAll();
    }

    public Optional<MovimientoInventario> obtenerPorId(Long id) {
        return movimientoRepo.findById(id);
    }

    @Transactional
    public MovimientoInventario guardarConUsuario(MovimientoInventario movimiento, String username) {
        Usuario usuario = usuarioRepo.findByUsername(username)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        ProductoTalla pt = productoTallaRepo.findById(movimiento.getProductoTalla().getId())
                .orElseThrow(() -> new RuntimeException("ProductoTalla no encontrado"));

        if ("ENTRADA".equalsIgnoreCase(movimiento.getTipo())) {
            pt.setStockActual(pt.getStockActual() + movimiento.getCantidad());
        } else if ("SALIDA".equalsIgnoreCase(movimiento.getTipo())) {
            if (pt.getStockActual() < movimiento.getCantidad()) {
                throw new RuntimeException("Stock insuficiente. Stock disponible: " 
                        + pt.getStockActual() + ", solicitado: " + movimiento.getCantidad());
            }
            pt.setStockActual(pt.getStockActual() - movimiento.getCantidad());
        } else {
            throw new RuntimeException("Tipo de movimiento no válido (use ENTRADA o SALIDA)");
        }

        productoTallaRepo.save(pt);

        movimiento.setFecha(LocalDateTime.now());
        movimiento.setUsuario(usuario);
        return movimientoRepo.save(movimiento);
    }

    @Transactional
    public MovimientoInventario actualizarConUsuario(Long id, MovimientoInventario nuevo, String username) {
        MovimientoInventario existente = movimientoRepo.findById(id)
                .orElseThrow(() -> new RuntimeException("Movimiento no encontrado"));

        ProductoTalla pt = productoTallaRepo.findById(nuevo.getProductoTalla().getId())
                .orElseThrow(() -> new RuntimeException("ProductoTalla no encontrado"));

        // Revertir stock anterior
        if ("ENTRADA".equalsIgnoreCase(existente.getTipo())) {
            pt.setStockActual(pt.getStockActual() - existente.getCantidad());
        } else if ("SALIDA".equalsIgnoreCase(existente.getTipo())) {
            pt.setStockActual(pt.getStockActual() + existente.getCantidad());
        }

        // Aplicar nuevo movimiento
        if ("ENTRADA".equalsIgnoreCase(nuevo.getTipo())) {
            pt.setStockActual(pt.getStockActual() + nuevo.getCantidad());
        } else if ("SALIDA".equalsIgnoreCase(nuevo.getTipo())) {
            if (pt.getStockActual() < nuevo.getCantidad()) {
                throw new RuntimeException("Stock insuficiente. Stock disponible: " 
                        + pt.getStockActual() + ", solicitado: " + nuevo.getCantidad());
            }
            pt.setStockActual(pt.getStockActual() - nuevo.getCantidad());
        } else {
            throw new RuntimeException("Tipo de movimiento no válido (use ENTRADA o SALIDA)");
        }

        productoTallaRepo.save(pt);

        existente.setProductoTalla(pt);
        existente.setCantidad(nuevo.getCantidad());
        existente.setTipo(nuevo.getTipo());
        existente.setDescripcion(nuevo.getDescripcion());
        existente.setFecha(LocalDateTime.now());

        return movimientoRepo.save(existente);
    }

    @Transactional
    public void eliminar(Long id) {
        movimientoRepo.findById(id).ifPresent(mov -> {
            ProductoTalla pt = mov.getProductoTalla();
            if (pt != null) {
                if ("ENTRADA".equalsIgnoreCase(mov.getTipo())) {
                    pt.setStockActual(pt.getStockActual() - mov.getCantidad());
                } else if ("SALIDA".equalsIgnoreCase(mov.getTipo())) {
                    pt.setStockActual(pt.getStockActual() + mov.getCantidad());
                }
                productoTallaRepo.save(pt);
            }
            movimientoRepo.delete(mov);
        });
    }

    public List<MovimientoInventario> obtenerPorProducto(Long productoId) {
        return movimientoRepo.findByProductoTalla_Producto_Id(productoId);
    }

    public List<MovimientoInventario> obtenerPorProductoTalla(Long productoTallaId) {
        return movimientoRepo.findByProductoTalla_Id(productoTallaId);
    }
    public int contarEsteMes() {
    LocalDateTime inicioMes = LocalDateTime.now().withDayOfMonth(1).withHour(0).withMinute(0).withSecond(0);
    return (int) movimientoRepo.findByFechaAfter(inicioMes).stream().count();
}

}
