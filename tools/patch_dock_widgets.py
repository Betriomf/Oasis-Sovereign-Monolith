#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

patch_script = """
// --- PARCHE OASIS OS v15.1: DOCK WIDGETS & ELIMINACIÓN DE CANAL NASA ---

function toggleDockMenu() {
    const panel = document.getElementById('dock-widgets-panel') || document.querySelector('.dock-panel');
    if (panel) {
        if (panel.style.display === 'block' || panel.classList.contains('active')) {
            panel.style.display = 'none';
            panel.classList.remove('active');
        } else {
            panel.style.display = 'block';
            panel.classList.add('active');
        }
    } else {
        console.warn("Panel Dock Widgets no encontrado en el DOM.");
    }
}

// Vincular el botón superior DOCK WIDGETS
document.addEventListener('DOMContentLoaded', function() {
    const btnTop = document.getElementById('btn-dock-top') || document.querySelector('[data-dock-trigger]');
    if (btnTop) {
        btnTop.addEventListener('click', toggleDockMenu);
    }
    
    // Eliminar cualquier widget o reproductor del canal NASA
    const nasaElements = document.querySelectorAll('#nasa-stream, .nasa-widget, [data-channel="nasa"]');
    nasaElements.forEach(el => el.remove());
});

// Ejecutar comando desde Widget directamente hacia la Terminal Web
function runWidgetCommand(cmd) {
    if (typeof executeTerminalCommand === 'function') {
        executeTerminalCommand(cmd);
    } else if (typeof printToTerminal === 'function') {
        printToTerminal("root@oasis-hurd:/workspace# " + cmd);
        // Despachar al backend
        fetch("http://127.0.0.1:8080/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: cmd })
        })
        .then(res => res.json())
        .then(data => printToTerminal(data.response || data.rust_kernel || "OK"))
        .catch(err => printToTerminal("Error: " + err));
    }
}
"""

with open("agents_core/oasis_dock_patch.js", "w", encoding="utf-8") as f:
    f.write(patch_script)

print("✅ Parche 'oasis_dock_patch.js' generado sin canal NASA y con triggers vinculados.")
