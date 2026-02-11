import pygame
from os import walk

def import_folder(path, scale):
    surface_list = []

    for _, __, img_files in walk(path):
        # --- ETAPE CRUCIALE : Trier la liste des noms de fichiers ---
        img_files.sort() 
        
        for image in img_files :
            if image.endswith(('.png', '.jpg', '.jpeg')) :
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                image_surf = pygame.transform.scale_by(image_surf, scale)
                surface_list.append(image_surf)

    return surface_list
