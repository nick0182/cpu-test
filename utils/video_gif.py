from moviepy.editor import VideoFileClip

if __name__ == '__main__':
    video = VideoFileClip(target_resolution=(270, 480),
                          filename="C:\\path\\to\\original\\video.mp4")
    video = video.set_end(t=3)
    video.write_gif(filename="C:\\path\\to\\video_gif.gif")
