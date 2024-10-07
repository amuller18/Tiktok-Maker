import tts
import parser
import assembler
import youtube_ripper
import stt

reddit_link = 'https://www.reddit.com/r/nosleep/comments/1fsdz1d/acne_took_over_my_neck_then_my_entire_life/' #input('Please input the reddit link. ')
youtube_link = 'https://www.youtube.com/watch?v=s600FYgI5-s'
textData = parser.get_reddit_story(reddit_link)

text = textData[0]
paragraphs = textData[1]
print(paragraphs[1])
tts = tts.tts()
tts.make_tts(text)

print('Getting Youtube')
youtube_ripper.get_video_and_prepare(youtube_link)

print('Editing Video')

assembler = assembler.editor()

assembler.add_subtitles('subtitles.srt', 'edited_video_1080x1920.mp4')
assembler.trim_video_to_audio_length('TTS.wav')

#parser.getImages(paragraphs)
