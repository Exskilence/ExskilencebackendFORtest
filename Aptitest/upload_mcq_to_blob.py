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


def _parse_mcq_from_excel(excel_file):
    """Parse Excel and return list of dicts with keys: Qn, Opt01, Opt02, Opt03, Opt04."""
    wb = openpyxl.load_workbook(excel_file, read_only=True, data_only=False)
    ws = wb.active
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    wb.close()
    if not rows:
        return []
    header = [str(c).strip() if c else "" for c in rows[0]]
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
        if not qn:
            continue
        qn_str = str(qn).strip() if qn else ""
        qn_str = qn_str.replace("\r\n", "\n").replace("\r", "\n")  # normalize line endings
        questions.append({
            "Qn": qn_str,
            "Opt01": str(row[opt01_col]).strip() if opt01_col < len(row) and row[opt01_col] else "",
            "Opt02": str(row[opt02_col]).strip() if opt02_col < len(row) and row[opt02_col] else "",
            "Opt03": str(row[opt03_col]).strip() if opt03_col < len(row) and row[opt03_col] else "",
            "Opt04": str(row[opt04_col]).strip() if opt04_col < len(row) and row[opt04_col] else "",
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
