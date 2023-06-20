import cv2
import torch
import torchvision

def inference(model, 
              device, 
              img_path, 
              treshold=0.5,
              label_dict=None):
    transforms = torchvision.transforms.ToTensor()
    model.eval()
    img_array = cv2.imread(img_path)
    img_tensor = transforms(img_array)
    img_tensor = img_tensor.to(device)
    with torch.no_grad():
        pred = model([img_tensor])

    boxes = pred[0]['boxes']
    scores = pred[0]['scores']
    boxes = boxes[scores > treshold]
    boxes_list = boxes.tolist()
    if label_dict:    
        labels = labels[scores > treshold]
        labels = pred[0]['labels']
        labels_list = labels.tolist()
        labels_list = [label_dict[i] for i in labels_list]
        return boxes_list,labels_list
    return boxes_list

if __name__ == '__main__':
    from utils import draw_bbox
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = torch.load('./weights/batchsize16_size512_loss_20155.pt',
                   map_location=device)
    img_path = './june.jpg'
    boxes_list = inference(model=model, device=device, img_path=img_path)
    output_img = draw_bbox(img_path, boxes_list)
    plt.imshow(output_img)
    plt.show()