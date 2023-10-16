def draw_text(text, font, text_color, surface, x=0, y=0, center=False):
    img = font.render(text, True, text_color)
    if center:
        text_rect = img.get_rect(center=(surface.get_width()/2, surface.get_height()/2))
        surface.blit(img, text_rect)
    else:
        surface.blit(img, (x, y))