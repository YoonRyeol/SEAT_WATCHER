def handle_uploaded_file(f):
    with open('test_image.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)