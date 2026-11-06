"""
Generates crisp, high-resolution mathematical equation images using matplotlib mathtext.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs", "equations")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def render_equation(latex_str, filename, figsize=(8, 0.8), fontsize=13):
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.text(0.5, 0.5, f"${latex_str}$", ha='center', va='center', fontsize=fontsize, color='black')
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white', pad_inches=0.03)
    plt.close()
    print(f"[+] Rendered: {out_path}")
    return out_path


def main():
    print("[*] Rendering Mathematical Equations...")
    # 1. CED Equation
    eq_ced = r"\mathrm{CED} = \sum_{t=1}^{T} \mathbf{I}(t) \cdot (t_{t+1} - t_t) \quad \mathrm{where} \quad (t_{t+1} - t_t) = \frac{1}{\mathrm{FPS}_{\mathrm{video}}}"
    render_equation(eq_ced, "eq_ced.png", figsize=(7.5, 0.7), fontsize=12.5)

    # 2. CER Equation
    eq_cer = r"\mathrm{CER} = \left( \frac{N_{\mathrm{overlap\ events}}}{T_{\mathrm{observation}}} \right) \times 60 \quad [\mathrm{events\ /\ minute}]"
    render_equation(eq_cer, "eq_cer.png", figsize=(5.5, 0.65), fontsize=12)

    # 3. MACE & RCE Equation
    eq_mace = r"\mathrm{MACE} = \frac{1}{K} \sum_{i=1}^{K} | N_{\mathrm{GT}, i} - N_{\mathrm{Pred}, i} | \qquad \mathrm{RCE}_i = \left( \frac{| N_{\mathrm{GT}, i} - N_{\mathrm{Pred}, i} |}{\max(1, N_{\mathrm{GT}, i})} \right) \times 100\%"
    render_equation(eq_mace, "eq_mace.png", figsize=(8.5, 0.7), fontsize=12)


if __name__ == "__main__":
    main()

