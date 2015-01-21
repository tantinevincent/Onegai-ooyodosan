class Status:
    def __init__(self, status_list):
        self.status_list = status_list
        
    def get_images(self, need_small=False):
        status_imgs = []
        for status in self.status_list:
            img = "status_" + status + (".png" if not need_small else "_small.png")
            status_imgs.append(img)

        return status_imgs
     
if __name__ == "__main__":
    status = Status(["heavily_damage", "minor_damage"])
    for status_img in status.get_images(need_small=True):
        print status_img