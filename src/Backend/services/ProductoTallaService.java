package com.inventario.sistema.services;

import com.inventario.sistema.entities.ProductoTalla;
import com.inventario.sistema.repositories.ProductoTallaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class ProductoTallaService {

    private final ProductoTallaRepository productoTallaRepository;

    public List<ProductoTalla> listarTodos() {
        return productoTallaRepository.findAll();
    }

    public Optional<ProductoTalla> obtenerPorId(Long id) {
        return productoTallaRepository.findById(id);
    }

    public List<ProductoTalla> obtenerPorProducto(Long productoId) {
        return productoTallaRepository.findByProductoId(productoId);
    }

    public ProductoTalla guardar(ProductoTalla productoTalla) {
        return productoTallaRepository.save(productoTalla);
    }

    public void eliminar(Long id) {
        productoTallaRepository.deleteById(id);
    }

    public boolean existePorProductoYPorTalla(Long productoId, Long tallaId) {
        return productoTallaRepository.existsByProductoIdAndTallaId(productoId, tallaId);
    }
    public int contarTotal() {
    return productoTallaRepository.findAll()
            .stream()
            .mapToInt(ProductoTalla::getStockActual)
            .sum();
}

}
