import shutil
import zipfile
from pathlib import Path

from django.conf import settings


def extract_source_archive_for_scan(scan_job):
    source_archive_path = Path(scan_job.source_file.path)
    extract_dir = Path(settings.STORAGE_ROOT) / "scans" / str(scan_job.id) / "extracted"

    if not source_archive_path.exists():
        raise FileNotFoundError("Source archive file does not exist.")

    if not zipfile.is_zipfile(source_archive_path):
        raise ValueError("Uploaded file is not a valid zip file.")

    if extract_dir.exists():
        shutil.rmtree(extract_dir)

    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(source_archive_path, "r") as zip_file:
        validate_zip_members(zip_file)
        zip_file.extractall(extract_dir)

    extracted_files_count = count_extracted_files(extract_dir)

    return {
        "extract_path": str(extract_dir),
        "extracted_files_count": extracted_files_count,
    }


def validate_zip_members(zip_file):
    for member_name in zip_file.namelist():
        member_path = Path(member_name)

        if member_path.is_absolute() or ".." in member_path.parts:
            raise ValueError(f"Unsafe zip path detected: {member_name}")


def count_extracted_files(extract_dir):
    return sum(1 for path in extract_dir.rglob("*") if path.is_file())
