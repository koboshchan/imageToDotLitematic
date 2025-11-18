import numpy as np
import tqdm
from litemapy import Schematic, Region, BlockState


def rotate_litematic(input_file, output_file, rotation_axis='x'):
    """
    Rotate a vertical litematic structure to lay it flat.
    
    Args:
        input_file: Path to input .litematic file
        output_file: Path to output .litematic file
        rotation_axis: Axis to rotate around ('x' or 'z')
                      'x' - rotates Y->Z (structure faces +Z after rotation)
                      'z' - rotates Y->X (structure faces +X after rotation)
    """
    # Load the schematic
    schem = Schematic.load(input_file)
    
    # Get the first region (assuming single region)
    reg_name = list(schem.regions.keys())[0]
    old_reg = schem.regions[reg_name]
    
    # Get dimensions
    old_width = old_reg.width   # X
    old_height = old_reg.height # Y
    old_length = old_reg.length # Z
    
    print(f"Input dimensions: X={old_width}, Y={old_height}, Z={old_length}")
    
    # Create new region with rotated dimensions
    if rotation_axis == 'x':
        # Rotate around X axis: Y becomes Z, Z becomes Y
        new_width = old_width
        new_height = old_length
        new_length = old_height
        print(f"Rotating around X axis: Y->Z, Z->-Y")
    elif rotation_axis == 'z':
        # Rotate around Z axis: Y becomes X, X becomes Y
        new_width = old_height
        new_height = old_width
        new_length = old_length
        print(f"Rotating around Z axis: Y->X, X->-Y")
    else:
        raise ValueError("rotation_axis must be 'x' or 'z'")
    
    print(f"Output dimensions: X={new_width}, Y={new_height}, Z={new_length}")
    
    # Create new region and schematic
    new_reg = Region(0, 0, 0, new_width, new_height, new_length)
    new_schem = new_reg.as_schematic(
        name=schem.name + "_rotated",
        author=schem.author,
        description=schem.description + " (rotated)"
    )
    
    # Copy blocks with rotation
    total_blocks = old_width * old_height * old_length
    pbar = tqdm.tqdm(total=total_blocks, desc="Rotating blocks")
    
    for x in range(old_width):
        for y in range(old_height):
            for z in range(old_length):
                block = old_reg.getblock(x, y, z)
                
                # Skip air blocks for efficiency
                if block.blockid == "minecraft:air":
                    pbar.update(1)
                    continue
                
                # Calculate new position based on rotation
                if rotation_axis == 'x':
                    # Rotate 90° around X: (x, y, z) -> (x, z, height-1-y)
                    new_x = x
                    new_y = z
                    new_z = old_height - 1 - y
                elif rotation_axis == 'z':
                    # Rotate 90° around Z: (x, y, z) -> (y, width-1-x, z)
                    new_x = y
                    new_y = old_width - 1 - x
                    new_z = z
                
                # Place block in new position
                new_reg.setblock(new_x, new_y, new_z, block)
                
                pbar.update(1)
    
    pbar.close()
    
    # Save the rotated schematic
    new_schem.save(output_file)
    print(f"Saved rotated schematic to {output_file}")


if __name__ == "__main__":
    # Example usage
    input_file = "input.litematic"
    output_file = "flat_structure.litematic"
    
    # Rotate around X axis (most common for vertical->horizontal)
    # This makes a tall structure lay flat on the ground
    rotate_litematic(input_file, output_file, rotation_axis='x')
    
    # Alternative: rotate around Z axis
    # rotate_litematic(input_file, output_file, rotation_axis='z')