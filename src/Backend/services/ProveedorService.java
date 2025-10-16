package com.inventario.sistema.services;

import com.inventario.sistema.entities.Proveedor;
import com.inventario.sistema.repositories.ProveedorRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class ProveedorService {

    private final ProveedorRepository proveedorRepository;

    public List<Proveedor> listar() {
        return proveedorRepository.findAll();
    }

    public Optional<Proveedor> obtenerPorId(Long id) {
        return proveedorRepository.findById(id);
    }

    public Proveedor crear(Proveedor proveedor) {
        return proveedorRepository.save(proveedor);
    }

    public Optional<Proveedor> actualizar(Long id, Proveedor datos) {
        return proveedorRepository.findById(id).map(p -> {
            p.setNombre(datos.getNombre());
            p.setContacto(datos.getContacto());
            p.setTelefono(datos.getTelefono());
            p.setEmail(datos.getEmail());
            p.setDireccion(datos.getDireccion());
            
            return proveedorRepository.save(p);
        });
    }

    public boolean eliminar(Long id) {
        if (proveedorRepository.existsById(id)) {
            proveedorRepository.deleteById(id);
            return true;
        }
        return false;
    }
}
