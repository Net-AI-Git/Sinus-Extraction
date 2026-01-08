import json
import sys

notebook_path = r'c:\Users\netanit\Desktop\Work\Sinus_Extraction\Segmentation_code_templates\ImageSegmentation_template.ipynb'

try:
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    print(f"Total cells before: {len(notebook['cells'])}")
    
    # Find cells to delete
    cells_to_delete = []
    for i, cell in enumerate(notebook['cells']):
        source = ''.join(cell.get('source', []))
        cell_id = cell.get('id', '')
        
        # Check by cell ID (most reliable)
        if cell_id in ['fancy-knock', '3f733cc7', '59d629a8', '2f08602f', '034cd3c9', '93c5d95d', 'further-vietnamese']:
            cells_to_delete.append(i)
            print(f"Found cell {i} (ID: {cell_id})")
        # Also check by content
        elif 'task 3' in source.lower() and 'augmentation' in source.lower():
            if i not in cells_to_delete:
                cells_to_delete.append(i)
                print(f"Found cell {i} by content")
        elif 'task 3.1' in source.lower() or 'task 3.2' in source.lower() or 'task 3.3' in source.lower() or 'task 3.4' in source.lower() or 'task 3.5' in source.lower() or 'task 3.6' in source.lower():
            if i not in cells_to_delete:
                cells_to_delete.append(i)
                print(f"Found cell {i} by content (TASK 3.x)")
        elif 'albumentation documentation' in source.lower() and 'task 4' not in source.lower():
            if i not in cells_to_delete:
                cells_to_delete.append(i)
                print(f"Found cell {i} by content (albumentation docs)")
    
    print(f"\nCells to delete: {len(cells_to_delete)} at indices: {cells_to_delete}")
    
    # Delete cells in reverse order
    for idx in sorted(cells_to_delete, reverse=True):
        del notebook['cells'][idx]
        print(f"Deleted cell at index {idx}")
    
    print(f"Total cells after: {len(notebook['cells'])}")
    
    # Save the notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)
    
    print("\nSuccess! Augmentation cells removed.")
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
