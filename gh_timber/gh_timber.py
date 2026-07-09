class Timber:
    def __init__(self, length=1, width=1, height=1):
        self.length = length
        self.width = width
        self.height = height

    def volume(self):
        return self.length * self.width * self.height
    
    def __str__(self):
        return f"Timber(length={self.length}, width={self.width}, height={self.height}, volume={self.volume()})"