package com.inventario.sistema.services;

import com.inventario.sistema.entities.Talla;
import com.inventario.sistema.repositories.TallaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class TallaService {

    private final TallaRepository tallaRepository;

    public List<Talla> listarTodas() {
        return tallaRepository.findAll();
    }

    public Optional<Talla> obtenerPorId(Long id) {
        return tallaRepository.findById(id);
    }

    public Talla guardar(Talla talla) {
        return tallaRepository.save(talla);
    }

    public void eliminar(Long id) {
        tallaRepository.deleteById(id);
    }

    public boolean existePorNombre(String nombre) {
        return tallaRepository.existsByNombre(nombre);
    }
}
