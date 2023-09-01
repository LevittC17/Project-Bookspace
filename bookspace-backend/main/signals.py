from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import BookImage
from PIL import Image


# @receiver(post_save, sender=BookImage)
# def generate_thumbnail(sender, instance, **kwargs):
#     if not instance.thumbnail:
#         # Open the uploaded image using Pillow
#         image = Image.open(instance.cover_image.path)
#
#         # Resize the image to create the thumbnail
#         thumb_size = (100, 100)  # Adjust the size as needed
#         image.thumbnail(thumb_size)
#
#         # Save the thumbnail with a filename like "<book_name>-thumbnail.jpg"
#         thumbnail_filename = f"{instance.book.name}-thumbnail.jpg"
#         instance.thumbnail.save(thumbnail_filename, image)
