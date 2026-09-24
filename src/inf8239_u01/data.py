import io
from pathlib import Path
import urllib.request
import zipfile
import pandas as pd


def download_csv(url: str, destination: str = "data/raw/dataset.csv") -> Path:
    if not url.startswith(("https://", "http://")):
        raise ValueError("La fuente debe ser una URL HTTP(S)")

    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Si es un archivo ZIP (caso del repositorio UCI)
    if url.endswith(".zip"):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req) as response:
            zip_content = response.read()

        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
            csv_files = [f for f in z.namelist() if f.endswith(".csv")]
            if not csv_files:
                raise ValueError(
                    "No se encontró ningún archivo CSV dentro del ZIP"
                )
            with z.open(csv_files[0]) as f:
                frame = pd.read_csv(f)
    else:
        frame = pd.read_csv(url)

    if frame.empty:
        raise ValueError("El dataset descargado está vacío")

    frame.to_csv(path, index=False)
    return path