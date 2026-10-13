
import os

from code import (
    add_date_to_file_name,
    find_destination_folder,
    get_clean_extension,
    make_unique_file_name,
    organize_files,
)


def test_get_clean_extension():
    assert get_clean_extension("photo.JPG") == "jpg"
    assert get_clean_extension("report.pdf") == "pdf"
    assert get_clean_extension("README") == ""


def test_find_destination_folder(tmp_path):
    assert find_destination_folder(str(tmp_path), "jpg") == os.path.join(
        str(tmp_path), "Sorted/Images"
    )
    assert find_destination_folder(str(tmp_path), "unknown") == os.path.join(
        str(tmp_path), "Sorted/Misc"
    )
    assert find_destination_folder(str(tmp_path), "") == os.path.join(
        str(tmp_path), "Sorted/Misc"
    )


def test_make_unique_file_name(tmp_path):
    (tmp_path / "report.pdf").write_text("first", encoding="utf-8")

    name, path = make_unique_file_name(str(tmp_path), "report.pdf")
    assert name == "report(1).pdf"
    assert path == str(tmp_path / "report(1).pdf")


def test_date_prefix(tmp_path):
    source = tmp_path / "resume.pdf"
    source.write_text("test", encoding="utf-8")

    result = add_date_to_file_name(str(source), "resume.pdf")

    assert result.endswith("_resume.pdf")
    assert len(result.split("_", 1)[0]) == 10


def test_dry_run_does_not_move_files(tmp_path):
    source = tmp_path / "input"
    destination = tmp_path / "output"
    source.mkdir()

    file_path = source / "photo.JPG"
    file_path.write_text("image data", encoding="utf-8")

    counts = organize_files(
        str(source), str(destination), dry_run=True
    )

    assert file_path.exists()
    assert counts["processed"] == 1
    assert counts["errors"] == 0
    assert not destination.exists()


def test_organize_files_moves_and_classifies(tmp_path):
    source = tmp_path / "input"
    destination = tmp_path / "output"
    source.mkdir()

    (source / "report.pdf").write_text("document", encoding="utf-8")
    (source / "photo.JPG").write_text("image", encoding="utf-8")
    (source / "unknown.xyz").write_text("other", encoding="utf-8")

    counts = organize_files(str(source), str(destination))

    assert not (source / "report.pdf").exists()
    assert (destination / "Sorted" / "Documents" / "PDF" / "report.pdf").exists()
    assert (destination / "Sorted" / "Images" / "photo.JPG").exists()
    assert (destination / "Sorted" / "Misc" / "unknown.xyz").exists()
    assert counts["processed"] == 3
    assert counts["errors"] == 0


def test_invalid_source_directory(tmp_path):
    missing = tmp_path / "does-not-exist"

    try:
        organize_files(str(missing), str(tmp_path / "output"))
        assert False, "Expected NotADirectoryError"
    except NotADirectoryError:
        pass
