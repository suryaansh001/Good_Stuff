import os
import xml.etree.ElementTree as ET

# Paths to dataset
VOC_ANNOTATIONS_PATH = "./dataset/roadsign/annotations"
YOLO_LABELS_PATH = "./dataset/labels"
CLASSES_FILE = "./dataset/classes.txt"

# Ensure output directory exists
os.makedirs(YOLO_LABELS_PATH, exist_ok=True)

# Get class names from XML files
classes = set()

def convert_voc_to_yolo(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    image_filename = root.find("filename").text
    image_width = int(root.find("size/width").text)
    image_height = int(root.find("size/height").text)
    
    yolo_filename = os.path.join(YOLO_LABELS_PATH, image_filename.replace(".jpg", ".txt"))
    
    with open(yolo_filename, "w") as yolo_file:
        for obj in root.findall("object"):
            class_name = obj.find("name").text
            classes.add(class_name)

            # Bounding box coordinates
            bbox = obj.find("bndbox")
            x_min = int(bbox.find("xmin").text)
            y_min = int(bbox.find("ymin").text)
            x_max = int(bbox.find("xmax").text)
            y_max = int(bbox.find("ymax").text)
            
            # Convert to YOLO format
            x_center = (x_min + x_max) / (2.0 * image_width)
            y_center = (y_min + y_max) / (2.0 * image_height)
            width = (x_max - x_min) / image_width
            height = (y_max - y_min) / image_height
            
            yolo_file.write(f"{class_name} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

# Process all XML files
for xml_file in os.listdir(VOC_ANNOTATIONS_PATH):
    if xml_file.endswith(".xml"):
        convert_voc_to_yolo(os.path.join(VOC_ANNOTATIONS_PATH, xml_file))

# Save class names to a file
with open(CLASSES_FILE, "w") as class_file:
    class_file.write("\n".join(sorted(classes)))

print("✅ Conversion Completed! Check your labels in", YOLO_LABELS_PATH)
