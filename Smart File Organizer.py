import os
import shutil
from datetime import datetime


# File categories and their extensions
FILE_TYPES = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos":     [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Audio":      [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".pptx", ".xlsx", ".csv"],
    "Code":       [".py", ".js", ".html", ".css", ".java", ".c", ".cpp"],
    "Archives":   [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Others":     []
}


def get_category(filename):
    """Returns category name based on file extension"""
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Others"


def organize_folder(folder_path):
    """Organizes all files in the given folder into subfolders"""
    if not os.path.exists(folder_path):
        raise ValueError(f"Folder not found: {folder_path}")

    files_moved = 0
    log = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Skip folders and this script itself
        if os.path.isdir(file_path):
            continue
        if filename == os.path.basename(__file__):
            continue

        category = get_category(filename)

        # Create category folder if it doesn't exist
        category_folder = os.path.join(folder_path, category)
        os.makedirs(category_folder, exist_ok=True)

        # Move the file
        destination = os.path.join(category_folder, filename)
        shutil.move(file_path, destination)

        log.append(f"{filename} → {category}")
        files_moved += 1

    return files_moved, log


def show_summary(folder_path):
    """Shows how many files are in each category folder"""
    print("\n📂 Folder Summary:")
    print("-" * 35)
    for category in FILE_TYPES:
        category_path = os.path.join(folder_path, category)
        if os.path.exists(category_path):
            count = len(os.listdir(category_path))
            print(f"{category:<15} : {count} files")
    print()


def save_log(log, folder_path):
    """Saves the activity log to a text file"""
    log_file = os.path.join(folder_path, "organizer_log.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(log_file, "w") as f:
        f.write(f"Smart File Organizer Log - {timestamp}\n")
        f.write("-" * 40 + "\n")
        for entry in log:
            f.write(entry + "\n")
    print(f"Log saved to: {log_file}")


def main():
    print("=" * 40)
    print("   Smart File Organizer")
    print("=" * 40)

    folder_path = input("\nEnter folder path to organize: ").strip()

    try:
        print("\nOrganizing files...")
        files_moved, log = organize_folder(folder_path)

        if files_moved == 0:
            print("No files found to organize!")
        else:
            print(f"\nSuccessfully organized {files_moved} files!\n")
            print("Files moved:")
            for entry in log:
                print(f"  ✅ {entry}")

            show_summary(folder_path)
            save_log(log, folder_path)

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()