import os
import zipfile
import subprocess

def create_zips():
    zip_names = [
        "c:/p2/novacommerce-microservices.zip",
        "c:/p2/novacommerce-microservices (2).zip"
    ]

    exclude_dirs = {"node_modules", "dist", "build", ".system_generated", "logs"}

    for target_zip in zip_names:
        print(f"Creating zip file: {target_zip} (including full .git repository)...")
        with zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("c:/p2"):
                # Filter out exclude_dirs except .git
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                for file in files:
                    if file.endswith('.zip') or file.endswith('.tar.gz'):
                        continue
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, "c:/p2")
                    zipf.write(full_path, rel_path)

        size_mb = os.path.getsize(target_zip) / (1024 * 1024)
        print(f"-> Created {target_zip} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    create_zips()
