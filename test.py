import time
import pychromecast

if __name__ == "__main__":
    services, browser = pychromecast.discovery.discover_chromecasts()
    pychromecast.discovery.stop_discovery(browser)
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["SHIELD"])
    cast = chromecasts[0]
    cast.wait()
    mc = cast.media_controller
    mc.play_media("https://media.mads.monster/sound/untitled.mp3", content_type = "audio/mpeg")
    mc.block_until_active()
    mc.play()