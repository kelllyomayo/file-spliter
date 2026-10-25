import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def init_gui():
    """Hides the ugly blank tkinter root window."""
    root = tk.Tk()
    root.withdraw()
    return root

def disassemble_file():
    """Splits a large file into smaller 3GB chunks for TeraBox."""
    # 1. Select the file to split
    input_file = filedialog.askopenfilename(title="Select Large File to Disassemble (Split)")
    if not input_file:
        print("Operation cancelled.")
        return

    # 2. Choose where to save the chunks and what to name them
    save_base = filedialog.asksaveasfilename(
        title="Create Base Name for Chunks (e.g. windows_11.iso)",
        initialfile=os.path.basename(input_file)
    )
    if not save_base:
        print("Operation cancelled.")
        return

    # Default chunk size: 3 GB to stay safely under TeraBox's 4GB firewall
    chunk_size = 3 * 1024 * 1024 * 1024 
    file_number = 1

    try:
        print(f"\nDisassembling: {input_file}")
        with open(input_file, 'rb') as src:
            while True:
                chunk = src.read(chunk_size)
                if not chunk:
                    break
                
                # Creates files like: game.iso.part1, game.iso.part2
                chunk_output_name = f"{save_base}.part{file_number}"
                print(f"Creating chunk: {os.path.basename(chunk_output_name)}")
                
                with open(chunk_output_name, 'wb') as dest:
                    dest.write(chunk)
                
                file_number += 1
                
        messagebox.showinfo("Success", f"File split into {file_number - 1} parts successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during disassembly:\n{str(e)}")

def assemble_file():
    """Gathers and merges chunks back into a single file."""
    # 1. Ask the user for the string name of the original file base
    base_name = simpledialog.askstring(
        "File Base Name", 
        "Enter the base name of the files to reassemble\n(e.g., windows_11.iso if your chunks are windows_11.iso.part1):"
    )
    if not base_name:
        print("Operation cancelled.")
        return

    # 2. Ask how many chunks there are
    total_chunks = simpledialog.askinteger(
        "Number of Chunks", 
        f"How many '.part' chunks exist for {base_name}?"
    )
    if not total_chunks or total_chunks < 1:
        print("Operation cancelled.")
        return

    # 3. Use File Explorer to pick where to save the reassembled file
    output_file = filedialog.asksaveasfilename(
        title="Save Reassembled File As...",
        initialfile=base_name
    )
    if not output_file:
        print("Operation cancelled.")
        return

    # 4. Find the directory containing the chunks
    messagebox.showinfo("Locate Chunks", "Please choose the FOLDER where your downloaded chunks are stored.")
    chunk_dir = filedialog.askdirectory(title="Select Folder Containing Chunks")
    if not chunk_dir:
        print("Operation cancelled.")
        return

    try:
        print(f"\nAssembling files into: {output_file}")
        with open(output_file, 'wb') as dest:
            for i in range(1, total_chunks + 1):
                chunk_path = os.path.join(chunk_dir, f"{base_name}.part{i}")
                
                if not os.path.exists(chunk_path):
                    raise FileNotFoundError(f"Missing required file: {os.path.basename(chunk_path)}")
                
                print(f"Appending: {os.path.basename(chunk_path)}")
                with open(chunk_path, 'rb') as src:
                    dest.write(src.read())
                    
        messagebox.showinfo("Success", f"File reassembled completely as:\n{output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during assembly:\n{str(e)}")

def main():
    init_gui()
    
    # Simple console or popup choice menu
    print("=== File Toolkit ===")
    print("1. Disassembler (Split big file into < 4GB chunks)")
    print("2. Assembler (Merge chunks back into a single file)")
    
    choice = simpledialog.askstring(
        "Mode Selection", 
        "Type '1' for Disassembler (Split)\nType '2' for Assembler (Merge):"
    )
    
    if choice == '1':
        disassemble_file()
    elif choice == '2':
        assemble_file()
    else:
        print("Invalid choice or window closed.")

if __name__ == "__main__":
    main()
