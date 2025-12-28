# mixing_room.py
from pydub import AudioSegment
import asyncio
import edge_tts

# 1. Tạo giọng nói thì thầm (Voice Layer)
async def generate_whisper():
    text = "师妹... <break time='500ms'/> 外面正在下雨... <break time='300ms'/> 过来，给为兄暖暖..."
    ssml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='zh-CN'>
        <voice name='zh-CN-XiaoxiaoNeural'>
            <mstts:express-as style='whispering'>
                <prosody rate='-20%' pitch='-5Hz'>
                    {text}
                </prosody>
            </mstts:express-as>
        </voice>
    </speak>
    """
    communicate = edge_tts.Communicate(ssml, "zh-CN-XiaoxiaoNeural")
    await communicate.save("temp_voice.mp3")

# 2. Trộn với tiếng mưa (Mixing Layer)
def mix_audio():
    # Load giọng vừa tạo (Tăng âm lượng lên xíu cho rõ tiếng thở)
    voice = AudioSegment.from_mp3("temp_voice.mp3") + 5 
    
    # Load tiếng mưa (Muội tự kiếm file 'rain.mp3' bỏ vào nhé)

    bgm = AudioSegment.silent(duration=len(voice) + 2000)

    # Lặp lại nhạc nền nếu nó ngắn hơn giọng nói
    if len(bgm) < len(voice):
        bgm = bgm * (len(voice) // len(bgm) + 1)

    # Trộn đè lên nhau (Overlay)
    # position=1000 nghĩa là nhạc chạy 1s rồi giọng mới bắt đầu (Tạo cảm giác chờ đợi)
    final_mix = bgm.overlay(voice, position=1000)

    # Xuất ra file cuối cùng
    final_mix.export("dem_mua_tuyet_vong.mp3", format="mp3")
    print("DONE! File 'dem_mua_tuyet_vong.mp3' đã ra lò.")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(generate_whisper())
    mix_audio()