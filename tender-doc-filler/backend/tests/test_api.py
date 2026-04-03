import pytest
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app
from backend.models import FieldResult, Confidence


MOCK_FIELDS = [
    FieldResult(
        location_id="T0R0", location_type="table_cell", label="Firma",
        original_value="", filled_value="TestFirma Sp. z o.o.",
        confidence=Confidence.HIGH,
    ),
]


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def uploaded_doc(client, simple_table_docx):
    with patch("backend.main.analyze_ai", return_value=MOCK_FIELDS):
        with open(simple_table_docx, "rb") as f:
            resp = client.post("/api/upload", files={"file": ("test.docx", f)})
    assert resp.status_code == 200
    return resp.json()


def test_upload_docx(client, simple_table_docx):
    with patch("backend.main.analyze_ai", return_value=MOCK_FIELDS):
        with open(simple_table_docx, "rb") as f:
            resp = client.post("/api/upload", files={"file": ("test.docx", f)})
    assert resp.status_code == 200
    data = resp.json()
    assert "document_id" in data
    assert data["filled_fields"] > 0


def test_upload_invalid_format(client, tmp_path):
    txt = tmp_path / "test.txt"
    txt.write_text("not a docx")
    with open(txt, "rb") as f:
        resp = client.post("/api/upload", files={"file": ("test.txt", f)})
    assert resp.status_code == 400
    assert resp.json()["detail"]["code"] == "INVALID_FORMAT"


def test_get_document(client, uploaded_doc):
    doc_id = uploaded_doc["document_id"]
    resp = client.get(f"/api/documents/{doc_id}")
    assert resp.status_code == 200
    assert resp.json()["document_id"] == doc_id


def test_get_document_not_found(client):
    resp = client.get("/api/documents/nonexistent-uuid")
    assert resp.status_code == 404


def test_download_filled(client, uploaded_doc):
    doc_id = uploaded_doc["document_id"]
    resp = client.get(f"/api/documents/{doc_id}/download")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def test_get_profile(client):
    resp = client.get("/api/profile")
    assert resp.status_code == 200
    assert "nazwa_firmy" in resp.json()


def test_update_profile(client):
    resp = client.put("/api/profile", json={"nazwa_firmy": "Updated Corp", "nip": "999"})
    assert resp.status_code == 200
    resp2 = client.get("/api/profile")
    assert resp2.json()["nazwa_firmy"] == "Updated Corp"
