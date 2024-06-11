import torch
from PIL import Image
import torchvision.transforms as transforms

# Function to define your model architecture
def create_model_architecture():
    # Example: use a pre-trained ResNet18
    from torchvision import models
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, 1000)  # Adjust based on your model's output classes
    return model

# Load the model
model = create_model_architecture()
model.load_state_dict(torch.load('best.pt'))
model.eval()  # Set the model to evaluation mode

# Load and preprocess the image
image_path = 'path_to_your_image/image.jpg'
image = Image.open(image_path).convert('RGB')

# Define the transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to the size your model expects
    transforms.ToTensor(),          # Convert the image to a PyTorch tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize
])

# Apply the transformations
image = transform(image)
image = image.unsqueeze(0)  # Add a batch dimension

# Perform inference
with torch.no_grad():
    output = model(image)

# Get the predicted class
_, predicted_class = torch.max(output, 1)
print(f'Predicted class: {predicted_class.item()}')

# If you have a list of class names
class_names = ['class1', 'class2', 'class3', ...]  # Replace with your actual class names
print(f'Predicted class name: {class_names[predicted_class.item()]}')
