# Copyright [2019] [Hayden Nix]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests


class ColorGen:
    colormind_url = "http://colormind.io/api/"
    colorapi_url = "https://www.thecolorapi.com/scheme"

    # Returns JSON Object with a 5 color scheme
    def _get_random_color_scheme(self):
        return requests.post(self.colormind_url, json={
            "model": "default"
        }).json()

    def _get_monochrome_colors(self, color, number):
        params = {
            "rgb": self._create_color_param(color),
            "mode": "monochrome",
            "count": number
        }
        return requests.get(self.colorapi_url, params=params).json()['colors']

    def _create_color_param(self, color):
        return str(color[0]) + "," + str(color[1]) + "," + str(color[2])