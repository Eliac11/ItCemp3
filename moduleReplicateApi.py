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

if __name__ == "__main__":
    ReplicateInterface("r8_7LQDYseC2kXuZYlhqpIEp3Kt7V4UXLH3M0Lxp").imageInpaiting("realistic, forest, Russia", "./tmp/hjfds.png")