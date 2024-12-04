import math
import re

#######################################################################

def stringify_size(size: int):
    ten_powers = {
        0: "B",
        1: "KB",
        2: "MB",
        3: "GB",
        4: "TB"
    }
    if isinstance(size, int) and size < 0:
        raise ValueError("File size must be positive integer")
    order = (int(math.log10(size)) if size > 0 else 0)
    p = min(order // 3, len(ten_powers) - 1)
    
    return (size / (10**(3 * p)),  ten_powers[p])

#######################################################################

def extract_percentage(text):
    # Regex pour extraire le pourcentage
    match = re.search(r'(\d+(\.\d+)?)%', text)
    if match:
        return float(match.group(1))  # Récupérer la partie numérique
    return None  # Aucun pourcentage trouvé
