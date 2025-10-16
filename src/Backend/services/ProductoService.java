package com.inventario.sistema.services;

import com.inventario.sistema.entities.Producto;
import com.inventario.sistema.repositories.ProductoRepository;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductoService {

    private final ProductoRepository productoRepository;

    @Transactional
    public List<Producto> listarTodos() {
        List<Producto> productos = productoRepository.findAll();

        
        productos.forEach(p -> {
            if (p.getCategoria() != null) {
                p.getCategoria().getNombre();
            }
            if (p.getProveedor() != null) {
                p.getProveedor().getNombre();
            }
        });

        return productos;
    }

    @Transactional
    public Producto obtenerPorId(Long id) {
        Producto producto = productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con ID: " + id));

        
        if (producto.getCategoria() != null) {
            producto.getCategoria().getNombre();
        }
        if (producto.getProveedor() != null) {
            producto.getProveedor().getNombre();
        }

        return producto;
    }

    @Transactional
    public void crear(Producto producto) {
        productoRepository.save(producto);
    }

    @Transactional
    public void actualizar(Long id, Producto nuevoProducto) {
        Producto existente = productoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con ID: " + id));

        existente.setNombre(nuevoProducto.getNombre());
        existente.setDescripcion(nuevoProducto.getDescripcion());
        existente.setCategoria(nuevoProducto.getCategoria());
        existente.setProveedor(nuevoProducto.getProveedor());
        existente.setPrecioCompra(nuevoProducto.getPrecioCompra());
        existente.setPrecioVenta(nuevoProducto.getPrecioVenta());
        existente.setSku(nuevoProducto.getSku());

        productoRepository.save(existente);
    }

    @Transactional
    public void eliminar(Long id) {
        productoRepository.deleteById(id);
    }
    public int contarActivos() {
    return productoRepository.findAll().size();
}

}
