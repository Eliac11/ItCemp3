import replicate
import os
import requests
import shutil
import datetime

class ReplicateInterface:
    def __init__(self,rep_token):

        os.environ["REPLICATE_API_TOKEN"] = rep_token

        self.imgsfolder = "./tmp/"
        if not os.path.exists(self.imgsfolder):
            os.makedirs(self.imgsfolder)

    def imageInpaiting(self, prompt,imgpath):
        output = replicate.run(
            "jagilley/controlnet-scribble:435061a1b5a4c1e26740464bf786efdfa9cb3a3ac488595a2de23e143fdb0117",
            input={"image": open(imgpath, "rb"),
                   "prompt":prompt}
        )
        newname = "_".join([prompt,datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")])
        self._loadimg(output[1],newname + ".png")
        return self.imgsfolder + newname

    def _loadimg(self,url,imgname):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(self.imgsfolder + imgname, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                return "ok"
        return "error"

paint_style = {"Realism": "forest, Finland, realism, lake",
                   "Cubism": "forest, Finland, abstraction, cubism, lake",
                   "Watercolour": "forest, Finland, watercolour, old version, lake",
                   "Oil": "forest, Finland, oil painting, large strokes, old version, lake",
                   "Charcoal": "forest, Finland, painting with charcoal, lake",
                   "Colour pencil": "forest, Finland, pencil paint, old version, lake",
                   "Black pencil": "forest, Finland, black pencil paint, old version, lake",
                   "Kashtanov": "Painting in the style of the artist Kashtanov, forest, Finland, watercolour, lake, sadness, very faded color",
                   "Ivanenko" : "Graphics paint, black pencil paint, big strokes, sharp lines",
                   "Anime" : "Russian forest, anime",
                   "Embroidery" : "only Karelian embroidery, 2d image, red thread, white linen, geomitrical elements"}

if __name__ == "__main__":
    ReplicateInterface("r8_DCtHIoSpvwN9qJfGRVnfvRgy0xsOhy92BrK04").imageInpaiting(str(paint_style[style]), str(image))