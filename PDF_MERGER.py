from pathlib import Path
from difflib import get_close_matches

from pypdf import PdfReader, PdfWriter

# Como executar (Windows): no terminal desta pasta, rode: py PDF_MERGER.py

base_dir = Path(__file__).resolve().parent
pdfs = [
    "questionarios_diana.pdf",
    "questionarios_dina.pdf",
    "questionarios_chico.pdf",
    "questionarios_lena.pdf",
    "questionarios_rafa.pdf",
]
output_file = base_dir / "merged_questionarios.pdf"
temp_output_file = base_dir / "merged_questionarios.tmp.pdf"

available_pdfs = sorted(p.name for p in base_dir.glob("*.pdf"))
missing = [name for name in pdfs if not (base_dir / name).exists()]

if missing:
    details = []
    for name in missing:
        person_token = Path(name).stem.split("_")[-1]
        same_person_candidates = [
            item for item in available_pdfs if Path(item).stem.split("_")[-1] == person_token
        ]
        suggestion_pool = same_person_candidates if same_person_candidates else available_pdfs
        suggestion = get_close_matches(name, suggestion_pool, n=1, cutoff=0.5)
        if suggestion:
            details.append(f"- {name} (quizas quiseste dizer: {suggestion[0]})")
        else:
            details.append(f"- {name}")

    raise FileNotFoundError(
        "Ficheiros nao encontrados:\n"
        + "\n".join(details)
        + "\n\nPDFs disponiveis na pasta:\n- "
        + "\n- ".join(available_pdfs)
    )

merger = PdfWriter()
for pdf_name in pdfs:
    source_path = base_dir / pdf_name
    reader = PdfReader(str(source_path), strict=True)
    for page in reader.pages:
        merger.add_page(page)

merger.write(str(temp_output_file))
merger.close()

# Validate the generated PDF before replacing the final output.
PdfReader(str(temp_output_file), strict=True)
temp_output_file.replace(output_file)