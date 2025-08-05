import numpy as np
import matplotlib.pyplot as plt

# Constante mu_0/(2pi)
MU0_OVER_2PI = 2e-7  # N/A²

def magnetic_field(x, y, wires):
    Bx, By = 0, 0
    for x0, y0, I in wires:
        dx = x - x0
        dy = y - y0
        r_squared = dx**2 + dy**2
        if r_squared < 1e-6:  # Evitar división por cero
            continue
        factor = MU0_OVER_2PI * I / r_squared
        Bx += -dy * factor
        By += dx * factor
    return Bx, By

def plot_magnetic_field(wires, title, xlim=(-2, 2), ylim=(-2, 2), grid_size=20):
    # Crear grid de puntos
    x = np.linspace(xlim[0], xlim[1], grid_size)
    y = np.linspace(ylim[0], ylim[1], grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Calcular campo en cada punto
    Bx, By = np.zeros_like(X), np.zeros_like(Y)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            bx, by = magnetic_field(X[i,j], Y[i,j], wires)
            Bx[i,j] = bx
            By[i,j] = by
    
    # Normalizar flechas para mejor visualización
    norm = np.sqrt(Bx**2 + By**2)
    mask = norm > 0
    Bx[mask] = Bx[mask]/norm[mask]  # Dirección unitaria
    By[mask] = By[mask]/norm[mask]
    
    # Crear figura
    plt.figure(figsize=(8, 6))
    plt.quiver(X, Y, Bx, By, norm, cmap='viridis', scale=30, width=0.002, pivot='middle')
    
    # Dibujar alambres
    for x0, y0, I in wires:
        if I > 0:
            plt.plot(x0, y0, 'ro', markersize=10, label='Corriente saliente (+z)' if I == wires[0][2] else "")
        else:
            plt.plot(x0, y0, 'bx', markersize=10, label='Corriente entrante (-z)' if I == wires[0][2] else "")
    
    plt.title(title, fontsize=14)
    plt.xlabel('x (m)', fontsize=12)
    plt.ylabel('y (m)', fontsize=12)
    plt.colorbar(label='Magnitud del campo (T)')
    plt.grid(alpha=0.5)
    plt.axis('equal')
    plt.legend()
    plt.tight_layout()  # Evitar solapamiento
    plt.show()

# Configuración de 3 alambres (triángulo equilátero)
wires_3 = [
    (0, 1, 1.0),       # (x, y, I): I > 0 = corriente saliente
    (0.866, -0.5, -1.0), # I < 0 = corriente entrante
    (-0.866, -0.5, 1.0)
]

# Configuración de 5 alambres (cruz)
wires_5 = [
    (0, 0, 2.0),     # Alambre central con mayor corriente
    (1, 0, -1.0),
    (-1, 0, -1.0),
    (0, 1, 1.0),
    (0, -1, 1.0)
]

# Generar gráficas por separado (requisito de la guía)
plot_magnetic_field(wires_3, "Campo Magnético: Configuración de 3 Alambres")
plot_magnetic_field(wires_5, "Campo Magnético: Configuración de 5 Alambres", xlim=(-2.5, 2.5), ylim=(-2.5, 2.5))