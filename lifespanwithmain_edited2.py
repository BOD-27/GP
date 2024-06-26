# -*- coding: utf-8 -*-
"""LifeSpanWithMain_edited.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/BOD-27/GP/blob/main/LifeSpanWithMain_edited.ipynb
"""

def import_libraries():
    global os, OrderedDict, TestOptions, CreateDataLoader, create_model, util, Visualizer, files
    import os
    from collections import OrderedDict
    from options.test_options import TestOptions
    from data.data_loader import CreateDataLoader
    from models.models import create_model
    import util.util as util
    from util.visualizer import Visualizer
    from google.colab import files

def mount_drive():
    from google.colab import drive
    drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
def clone_repo_and_install_deps():
    !git clone https://github.com/royorel/Lifespan_Age_Transformation_Synthesis
#     %cd Lifespan_Age_Transformation_Synthesis/
    !pip3 install -r requirements.txt

def download_models():
    !python download_models.py

def set_options():
    opt = TestOptions().parse(save=False)
    opt.display_id = 0
    opt.nThreads = 1
    opt.batchSize = 1
    opt.serial_batches = True
    opt.no_flip = True
    opt.in_the_wild = True
    opt.traverse = False
    opt.interp_step = 0.05
    opt.deploy = True
    return opt

def load_data_visualizer(opt):
    data_loader = CreateDataLoader(opt)
    dataset = data_loader.load_data()
    visualizer = Visualizer(opt)
    return dataset, visualizer

def load_model(model_name, opt):
    opt.name = model_name
    model = create_model(opt)
    model.eval()
    return model

def switch_model_gender(gender, opt):
    if gender.lower() == 'male':
        return load_model('males_model', opt)
    elif gender.lower() == 'female':
        return load_model('females_model', opt)
    else:
        raise ValueError("Invalid gender provided. Please provide either 'male' or 'female'.")

def upload_image():
    uploaded = files.upload()
    for filename in uploaded.keys():
        img_path = filename
        print('User uploaded file "{name}"'.format(name=filename))
    return img_path

def process_image_and_save_result(img_path, dataset, model, visualizer):
    from google.colab import drive
    drive.mount('/content/drive')
    base_drive_path = '/content/drive/My Drive/Lifespane'
    os.makedirs(base_drive_path, exist_ok=True)
    image_folder_name = os.path.splitext(os.path.basename(img_path))[0]
    image_folder_path = os.path.join(base_drive_path, image_folder_name)
    os.makedirs(image_folder_path, exist_ok=True)

    data = dataset.dataset.get_item_from_path(img_path)
    visuals = model.inference(data)
    out_path = os.path.join(image_folder_path, os.path.splitext(os.path.basename(img_path))[0].replace(' ', '') + '.png')
    visualizer.save_images_deploy(visuals, out_path)
    return image_folder_path



