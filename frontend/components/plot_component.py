import numpy as np

def beeswarm_positions(y_values: np.ndarray, x_center: float = 0, width: float = 0.08, size: float = 0.015) -> np.ndarray:
    positions = np.zeros(len(y_values))
    sorted_indices = np.argsort(y_values)
    placed_indices = []

    for idx in sorted_indices:
        y = y_values[idx]
        best_x = x_center
        min_shift_needed = 0
    
        for other_idx in placed_indices:
            dx = x_center - positions[other_idx]
            dy = y - y_values[other_idx]
            distance = np.sqrt(dx**2 + dy**2)
            
            if distance < size:
                dx_needed = np.sqrt(max(0, size**2 - dy**2))
                shift_needed = dx_needed - abs(dx)
                if shift_needed > min_shift_needed:
                    min_shift_needed = shift_needed
    
        if min_shift_needed > 0:
            x_right = x_center + min_shift_needed
            x_left = x_center - min_shift_needed
            if abs(x_right - x_center) <= width:
                best_x = x_right
            elif abs(x_left - x_center) <= width:
                best_x = x_left
            else:
                best_x = x_right
    
        positions[idx] = best_x
        placed_indices.append(idx)

    
    return positions