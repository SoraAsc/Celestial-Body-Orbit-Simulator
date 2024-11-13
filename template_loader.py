import json
import numpy as np

from celestial_body import CelestialBody

class TemplateLoader:
    """This class handles the load and convertion of json to Celestial Body"""

    def __init__(self, template_file: str, template_name: str):
        """Initialize the template loader

        Args:
            template_file (str): Name of the file with the templates
        """
        self.template_name = template_name
        with open(template_file, 'r') as file:
            self.templates = json.load(file)

    def get_template(self, template_name: str) -> list[CelestialBody]:
        """Return a template configuration by name.

        Args:
            template_name (str): Name of the template inside the template file

        Returns:
            list[CelestialBody]: A list of celestial bodies
        """
        bodies = []
        self.template_name = template_name
        for data in self.templates.get(template_name, None):
            body = CelestialBody(
                name=data["name"],
                mass=data["mass"],
                position=np.array(data["position"], dtype="float64"),
                velocity=np.array(data["velocity"], dtype="float64"),
                color=data["color"]
            )
            bodies.append(body)
        return bodies
