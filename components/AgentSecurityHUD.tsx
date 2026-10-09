import React, { useState, useEffect } from 'react';

// Banderas BitMaskOS (16-bit)
export const CAP_FLAGS = [
  { bit: 0x0001, label: "READ_CAPA0", color: "#00ff9d" },
  { bit: 0x0002, label: "EXEC_WASM", color: "#00e5ff" },
  { bit: 0x0004, label: "VORTEX_RUN", color: "#00e5ff" },
  { bit: 0x0008, label: "ECASH_MINT", color: "#ffb703" },
  { bit: 0x0010, label: "VOXEL_3D", color: "#00ff9d" },
  { bit: 0x0020, label: "P2P_MESH", color: "#00e5ff" },
  { bit: 0x0040, label: "LOCAL_AI", color: "#ffb703" },
  { bit: 0x0100, label: "TERMINAL_EXEC", color: "#ff0055" },
  { bit: 0x0200, label: "GPU_STREAM", color: "#ff0055" },
  { bit: 0x8000, label: "SOVEREIGN_ROOT", color: "#ff0055" },
];

export interface AgentMetrics {
  capsMask: number;
  powerWatts: number;
  ramUsageMb: number;
  piFrameBytes: number;
  quarantineActive: boolean;
  activeAgent: 'BOHR-HAFNIO' | 'VELÁZQUEZ' | 'GOYA' | 'SWARTZ';
  entropyEnergyJoule: string;
}

export const AgentSecurityHUD: React.FC<{ initialCaps?: number }> = ({ initialCaps = 0x0047 }) => {
  const [metrics, setMetrics] = useState<AgentMetrics>({
    capsMask: initialCaps,
    powerWatts: 4.18,
    ramUsageMb: 24.6,
    piFrameBytes: 3141,
    quarantineActive: true,
    activeAgent: 'BOHR-HAFNIO',
    entropyEnergyJoule: "1.9932e-21",
  });

  // Simulación de latido de telemetría P2P / Darwin local
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics((prev) => ({
        ...prev,
        powerWatts: Number((4.1 + Math.random() * 0.25).toFixed(2)),
        ramUsageMb: Number((24.0 + Math.random() * 1.5).toFixed(1)),
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const hasCap = (bit: number) => (metrics.capsMask & bit) === bit;

  return (
    <div style={{
      background: 'rgba(5, 8, 13, 0.95)',
      border: '1px solid #007744',
      borderRadius: '8px',
      padding: '16px',
      fontFamily: "'JetBrains Mono', monospace",
      color: '#00ff9d',
      maxWidth: '650px',
      boxShadow: '0 0 25px rgba(0, 255, 157, 0.15)',
    }}>
      {/* CABECERA HUD */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #007744', paddingBottom: '8px', marginBottom: '12px' }}>
        <span style={{ fontWeight: 'bold', color: '#00e5ff', fontSize: '0.9rem' }}>
          🛡️ OASIS BITMASK-OS AGENT HUD
        </span>
        <span style={{ fontSize: '0.75rem', background: 'rgba(0, 229, 255, 0.1)', padding: '2px 8px', borderRadius: '4px', border: '1px solid #00e5ff', color: '#00e5ff' }}>
          0x{metrics.capsMask.toString(16).toUpperCase().padStart(4, '0')}
        </span>
      </div>

      {/* MÉTRICAS FÍSICAS (SILICIO FRÍO) */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', marginBottom: '16px' }}>
        <div style={{ background: 'rgba(6, 12, 20, 0.8)', padding: '8px', borderRadius: '4px', border: '1px solid #007744' }}>
          <div style={{ fontSize: '0.7rem', color: '#888' }}>POTENCIA SILICIO</div>
          <div style={{ fontSize: '1rem', fontWeight: 'bold', color: metrics.powerWatts <= 5.39 ? '#00ff9d' : '#ff0055' }}>
            {metrics.powerWatts} W <span style={{ fontSize: '0.65rem', color: '#555' }}>/ ≤ 5.39W</span>
          </div>
        </div>

        <div style={{ background: 'rgba(6, 12, 20, 0.8)', padding: '8px', borderRadius: '4px', border: '1px solid #007744' }}>
          <div style={{ fontSize: '0.7rem', color: '#888' }}>MEMORIA RESIDENTE</div>
          <div style={{ fontSize: '1rem', fontWeight: 'bold', color: '#00e5ff' }}>
            {metrics.ramUsageMb} MB <span style={{ fontSize: '0.65rem', color: '#555' }}>/ &lt; 30MB</span>
          </div>
        </div>

        <div style={{ background: 'rgba(6, 12, 20, 0.8)', padding: '8px', borderRadius: '4px', border: '1px solid #007744' }}>
          <div style={{ fontSize: '0.7rem', color: '#888' }}>CUADRILLA ACTIVA</div>
          <div style={{ fontSize: '0.85rem', fontWeight: 'bold', color: '#ffb703' }}>
            {metrics.activeAgent}
          </div>
        </div>
      </div>

      {/* ESTADO DE CONFINAMIENTO Y CUARENTENA */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '14px', fontSize: '0.75rem' }}>
        <span style={{ flex: 1, padding: '4px 8px', background: 'rgba(0, 255, 157, 0.08)', border: '1px solid #007744', borderRadius: '4px' }}>
          📦 Trama Máxima: <strong>{metrics.piFrameBytes} bytes (π-KB)</strong>
        </span>
        <span style={{ flex: 1, padding: '4px 8px', background: metrics.quarantineActive ? 'rgba(0, 229, 255, 0.08)' : 'rgba(255, 0, 85, 0.1)', border: '1px solid #00e5ff', borderRadius: '4px' }}>
          🔒 Cuarentena: <strong>{metrics.quarantineActive ? 'ACTIVA (Pass Verificado)' : 'INACTIVA'}</strong>
        </span>
      </div>

      {/* MATRIZ DE CAPACIDADES BITMASKOS */}
      <div style={{ fontSize: '0.75rem', marginBottom: '6px', color: '#aaa' }}>CAPACIDADES ACTIVAS EN HARDWARE (&lt; 1 ns):</div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
        {CAP_FLAGS.map(({ bit, label, color }) => {
          const authorized = hasCap(bit);
          return (
            <span
              key={bit}
              style={{
                fontSize: '0.65rem',
                padding: '3px 6px',
                borderRadius: '3px',
                border: `1px solid ${authorized ? color : '#333'}`,
                background: authorized ? `${color}18` : 'transparent',
                color: authorized ? color : '#444',
                textDecoration: authorized ? 'none' : 'line-through',
              }}
            >
              0x{bit.toString(16).padStart(4, '0')} {label}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export default AgentSecurityHUD;
