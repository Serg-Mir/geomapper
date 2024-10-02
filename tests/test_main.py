import unittest
from fastapi.testclient import TestClient
from src.main import app


class TestGeoMapperAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome to GeoMapper API"})

    def test_generate_map_code(self):
        response = self.client.get("/generate_map_code?lat=35.6762&lon=139.6503")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "<html>", response.text
        )  # Adjust this check based on expected content

    def test_download_map(self):
        lat = 47.9105
        lon = 33.3918
        response = self.client.get(f"/download_map?lat={lat}&lon={lon}&zoom=12")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/octet-stream"

        # Extracting the filename from the Content-Disposition header
        content_disposition = response.headers["content-disposition"]

        # Splitting the content_disposition string to find the filename
        filename = None
        for part in content_disposition.split(";"):
            if "filename=" in part:
                filename = part.split("=")[1].strip('"')
                break

        assert filename == f"generated_maps/downloadable_map-{lat}-{lon}.html"

        # we check the content of the response
        assert (
            "html" in response.content.decode()
        )  # Check if the response content is HTML
