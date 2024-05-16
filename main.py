from rembg import remove
from PIL import ImageSequence, Image
import glob

def get_avg_fps(PIL_Image_object):
    """ Returns the average framerate of a PIL Image object """
    PIL_Image_object.seek(0)
    frames = duration = 0
    while True:
        try:
            frames += 1
            duration += PIL_Image_object.info['duration']
            PIL_Image_object.seek(PIL_Image_object.tell() + 1)
        except EOFError:
            return frames / duration * 1000
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print() 
files = glob.glob("img/*.gif")
it = 0
for file in files:
    filename = file.removeprefix("img/")
    printProgressBar(it, len(files), f"{it}/{len(files)}", filename)
    
    output = f"output/{filename}"
    final_frames = []
    with Image.open(file) as im:
        
        for frame in ImageSequence.Iterator(im):
            final_frames.append(remove(frame))
        final_frames[0].save(output,
                save_all=True, append_images=final_frames[1:], optimize=False,disposal=2, duration=get_avg_fps(im),  loop=0)
    it+=1