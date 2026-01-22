import pygame
from os import walk

def import_folder(path) :
    surface_list = []
    for _,__,img_files in walk(path) :
        for image in img_files :
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path)
            image_surf = pygame.transform.scale_by(image_surf, 4).convert_alpha()
            surface_list.append(image_surf)
    return surface_list