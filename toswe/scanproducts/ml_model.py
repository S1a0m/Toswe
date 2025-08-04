# ml_model.py
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image

class ProductImageEmbedder:
    def __init__(self, device="cpu"):
        self.device = torch.device(device)
        self.model = resnet50(pretrained=True)
        self.model.fc = torch.nn.Identity()  # remove classification head
        self.model.eval()
        self.model.to(self.device)

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
        ])

    def extract_embedding(self, image: Image.Image) -> torch.Tensor:
        """Transforme une image PIL en embedding 2048D."""
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.model(input_tensor)
        return embedding.squeeze()
