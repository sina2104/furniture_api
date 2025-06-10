# Furniture_detection

### Introduction
This is a furniture detction model trained on pytorch resnet50 model with synthetic dataset generated in Unreal engine and annoatated with coco-annotator.

---
### How to run it?
To run fastapi where you can upload your jpg file and get furniture annotations on the file -> run this code:
```shell
python3 app/main.py
```
The result with annotaions will also appear in the images folder:
```shell
app/images/Result.jpg
```

---
### Dataset
Dataset with the images made on UnrealEngine and their annotations has been uploaded publicly: [Huggingface_Dataset](https://huggingface.co/datasets/sina09/UnrealEngine_Furniture). 

### Color codes:
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Sofa`
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) `Chair`
- ![#1589F0](https://placehold.co/15x15/1589F0/1589F0.png) `Table`
### Example
![Test_result3](https://github.com/user-attachments/assets/9e59d87e-3a7b-4a95-9c8b-4ac2a2847488)
![Test_result2](https://github.com/user-attachments/assets/417030bf-7d39-4a64-b035-2e23a60a2c34)
![Test_result1](https://github.com/user-attachments/assets/60e55c5b-8176-494d-93f6-2b9538a6e486)
