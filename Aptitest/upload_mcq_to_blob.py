"""
Upload MCQ questions from Excel to Azure Blob Storage.
Excel columns: Qn, Opt01, Opt02, Opt03, Opt04
Output JSON format per question: [{"Qn": "...", "Opt01": "...", "Opt02": "...", "Opt03": "...", "Opt04": "..."}]
Blob naming: QA{DDMMYYHHMM}EM{idx}.json (e.g. QA051225001EM01.json)
"""
import json
from datetime import datetime
import openpyxl
from django.http import HttpResponse
from rest_framework.decorators import api_view
from ExskilenceTest.Blob_service import upload_blob

BLOB_PREFIX = "test_InterviewQuestion/NEWQns/mcq/"


def _cell_to_str(val):
    """Convert cell value to string. Preserves 0 as '0'. Formats 0.1 as '10%' when stored as decimal."""
    if val is None:
        return ""
    if isinstance(val, float) and 0 <= val <= 1 and val not in (0.0, 1.0):
        return str(int(round(val * 100))) + "%"
    return str(val).strip()


def _parse_mcq_from_excel(excel_file):
    """Parse Excel and return list of dicts with keys: Qn, Opt01, Opt02, Opt03, Opt04."""
    wb = openpyxl.load_workbook(excel_file, read_only=True, data_only=False)
    ws = wb.active
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    wb.close()
    if not rows:
        return []
    header = [_cell_to_str(c) if c is not None else "" for c in rows[0]]
    qn_col = next((i for i, h in enumerate(header) if str(h).lower() == "qn"), 0)
    opt01_col = next((i for i, h in enumerate(header) if str(h).lower() == "opt01"), 1)
    opt02_col = next((i for i, h in enumerate(header) if str(h).lower() == "opt02"), 2)
    opt03_col = next((i for i, h in enumerate(header) if str(h).lower() == "opt03"), 3)
    opt04_col = next((i for i, h in enumerate(header) if str(h).lower() == "opt04"), 4)
    questions = []
    for idx, row in enumerate(rows[1:], start=1):
        if not row:
            continue
        qn = row[qn_col] if qn_col < len(row) else None
        if qn is None or (isinstance(qn, str) and not qn.strip()):
            continue
        qn_str = _cell_to_str(qn)
        qn_str = qn_str.replace("\r\n", "\n").replace("\r", "\n")  # normalize line endings
        questions.append({
            "Qn": qn_str,
            "Opt01": _cell_to_str(row[opt01_col] if opt01_col < len(row) else None),
            "Opt02": _cell_to_str(row[opt02_col] if opt02_col < len(row) else None),
            "Opt03": _cell_to_str(row[opt03_col] if opt03_col < len(row) else None),
            "Opt04": _cell_to_str(row[opt04_col] if opt04_col < len(row) else None),
        })
    return questions


@api_view(["POST"])
def upload_mcq_questions(request):
    """Accept Excel file, parse MCQ rows, upload each as JSON to blob."""
    try:
        excel_file = request.FILES.get("file")
        if not excel_file:
            return HttpResponse(
                json.dumps({"status": "error", "data": "No file provided. Use form-data key 'file'."}),
                content_type="application/json",
                status=400,
            )
        if not excel_file.name.endswith((".xlsx", ".xls")):
            return HttpResponse(
                json.dumps({"status": "error", "data": "Only .xlsx or .xls files allowed."}),
                content_type="application/json",
                status=400,
            )
        if excel_file.name.endswith(".xls"):
            return HttpResponse(
                json.dumps({"status": "error", "data": "Please use .xlsx format."}),
                content_type="application/json",
                status=400,
            )
        questions = _parse_mcq_from_excel(excel_file)
        if not questions:
            return HttpResponse(
                json.dumps({
                    "status": "error",
                    "data": "No valid rows found. Ensure columns: Qn, Opt01, Opt02, Opt03, Opt04.",
                }),
                content_type="application/json",
                status=400,
            )
        uploaded = []
        failed = []
        dt = datetime.utcnow()
        dt_str = dt.strftime("%d%m%y%H%M")  # DDMMYYHHMM e.g. 051225001
        for idx, q in enumerate(questions, start=1):
            try:
                blob_name = f"{BLOB_PREFIX}QA{dt_str}EM{idx:02d}.json"
                json_content = json.dumps([q], ensure_ascii=False, indent=2)
                upload_blob(blob_name, json_content)
                uploaded.append(blob_name)
            except Exception as e:
                failed.append({"row": idx, "error": str(e)})
        return HttpResponse(
            json.dumps({
                "status": "success" if not failed else "partial",
                "uploaded": len(uploaded),
                "failed": len(failed),
                "blob_names": uploaded,
                "errors": failed,
            }),
            content_type="application/json",
        )
    except Exception as e:
        return HttpResponse(
            json.dumps({"status": "error", "data": str(e)}),
            content_type="application/json",
            status=500,
        )
