class SignalControl:
    image_loaded = False
    result_image_loaded = False

    def set_image_loaded(self, image_loaded):
        self.image_loaded = image_loaded

    def get_image_loaded(self):
        return self.image_loaded

    def set_result_image_loaded(self, result_image_loaded):
        self.result_image_loaded = result_image_loaded

    def get_result_image_loaded(self):
        return self.image_loaded
