from io import BytesIO
import zipfile
import py7zr
import mimetypes

def extract_archive_to_memory(filename: str, data: bytes) -> BytesIO:
    mem_out = BytesIO()
    # ZIP形式
    if filename.endswith(".zip"):
        mem_in = BytesIO(data)
        with zipfile.ZipFile(mem_in) as zf:
            with zipfile.ZipFile(mem_out, "w") as out_zf:
                for name in zf.namelist():
                    out_zf.writestr(name, zf.read(name))
    # 7z形式
    elif filename.endswith(".7z"):
        mem_in = BytesIO(data)
        with py7zr.SevenZipFile(mem_in) as zf:
            files = zf.readall()
            with zipfile.ZipFile(mem_out, "w") as out_zf:
                for name, content in files.items():
                    out_zf.writestr(name, content.read())
    else:
        # ZIP化してそのまま返す（展開不要な形式）
        mem_out.write(data)
    mem_out.seek(0)
    return mem_out
