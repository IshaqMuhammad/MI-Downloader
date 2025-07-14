import time
import streamlit as st
import yt_dlp


def gui():
    st.set_page_config(page_title="MI Downloader", page_icon="20250714_164844.png")
    st.markdown(
    """
    <style>
    .stApp {
        background-image: url("background.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    st.markdown(
    "<h1 style='color: #FF5733; text-align: center;'>YouTube Video Downloader</h1>",
    unsafe_allow_html=True)
    video_link = st.text_input("Enter YouTube video link:")
    formate_choice = st.selectbox("Choose Video Formate:", ["Only Video","Only Audio","Both Video and Audio"])


    progress_bar = st.empty()
    status_text = st.empty()

    def progress_callback(d):
        if d['status'] == 'downloading':
            percent = d.get('progress',0)
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', d.get('total_bytes_estimate', 0))
            speed = d.get('speed', 0)
            title = d.get('info_dict',{}).get('title', 'Unknown')
            percent_complete = (downloaded/total) if total else 0
            progress_bar.progress(percent_complete)
            status_text.write(
                f"title: {title} |"
                f"Downloaded: {downloaded/1024/1024:.2f} MB / {total/1024/1024:.2f} MB |"
                f"Speed: {speed/1024:.2f} KB/s |"
                f"{percent_complete*100:.2f}%"
            )
        elif d['status'] =='finished':
            status_text.write('Download Finished!')

    def get_formate(choice):
        if choice == "Only Video":
            return 'bestvideo'
        elif choice == "Only Audio":
            return 'bestaudio'
        elif choice == 'Both Video and Audio':
            return 'best'

    def download(link, format_opt):
        timestamp = int(time.time())
        ydl_opts = {'outtmpl': f'%(title)s{timestamp}.%(ext)s','progress_hooks': [progress_callback], 'format':format_opt}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            return True
        except Exception as e:
            status_text.write(f"Error: {e}")
        return False
        
    if st.button("Download"):
        format_opt = get_formate(formate_choice)
        if download(video_link, format_opt):
            st.info("Video is downloaded")
        else:
            st.error("Failed to download video. Please check the link and try again.")
if __name__ == "__main__":
    gui()
