import folium
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import imgkit

from src.geomapper.map import GeoMapper
import os


app = FastAPI(
    title="GeoMapper",
    description="Tool for creating interactive geospatial maps using Folium",
)


@app.get("/generate_map_code", response_class=HTMLResponse)
def get_map_code(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
):
    """
    Endpoint to return the interactive map as an HTML code response based on input coordinates.
    """
    location = [lat, lon]
    geomap = GeoMapper(location, zoom_start=14)
    geomap.add_marker(location, popup=f"Coordinates: {lat}, {lon}")
    file_path = f"generated_maps/map-{lat}-{lon}.html"
    geomap.save_map(file_path)

    with open(file_path, "r") as f:
        map_html = f.read()

    return HTMLResponse(content=map_html, status_code=200)


@app.get("/download_map")
def download_map(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
):
    """
    Endpoint to download the generated map as an HTML file based on input coordinates.
    """
    location = [lat, lon]

    geomap = GeoMapper(location, zoom_start=14)
    geomap.add_marker(location, popup=f"Coordinates: {lat}, {lon}")

    # Define the path for the downloadable map file
    file_path = f"generated_maps/downloadable_map-{lat}-{lon}.html"

    # Save the map as an HTML file
    geomap.save_map(file_path)

    # Check if the file exists and return it; otherwise, raise an HTTPException
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="application/octet-stream",
            filename=f"generated_maps/downloadable_map-{lat}-{lon}.html",
        )
    else:
        raise HTTPException(status_code=404, detail="Map file not found")


@app.get("/get_map_image")
def get_map_image(lat: float, lon: float, zoom_level: int = 12):
    """
    Endpoint to view the generated map as an image based on input coordinates.
    """
    map_center = [lat, lon]
    mymap = folium.Map(location=map_center, zoom_start=zoom_level, control_scale=True)

    # Add a marker
    folium.Marker(
        location=map_center,
        popup="Location",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(mymap)

    map_html_path = f"generated_maps/map-{lat}-{lon}.html"
    mymap.save(map_html_path)

    # Update the HTML to set a fixed size for the map
    with open(map_html_path, "r+") as f:
        html_content = f.read()
        html_content = html_content.replace(
            '<div class="folium-map" ',
            '<div class="folium-map" style="width: 1200px; height: 600px;" ',
        )
        f.seek(0)
        f.write(html_content)
        f.truncate()

    # Convert the HTML to an image
    img_path = "generated_maps/map_image.png"
    imgkit.from_file(map_html_path, img_path)

    # Read the image file to return as response
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            return HTMLResponse(content=img_file.read(), media_type="image/png")

    raise HTTPException(status_code=500, detail="Image generation failed.")


@app.get("/healthcheck")
def health_check():
    """
    Root endpoint to serve a simple check to see if the server is up and running.
    """
    return {"message": "Welcome to GeoMapper API"}
