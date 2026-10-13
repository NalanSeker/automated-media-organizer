
"""Automated Media Organizer - a zero-dependency command-line utility.

Usage:
    python code.py --source /sourcefolderaddress
    python code.py --source /sourcefolderaddress --dest /organizedfolder --dry-run
    python code.py --source /sourcefolderaddress --date-prefix
"""
import argparse
import os
import shutil
import sys
from datetime import datetime

# Category name -> folder path (relative to the destination folder).
FOLDER_FOR_CATEGORY = {
    "IMAGES": "Sorted/Images",
    "VIDEO": "Sorted/Video",
    # Documents are split into sub-folders by document type.
    "WORD": "Sorted/Documents/Word",
    "POWERPOINT": "Sorted/Documents/PowerPoint",
    "EXCEL": "Sorted/Documents/Excel",
    "PDF": "Sorted/Documents/PDF",
    "TEXT": "Sorted/Documents/Text",
    "OTHER_DOCUMENTS": "Sorted/Documents/Other",
    "ARCHIVES_CODE": "Sorted/Archives_Code",
    "MISC": "Sorted/Misc",
}

# File extension (lowercase, no dot) -> category name.
CATEGORY_FOR_EXTENSION = {
    # Images
    "jpg": "IMAGES",
    "png": "IMAGES",
    "gif": "IMAGES",
    "svg": "IMAGES",
    # Videos
    "mp4": "VIDEO",
    "avi": "VIDEO",
    "mkv": "VIDEO",
    # Documents - Word
    "docx": "WORD",
    "doc": "WORD",
    # Documents - PowerPoint
    "pptx": "POWERPOINT",
    "ppt": "POWERPOINT",
    # Documents - Excel
    "xlsx": "EXCEL",
    "xls": "EXCEL",
    "csv": "EXCEL",
    # Documents - PDF and plain text
    "pdf": "PDF",
    "txt": "TEXT",
    # Documents - other formats
    "rtf": "OTHER_DOCUMENTS",
    "odt": "OTHER_DOCUMENTS",
    "md": "OTHER_DOCUMENTS",
    # Archives and code
    "zip": "ARCHIVES_CODE",
    "py": "ARCHIVES_CODE",
    "js": "ARCHIVES_CODE",
    "json": "ARCHIVES_CODE",
}

FALLBACK_FOLDER = "Sorted/Misc"      # these will be using for unknown or missing extensions
LOG_FILE_NAME = "activity.log"


# Step 1: Get the file extension

def get_clean_extension(file_name):
    file_name = file_name.strip()
    name_without_extension, extension = os.path.splitext(file_name)
    return extension.lstrip(".").lower()



# Step 2: Decide which folder a file belongs in

def find_destination_folder(destination_root, extension):
    """Return the full path of the folder where this extension should go."""
    if not extension:
        category_folder = FALLBACK_FOLDER
    else:
        category = CATEGORY_FOR_EXTENSION.get(extension)
        # .get() with a default replaces a long if/elif chain.
        category_folder = FOLDER_FOR_CATEGORY.get(category, FALLBACK_FOLDER)
    return os.path.join(destination_root, category_folder)



# Step 3: Avoid overwriting existing files

def make_unique_file_name(destination_folder, wanted_file_name):

    name_without_extension, extension = os.path.splitext(wanted_file_name)
    unique_file_name = wanted_file_name
    full_path = os.path.join(destination_folder, unique_file_name)
    copy_number = 1

    # lexists() also counts broken symlinks as "taken", so they are never
    # overwritten either.
    while os.path.lexists(full_path):
        unique_file_name = f"{name_without_extension}({copy_number}){extension}"
        full_path = os.path.join(destination_folder, unique_file_name)
        copy_number += 1

    return unique_file_name, full_path


# Step 4 (optional): Put the file's date in front of its name

def add_date_to_file_name(file_path, file_name):
    modified_time = os.path.getmtime(file_path)
    date_text = datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d")
    return f"{date_text}_{file_name}"


# Step 5: Record what happened

def write_log_entry(log_file_path, old_path, new_path, dry_run):
    time_text = datetime.now().isoformat(timespec="seconds")
    mode_label = "[DRY-RUN]" if dry_run else "[MOVED]"
    log_line = f"{time_text} {mode_label} {old_path} -> {new_path}"
    print(log_line)

    if not dry_run:
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(log_line + "\n")


# Step 6: The main organizing loop

def organize_files(source_folder, destination_folder, dry_run=False, date_prefix=False):
    source_folder = os.path.abspath(source_folder)
    destination_folder = os.path.abspath(destination_folder)

    #  Check that the source folder is valid.
    if not os.path.isdir(source_folder):
        raise NotADirectoryError(
            f"Source is not an existing directory: {source_folder}"
        )
    # Ensure we can always place the activity log in the destination root,
    # even if the destination folder does not already exist.
    if not dry_run:
        os.makedirs(destination_folder, exist_ok=True)

    counts = {"processed": 0, "skipped_directories": 0, "errors": 0}
    log_file_path = os.path.join(destination_folder, LOG_FILE_NAME)

    # 2. Look at every item in the source folder (sorted = same order everywhere).
    for item_name in sorted(os.listdir(source_folder)):
        item_path = os.path.join(source_folder, item_name)

        # Don't move our own log file if source and destination are the same.
        if os.path.abspath(item_path) == os.path.abspath(log_file_path):
            continue

        # 3. Only handle real files; skip sub-folders and symbolic links.
        if os.path.islink(item_path) or not os.path.isfile(item_path):
            counts["skipped_directories"] += 1
            continue

        try:
            # 4. Work out where the file should go and what it will be called.
            extension = get_clean_extension(item_name)
            target_folder = find_destination_folder(destination_folder, extension)

            wanted_file_name = item_name
            if date_prefix:
                wanted_file_name = add_date_to_file_name(item_path, item_name)

            _final_file_name, final_path = make_unique_file_name(
                target_folder, wanted_file_name
            )

            # 5. Move the file (skipped completely during a dry run).
            if not dry_run:
                os.makedirs(target_folder, exist_ok=True)
                shutil.move(item_path, final_path)

            # 6. Record the action.
            write_log_entry(log_file_path, item_path, final_path, dry_run)
            counts["processed"] += 1

        except (PermissionError, FileNotFoundError, OSError) as error:
            counts["errors"] += 1
            print(f"[ERROR] {item_path}: {error}", file=sys.stderr)

    # 7. Give the totals back to the caller.
    return counts



# Step 7: Command-line interface
def create_argument_parser():
    parser = argparse.ArgumentParser(
        description="Automated Media Organizer: sort files into category "
                    "folders by extension."
    )
    parser.add_argument("--source", required=True,
                        help="Folder to organize.")
    parser.add_argument("--dest", default=".",
                        help="Folder where 'Sorted' will be created "
                             "(default: current folder).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without changing any files.")
    parser.add_argument("--date-prefix", action="store_true",
                        help="Start file names with their YYYY-MM-DD modified date.")
    return parser


def main(argv=None):
    arguments = create_argument_parser().parse_args(argv)

    try:
        counts = organize_files(
            source_folder=arguments.source,
            destination_folder=arguments.dest,
            dry_run=arguments.dry_run,
            date_prefix=arguments.date_prefix,
        )
    except NotADirectoryError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("\n--- Summary ---")
    print(f"Processed files     : {counts['processed']}")
    print(f"Skipped directories : {counts['skipped_directories']}")
    print(f"Errors              : {counts['errors']}")
    if arguments.dry_run:
        print("(dry run - no files were changed)")

    return 1 if counts["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())